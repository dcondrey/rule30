"""
Deterministic fuel counter for Rule 30 P3 candidate programs.

WHY THIS EXISTS
---------------
The pre-registered evaluator (`evaluator.py`) estimates a candidate's
asymptotic exponent from WALL-CLOCK time.  On a loaded machine that
instrument failed its own sanity gate (see
`docs/rule30/RESULTS-openevolve-p3.md`): the unchanged naive baseline
scored 0.2667 / 0.2957 / 0.7896 against its own stored value, and the
constant-factor bit-packed control scored 0.9335 against a documented
0.210.  This module replaces the clock with an exact count of the work a
candidate performs, which is a pure function of the candidate's source and
of `n` -- no timeouts, no load sensitivity, no run-to-run variance.

THE CENTRAL HAZARD, AND THE RULE THAT CLOSES IT
-----------------------------------------------
A fuel counter that charges 1 unit per Python-level operation would be
catastrophically wrong here, in the mirror image of the wall-clock failure.
`reference/bigint_reference.py` advances an entire Rule 30 row with about
five Python bigint operations; one `row << 1` on a (2n+3)-bit integer is
ONE Python operation but performs ~n bits of work.  A naive counter would
report that constant-factor trick as an asymptotic breakthrough.

So the load-bearing rule of this module is:

    EVERY OPERATION WHOSE REAL COST GROWS WITH THE SIZE OF ITS OPERANDS IS
    CHARGED PROPORTIONALLY TO THAT SIZE.

and the rule that makes it auditable is:

    DEFAULT DENY.  An AST node type, a callable, or a combination of
    operand types that this module does not have an explicit cost rule for
    raises FuelModelError.  Nothing is ever charged "1 because we did not
    think about it".

MECHANISM
---------
The candidate's source is rewritten (`instrument_source`) so that every
cost-bearing construct is routed through a `FuelMeter` method:

    a + b            ->  __fuel__.binop('Add', a, b)
    -a               ->  __fuel__.unop('USub', a)
    a < b            ->  __fuel__.cmp('Lt', a, b)
    v[k]             ->  __fuel__.getitem(v, k)
    v[k] = x         ->  __fuel__.setitem(v, k, x)
    v[k] += x        ->  __fuel__.augitem(v, k, 'Add', x)
    f(x)             ->  __fuel__.call(f, x)
    for t in it:     ->  for t in __fuel__.tick(it):     (1 per iteration)
    while c:         ->  while __fuel__.tick1(c):        (1 per iteration)
    [e for x in it]  ->  [e for x in __fuel__.tick(it)]  (1 per iteration)
    f"{v}"           ->  f"{__fuel__.fmt(v)}"

SOUNDNESS ARGUMENT (why loops + calls + primitives is enough)
-------------------------------------------------------------
Any Python program's unbounded work must flow through one of exactly three
channels: (i) a loop, (ii) a (possibly recursive) call, (iii) a single
primitive operation on a variable-width value.  (i) is charged once per
iteration by `tick`/`tick1`, (ii) is charged once per invocation by `call`
-- and the callee's own body is instrumented, or it is a builtin with an
explicit table entry, or it is denied -- and (iii) is charged by size in
`binop`/`unop`/`cmp`/`getitem`/`setitem`/`call`.  Straight-line code
between these is O(1) and is deliberately not charged; it cannot carry
n-dependent work.  So no n-dependent work is uncharged.

WHAT IS DELIBERATELY *OVER*-CHARGED (conservative direction)
-------------------------------------------------------------
Multiplication and division of big integers are charged
`bits(a) * bits(b)`, i.e. the schoolbook bound.  CPython switches to
Karatsuba above ~2100 bits, so for very large operands this over-charges by
roughly max_bits**0.415.  That is conservative AGAINST a multiplication-
based candidate (it can only make such a candidate look worse, never
better), which is the safe direction for a gate whose job is to refuse
false positives.  RE-DERIVATION TRIGGER: if a search ever produces a winner
whose fuel is dominated by big-integer multiplication, this rule must be
replaced with a Karatsuba/FFT-aware one before the result is believed.
None of the sanity candidates, the seed program, or either reference
implementation multiplies.

WHAT IS NOT MODELLED (and is therefore denied outright)
--------------------------------------------------------
Imports (allowlist is empty), `eval`/`exec`/`compile`/`__import__`/
`getattr`/`setattr`/`globals`/`locals`/`vars`, async constructs, `yield`,
`match`, and any callable not in COST_TABLE / METHOD_COST that is not a
function defined inside the instrumented candidate module.  Each raises
FuelModelError naming the offending construct, so a candidate that would
have been mis-metered is rejected rather than mis-scored.
"""
from __future__ import annotations

import ast
import importlib.util
import types

METER_NAME = "__fuel__"


class FuelModelError(Exception):
    """The candidate used a construct with no explicit cost rule.

    This is a hard failure by design: an unmodelled construct is a hole in
    the instrument, and the whole point of this module is that there are
    none that are silently charged 1.
    """


class FuelExhausted(Exception):
    """Deterministic analogue of a timeout: the fuel budget was exceeded."""


# ---------------------------------------------------------------------------
# Size primitives
# ---------------------------------------------------------------------------

WORD_BITS = 30


def _bits(x: int) -> int:
    """Width of an integer in MACHINE WORDS -- the unit of the cost model.

    This is a word-RAM model: an operation on a value that fits in one
    64-bit word costs 1, and an operation on a k-word big integer costs k.
    Using words rather than bits is not cosmetic. Charging raw bit-length
    would put a spurious log n factor on every loop-index arithmetic and
    comparison (`i - 1`, `i + 1 < width`), which measurably inflates the
    naive O(n^2) simulation to a fitted 2.12-2.15 -- an instrument that
    cannot recover a known exponent. Under the word model, index
    arithmetic is O(1) as it is on real hardware, while a bitwise op on a
    (2n+3)-bit packed row still costs ~n/64, i.e. still proportional to n.
    The fitted EXPONENT is invariant to the choice of word size; only the
    constant changes.
    """
    n = x.bit_length()
    return (n + WORD_BITS - 1) // WORD_BITS if n > WORD_BITS else 1


_SEQ_TYPES = (list, tuple, str, bytes, bytearray, range)
_SET_TYPES = (set, frozenset)


def _elems(x) -> int:
    """Element count of a sized container; ndarray element count for arrays."""
    if isinstance(x, (list, tuple, str, bytes, bytearray, set, frozenset, dict)):
        return len(x) if len(x) > 0 else 1
    size = getattr(x, "size", None)  # numpy.ndarray and friends
    if isinstance(size, int):
        return size if size > 0 else 1
    raise FuelModelError(f"no size rule for value of type {type(x).__name__}")


def _is_array(x) -> bool:
    return (
        not isinstance(x, (list, tuple, str, bytes, bytearray, set, frozenset, dict, int, float, bool, complex))
        and isinstance(getattr(x, "size", None), int)
        and hasattr(x, "shape")
    )


# ---------------------------------------------------------------------------
# Operator classes
# ---------------------------------------------------------------------------

# Integer ops whose cost is linear in the widest operand/result.
# Note: _bits() returns WORDS, not bits (see its docstring).
_INT_LINEAR = {"Add", "Sub", "BitAnd", "BitOr", "BitXor", "LShift", "RShift"}
# Integer ops whose cost is (schoolbook) quadratic in the operand widths.
_INT_QUADRATIC = {"Mult", "Div", "FloorDiv", "Mod", "Pow", "MatMult"}

_ORDERING_CMPS = {"Lt", "LtE", "Gt", "GtE", "Eq", "NotEq"}


class FuelMeter:
    """Accumulates fuel. One meter per measured call; never shared."""

    __slots__ = ("fuel", "limit", "module_globals", "_denied")

    def __init__(self, limit: int | None = None):
        self.fuel = 0
        self.limit = limit
        self.module_globals = None
        self._denied = None

    # -- core charge ------------------------------------------------------
    def _charge(self, k: int) -> None:
        self.fuel += k
        if self.limit is not None and self.fuel > self.limit:
            raise FuelExhausted(f"fuel budget {self.limit} exceeded")

    # -- loops ------------------------------------------------------------
    def tick(self, iterable):
        """1 fuel per loop iteration."""
        for item in iterable:
            self._charge(1)
            yield item

    def tick1(self, value):
        """1 fuel per `while` test evaluation."""
        self._charge(1)
        return value

    # -- binary operators -------------------------------------------------
    def binop(self, op: str, a, b):
        ta, tb = type(a), type(b)
        # bool is a subclass of int; treat it under the integer rules so a
        # candidate cannot dodge width-proportional charging by mixing types.
        if isinstance(a, int) and isinstance(b, int):
            if op in _INT_LINEAR:
                r = _INT_BINOP[op](a, b)
                self._charge(max(_bits(a), _bits(b), _bits(r)))
                return r
            if op in _INT_QUADRATIC:
                if op == "MatMult":
                    raise FuelModelError("@ on ints")
                r = _INT_BINOP[op](a, b)
                self._charge(_bits(a) * _bits(b) + _bits(r))
                return r
            raise FuelModelError(f"no int rule for operator {op}")

        if _is_array(a) or _is_array(b):
            r = _INT_BINOP[op](a, b)
            self._charge(_elems(a) + _elems(b) + _elems(r) if _is_array(r) else _elems(a) + _elems(b))
            return r

        if op == "Mult" and (isinstance(a, _SEQ_TYPES) or isinstance(b, _SEQ_TYPES)):
            # sequence repetition: [0] * width  --  cost is the result length
            r = a * b
            self._charge(_elems(r))
            return r
        if op == "Add" and isinstance(a, _SEQ_TYPES) and isinstance(b, _SEQ_TYPES):
            r = a + b
            self._charge(_elems(r))
            return r
        if op in ("BitOr", "BitAnd", "Sub", "BitXor") and isinstance(a, _SET_TYPES) and isinstance(b, _SET_TYPES):
            r = _INT_BINOP[op](a, b)
            self._charge(_elems(a) + _elems(b) + _elems(r))
            return r
        if op == "BitOr" and isinstance(a, dict) and isinstance(b, dict):
            r = a | b
            self._charge(_elems(a) + _elems(b) + _elems(r))
            return r
        if op == "Mod" and isinstance(a, (str, bytes)):
            r = a % b
            self._charge(_elems(a) + _elems(r))
            return r
        if isinstance(a, (float, complex, bool)) and isinstance(b, (float, complex, bool, int)):
            self._charge(1)
            return _INT_BINOP[op](a, b)
        if isinstance(a, int) and isinstance(b, (float, complex, bool)):
            self._charge(1)
            return _INT_BINOP[op](a, b)
        raise FuelModelError(
            f"no cost rule for {ta.__name__} {op} {tb.__name__}"
        )

    # -- unary operators --------------------------------------------------
    def unop(self, op: str, a):
        if op == "Not":
            self._charge(1)
            return not a
        if type(a) is int:
            r = -a if op == "USub" else (+a if op == "UAdd" else ~a)
            self._charge(max(_bits(a), _bits(r)))
            return r
        if _is_array(a):
            r = -a if op == "USub" else (+a if op == "UAdd" else ~a)
            self._charge(_elems(a))
            return r
        if isinstance(a, (float, complex, bool)):
            self._charge(1)
            return -a if op == "USub" else (+a if op == "UAdd" else ~a)
        raise FuelModelError(f"no cost rule for unary {op} on {type(a).__name__}")

    # -- comparisons ------------------------------------------------------
    def cmp(self, op: str, a, b):
        if op in ("Is", "IsNot"):
            self._charge(1)
            return (a is b) if op == "Is" else (a is not b)

        if op in ("In", "NotIn"):
            self._charge(self._contains_cost(a, b))
            r = a in b
            return r if op == "In" else (not r)

        if op not in _ORDERING_CMPS:
            raise FuelModelError(f"no cost rule for comparison {op}")

        ta, tb = type(a), type(b)
        if isinstance(a, int) and isinstance(b, int):
            self._charge(max(_bits(a), _bits(b)))
        elif _is_array(a) or _is_array(b):
            self._charge(_elems(a) + _elems(b))
        elif isinstance(a, (str, bytes, bytearray, list, tuple)) and isinstance(
            b, (str, bytes, bytearray, list, tuple)
        ):
            self._charge(min(_elems(a), _elems(b)))
        elif isinstance(a, (set, frozenset, dict)) and isinstance(b, (set, frozenset, dict)):
            self._charge(_elems(a) + _elems(b))
        elif isinstance(a, (int, float, bool, complex, type(None))) and isinstance(
            b, (int, float, bool, complex, type(None))
        ):
            self._charge(1)
        else:
            raise FuelModelError(
                f"no cost rule for {ta.__name__} {op} {tb.__name__}"
            )
        return _CMP_OP[op](a, b)

    def _contains_cost(self, needle, container) -> int:
        if isinstance(container, (set, frozenset, dict)):
            # hashing the key is proportional to its width
            return _bits(needle) if type(needle) is int else 1
        if isinstance(container, (str, bytes, bytearray)) and isinstance(
            needle, (str, bytes, bytearray)
        ):
            return _elems(container) * _elems(needle)  # naive substring search
        if isinstance(container, (list, tuple, range)):
            return _elems(container) if not isinstance(container, range) else 1
        if _is_array(container):
            return _elems(container)
        raise FuelModelError(
            f"no cost rule for `in` on {type(container).__name__}"
        )

    # -- subscripting -----------------------------------------------------
    def getitem(self, v, k):
        if isinstance(k, slice):
            r = v[k]
            self._charge(_elems(r))
            return r
        if isinstance(v, (list, tuple, str, bytes, bytearray, range)):
            self._charge(1)
            return v[k]
        if isinstance(v, dict):
            self._charge(_bits(k) if type(k) is int else 1)
            return v[k]
        if _is_array(v):
            r = v[k]
            self._charge(_elems(r) if _is_array(r) else 1)
            return r
        raise FuelModelError(f"no cost rule for subscripting {type(v).__name__}")

    def setitem(self, v, k, x):
        if isinstance(k, slice):
            v[k] = x
            self._charge(_elems(x))
            return
        if isinstance(v, (list, bytearray)):
            self._charge(1)
            v[k] = x
            return
        if isinstance(v, dict):
            self._charge(_bits(k) if type(k) is int else 1)
            v[k] = x
            return
        if _is_array(v):
            v[k] = x
            self._charge(_elems(x) if (_is_array(x) or isinstance(x, (list, tuple))) else 1)
            return
        raise FuelModelError(f"no cost rule for item assignment on {type(v).__name__}")

    def augitem(self, v, k, op: str, x):
        cur = self.getitem(v, k)
        self.setitem(v, k, self.binop(op, cur, x))

    # -- f-strings --------------------------------------------------------
    def fmt(self, v):
        """Interpolating an int into a string is a base conversion, which is
        superlinear in its width; charge the schoolbook bound."""
        if type(v) is int:
            self._charge(_bits(v) * _bits(v))
        elif isinstance(v, (str, bytes, bytearray, list, tuple, set, frozenset, dict)):
            self._charge(_elems(v))
        else:
            self._charge(1)
        return v

    # -- calls ------------------------------------------------------------
    def call(self, fn, *args, **kwargs):
        # 1. a function defined inside the instrumented candidate module:
        #    charge the frame, then let its (instrumented) body charge itself.
        g = getattr(fn, "__globals__", None)
        if g is not None and g is self.module_globals:
            self._charge(1)
            return fn(*args, **kwargs)

        # 2. an explicitly modelled builtin
        rule = None
        try:
            rule = COST_TABLE.get(fn)
        except TypeError:
            rule = None
        if rule is not None:
            return rule(self, fn, args, kwargs)

        # 3. an explicitly modelled bound method
        self_obj = getattr(fn, "__self__", None)
        name = getattr(fn, "__name__", None)
        if self_obj is not None and name is not None:
            key = (type(self_obj).__name__, name)
            mrule = METHOD_COST.get(key)
            if mrule is not None:
                return mrule(self, fn, self_obj, args, kwargs)

        # 4. exception classes raised by the candidate
        if isinstance(fn, type) and issubclass(fn, BaseException):
            self._charge(1)
            return fn(*args, **kwargs)

        raise FuelModelError(
            f"no cost rule for call to {getattr(fn, '__qualname__', repr(fn))!s} "
            f"(type {type(fn).__name__}); every callable must be modelled explicitly"
        )


# ---------------------------------------------------------------------------
# Operator dispatch tables (plain Python semantics; the meter charges, these
# just compute)
# ---------------------------------------------------------------------------
import operator as _op  # noqa: E402

_INT_BINOP = {
    "Add": _op.add, "Sub": _op.sub, "Mult": _op.mul, "Div": _op.truediv,
    "FloorDiv": _op.floordiv, "Mod": _op.mod, "Pow": _op.pow,
    "LShift": _op.lshift, "RShift": _op.rshift, "BitAnd": _op.and_,
    "BitOr": _op.or_, "BitXor": _op.xor, "MatMult": _op.matmul,
}
_CMP_OP = {
    "Eq": _op.eq, "NotEq": _op.ne, "Lt": _op.lt, "LtE": _op.le,
    "Gt": _op.gt, "GtE": _op.ge,
}


# ---------------------------------------------------------------------------
# Builtin cost table. Each rule is (meter, fn, args, kwargs) -> result and is
# responsible for charging. DEFAULT DENY: anything absent raises.
# ---------------------------------------------------------------------------

def _c_const(k):
    def rule(m, fn, args, kwargs):
        m._charge(k)
        return fn(*args, **kwargs)
    return rule


def _c_result_len(m, fn, args, kwargs):
    r = fn(*args, **kwargs)
    m._charge(_elems(r))
    return r


def _elem_cost(x) -> int:
    """Cost of touching one element: proportional to its width."""
    if isinstance(x, int):
        return _bits(x)
    if isinstance(x, (str, bytes, bytearray, list, tuple, set, frozenset, dict)):
        return _elems(x)
    if _is_array(x):
        return _elems(x)
    return 1


def _c_reduce(m, fn, args, kwargs):
    """sum/min/max/any/all: charge the total WIDTH of everything folded, so a
    candidate cannot hide bigint additions inside a C-level reduction.

    A lazy iterator argument is denied: its elements cannot be weighed
    without consuming it, and consuming it would change semantics."""
    if len(args) == 1 and isinstance(
        args[0], (list, tuple, set, frozenset, dict, str, bytes, bytearray)
    ):
        m._charge(max(1, sum(_elem_cost(e) for e in args[0])))
    elif len(args) >= 2 or (len(args) == 1 and isinstance(args[0], (int, float))):
        m._charge(max(1, sum(_elem_cost(a) for a in args)))
    else:
        raise FuelModelError(
            f"{getattr(fn, '__name__', fn)}() over an unsized/lazy "
            f"{type(args[0]).__name__ if args else 'nothing'}; not modelled "
            f"(materialise it into a list first)"
        )
    return fn(*args, **kwargs)


def _c_sorted(m, fn, args, kwargs):
    if not args or not isinstance(args[0], (list, tuple, set, frozenset, str, bytes)):
        raise FuelModelError("sorted() over an unsized/lazy iterable; not modelled")
    seq = args[0]
    per = max(1, sum(_elem_cost(e) for e in seq))
    m._charge(per * max(1, len(seq).bit_length()))  # n log n comparisons
    return fn(*args, **kwargs)


def _c_int(m, fn, args, kwargs):
    # int(x) / int(s, base): parsing a string of d digits costs ~d^2
    # (schoolbook base conversion); int(int) is a no-op.
    if args and isinstance(args[0], (str, bytes, bytearray)):
        d = _elems(args[0])
        m._charge(d * d)
    elif args and type(args[0]) is int:
        m._charge(_bits(args[0]))
    else:
        m._charge(1)
    return fn(*args, **kwargs)


def _c_str_of_int(m, fn, args, kwargs):
    # str/repr/bin/oct/hex/format of an int: base conversion.
    if args and type(args[0]) is int:
        b = _bits(args[0])
        m._charge(b * b if fn in (str, repr, format) else b)
    elif args:
        try:
            m._charge(_elems(args[0]))
        except FuelModelError:
            m._charge(1)
    else:
        m._charge(1)
    return fn(*args, **kwargs)


def _c_pow(m, fn, args, kwargs):
    a = args[0] if args else 0
    b = args[1] if len(args) > 1 else 0
    if type(a) is int and type(b) is int:
        r = fn(*args, **kwargs)
        m._charge(_bits(a) * max(1, b if b >= 0 else 1) + _bits(r) if type(r) is int else 1)
        return r
    m._charge(1)
    return fn(*args, **kwargs)


def _c_divmod(m, fn, args, kwargs):
    a, b = args[0], args[1]
    if type(a) is int and type(b) is int:
        m._charge(_bits(a) * _bits(b))
    else:
        m._charge(1)
    return fn(*args, **kwargs)


COST_TABLE = {
    len: _c_const(1),
    range: _c_const(1),          # lazy; iteration is charged by tick()
    abs: _c_str_of_int,
    bool: _c_const(1),
    float: _c_const(1),
    isinstance: _c_const(1),
    int: _c_int,
    str: _c_str_of_int,
    repr: _c_str_of_int,
    bin: _c_str_of_int,
    oct: _c_str_of_int,
    hex: _c_str_of_int,
    format: _c_str_of_int,
    pow: _c_pow,
    divmod: _c_divmod,
    list: _c_result_len,
    tuple: _c_result_len,
    set: _c_result_len,
    frozenset: _c_result_len,
    dict: _c_result_len,
    bytes: _c_result_len,
    bytearray: _c_result_len,
    sorted: _c_sorted,
    sum: _c_reduce,
    min: _c_reduce,
    max: _c_reduce,
    any: _c_reduce,
    all: _c_reduce,
    # lazy builtins: cheap to construct, and every element they yield is
    # charged by tick() when the loop that consumes them runs.
    enumerate: _c_const(1),
    zip: _c_const(1),
    map: _c_const(1),
    filter: _c_const(1),
    reversed: _c_const(1),
    iter: _c_const(1),
    next: _c_const(1),
}

# Explicitly denied: transformer escapes. These would let a candidate run
# uninstrumented code.
for _bad in (eval, exec, compile, __import__, getattr, setattr, delattr,
             globals, locals, vars, dir, open, input, print, id, hash,
             memoryview, object, type, super):
    COST_TABLE.pop(_bad, None)


def _m_const(k):
    def rule(m, fn, obj, args, kwargs):
        m._charge(k)
        return fn(*args, **kwargs)
    return rule


def _m_len_self(m, fn, obj, args, kwargs):
    m._charge(_elems(obj))
    return fn(*args, **kwargs)


def _m_len_arg(m, fn, obj, args, kwargs):
    m._charge(max(1, sum(_elems(a) for a in args)))
    return fn(*args, **kwargs)


def _m_result_len(m, fn, obj, args, kwargs):
    r = fn(*args, **kwargs)
    m._charge(_elems(r) if r is not None else 1)
    return r


def _m_to_bytes(m, fn, obj, args, kwargs):
    m._charge(_bits(obj))
    return fn(*args, **kwargs)


METHOD_COST = {
    # list / bytearray
    ("list", "append"): _m_const(1),
    ("list", "pop"): _m_len_self,      # pop(0) shifts the whole list
    ("list", "insert"): _m_len_self,
    ("list", "extend"): _m_len_arg,
    ("list", "copy"): _m_len_self,
    ("list", "reverse"): _m_len_self,
    ("list", "sort"): _m_len_self,
    ("list", "index"): _m_len_self,
    ("list", "count"): _m_len_self,
    ("list", "remove"): _m_len_self,
    ("list", "clear"): _m_len_self,
    ("bytearray", "append"): _m_const(1),
    ("bytearray", "extend"): _m_len_arg,
    # dict / set
    ("dict", "get"): _m_const(1),
    ("dict", "setdefault"): _m_const(1),
    ("dict", "pop"): _m_const(1),
    ("dict", "keys"): _m_const(1),
    ("dict", "values"): _m_const(1),
    ("dict", "items"): _m_const(1),
    ("dict", "update"): _m_len_arg,
    ("dict", "copy"): _m_len_self,
    ("dict", "clear"): _m_len_self,
    ("set", "add"): _m_const(1),
    ("set", "discard"): _m_const(1),
    ("set", "remove"): _m_const(1),
    ("set", "update"): _m_len_arg,
    ("set", "copy"): _m_len_self,
    ("set", "clear"): _m_len_self,
    # int
    ("int", "bit_length"): _m_const(1),
    ("int", "bit_count"): _m_to_bytes,
    ("int", "to_bytes"): _m_to_bytes,
    ("int", "from_bytes"): _m_len_arg,
    ("int", "conjugate"): _m_const(1),
    # str / bytes
    ("str", "join"): _m_result_len,
    ("str", "split"): _m_len_self,
    ("str", "replace"): _m_len_self,
    ("str", "translate"): _m_len_self,
    ("str", "count"): _m_len_self,
    ("str", "find"): _m_len_self,
    ("str", "index"): _m_len_self,
    ("str", "strip"): _m_len_self,
    ("str", "zfill"): _m_result_len,
    ("str", "format"): _m_result_len,
    ("str", "encode"): _m_len_self,
    ("bytes", "join"): _m_result_len,
    ("bytes", "decode"): _m_len_self,
    ("bytes", "count"): _m_len_self,
    ("bytes", "find"): _m_len_self,
    ("bytes", "translate"): _m_len_self,
}


# ---------------------------------------------------------------------------
# AST instrumentation
# ---------------------------------------------------------------------------

# DEFAULT DENY: only these node types may appear in a candidate.
_ALLOWED_NODES = {
    ast.Module, ast.FunctionDef, ast.Return, ast.Assign, ast.AugAssign,
    ast.AnnAssign, ast.For, ast.While, ast.If, ast.Raise, ast.Assert,
    ast.Expr, ast.Pass, ast.Break, ast.Continue, ast.Delete, ast.Global,
    ast.Nonlocal, ast.Try, ast.ExceptHandler, ast.With, ast.withitem,
    ast.ClassDef, ast.ImportFrom, ast.Import,
    ast.BoolOp, ast.BinOp, ast.UnaryOp, ast.Lambda, ast.IfExp, ast.Dict,
    ast.Set, ast.ListComp, ast.SetComp, ast.DictComp, ast.GeneratorExp,
    ast.Compare, ast.Call, ast.Constant, ast.Attribute, ast.Subscript,
    ast.Starred, ast.Name, ast.List, ast.Tuple, ast.Slice, ast.NamedExpr,
    ast.JoinedStr, ast.FormattedValue, ast.comprehension, ast.arguments,
    ast.arg, ast.keyword, ast.alias, ast.Load, ast.Store, ast.Del,
    ast.And, ast.Or, ast.Add, ast.Sub, ast.Mult, ast.MatMult, ast.Div,
    ast.Mod, ast.Pow, ast.LShift, ast.RShift, ast.BitOr, ast.BitXor,
    ast.BitAnd, ast.FloorDiv, ast.Invert, ast.Not, ast.UAdd, ast.USub,
    ast.Eq, ast.NotEq, ast.Lt, ast.LtE, ast.Gt, ast.GtE, ast.Is,
    ast.IsNot, ast.In, ast.NotIn,
}

# Imports a candidate may make. Deliberately empty apart from the
# no-op __future__ annotations import, so that an evolved candidate cannot
# reach an unmetered C extension. Extending this list requires adding cost
# rules for everything it exposes.
_ALLOWED_IMPORTS = {"__future__"}


def _meter_attr(name: str) -> ast.Attribute:
    return ast.Attribute(
        value=ast.Name(id=METER_NAME, ctx=ast.Load()), attr=name, ctx=ast.Load()
    )


def _meter_call(name: str, args: list, keywords: list | None = None) -> ast.Call:
    return ast.Call(func=_meter_attr(name), args=args, keywords=keywords or [])


def _s(v: str) -> ast.Constant:
    return ast.Constant(value=v)


class _Instrumenter(ast.NodeTransformer):
    def __init__(self):
        self.tmp = 0

    # -- gate ------------------------------------------------------------
    def visit(self, node):
        if type(node) not in _ALLOWED_NODES:
            raise FuelModelError(
                f"unmodelled AST node type {type(node).__name__} at line "
                f"{getattr(node, 'lineno', '?')}; the fuel model denies by default"
            )
        return super().visit(node)

    # -- imports ---------------------------------------------------------
    def visit_Import(self, node):
        for a in node.names:
            root = a.name.split(".")[0]
            if root not in _ALLOWED_IMPORTS:
                raise FuelModelError(f"import of unmodelled module {a.name!r}")
        return node

    def visit_ImportFrom(self, node):
        root = (node.module or "").split(".")[0]
        if root not in _ALLOWED_IMPORTS:
            raise FuelModelError(f"import from unmodelled module {node.module!r}")
        return node

    # -- expressions ------------------------------------------------------
    def visit_BinOp(self, node):
        self.generic_visit(node)
        return _meter_call("binop", [_s(type(node.op).__name__), node.left, node.right])

    def visit_UnaryOp(self, node):
        self.generic_visit(node)
        return _meter_call("unop", [_s(type(node.op).__name__), node.operand])

    def visit_Compare(self, node):
        self.generic_visit(node)
        if len(node.ops) == 1:
            return _meter_call(
                "cmp", [_s(type(node.ops[0]).__name__), node.left, node.comparators[0]]
            )
        # Chained comparison a OP1 b OP2 c ... -> conjunction of pairwise
        # metered comparisons, with each comparator bound once by a walrus so
        # short-circuiting and single-evaluation semantics are preserved.
        parts = []
        left = node.left
        for i, (op, comp) in enumerate(zip(node.ops, node.comparators)):
            if i < len(node.ops) - 1:
                self.tmp += 1
                tname = f"__fuel_t{self.tmp}__"
                bound = ast.NamedExpr(target=ast.Name(id=tname, ctx=ast.Store()), value=comp)
                parts.append(_meter_call("cmp", [_s(type(op).__name__), left, bound]))
                left = ast.Name(id=tname, ctx=ast.Load())
            else:
                parts.append(_meter_call("cmp", [_s(type(op).__name__), left, comp]))
        return ast.BoolOp(op=ast.And(), values=parts)

    def visit_Subscript(self, node):
        self.generic_visit(node)
        if isinstance(node.ctx, ast.Load):
            return _meter_call("getitem", [node.value, self._key(node.slice)])
        return node  # Store/Del handled by the enclosing statement

    def _key(self, sl):
        if isinstance(sl, ast.Slice):
            return ast.Call(
                func=ast.Name(id="slice", ctx=ast.Load()),
                args=[
                    sl.lower or ast.Constant(value=None),
                    sl.upper or ast.Constant(value=None),
                    sl.step or ast.Constant(value=None),
                ],
                keywords=[],
            )
        return sl

    def visit_Call(self, node):
        self.generic_visit(node)
        return _meter_call("call", [node.func] + node.args, node.keywords)

    def visit_FormattedValue(self, node):
        self.generic_visit(node)
        node.value = _meter_call("fmt", [node.value])
        return node

    # -- statements -------------------------------------------------------
    def visit_Assign(self, node):
        self.generic_visit(node)
        subs = [t for t in node.targets if isinstance(t, ast.Subscript)]
        if not subs:
            return node
        if len(node.targets) != 1:
            raise FuelModelError("chained assignment with a subscript target")
        t = node.targets[0]
        return ast.Expr(
            value=_meter_call("setitem", [t.value, self._key(t.slice), node.value])
        )

    def visit_AugAssign(self, node):
        self.generic_visit(node)
        opname = _s(type(node.op).__name__)
        t = node.target
        if isinstance(t, ast.Name):
            return ast.Assign(
                targets=[t],
                value=_meter_call(
                    "binop", [opname, ast.Name(id=t.id, ctx=ast.Load()), node.value]
                ),
            )
        if isinstance(t, ast.Subscript):
            return ast.Expr(
                value=_meter_call(
                    "augitem", [t.value, self._key(t.slice), opname, node.value]
                )
            )
        if isinstance(t, ast.Attribute) and isinstance(t.value, ast.Name):
            return ast.Assign(
                targets=[t],
                value=_meter_call(
                    "binop",
                    [
                        opname,
                        ast.Attribute(
                            value=ast.Name(id=t.value.id, ctx=ast.Load()),
                            attr=t.attr,
                            ctx=ast.Load(),
                        ),
                        node.value,
                    ],
                ),
            )
        raise FuelModelError("unmodelled augmented-assignment target")

    def visit_Delete(self, node):
        self.generic_visit(node)
        for t in node.targets:
            if not isinstance(t, ast.Name):
                raise FuelModelError(
                    "`del` on a subscript/attribute target is not modelled "
                    "(del lst[0] is O(len), del d[k] is O(1); rather than guess, "
                    "this is denied)"
                )
        return node

    def visit_For(self, node):
        self.generic_visit(node)
        node.iter = _meter_call("tick", [node.iter])
        return node

    def visit_While(self, node):
        self.generic_visit(node)
        node.test = _meter_call("tick1", [node.test])
        return node

    def visit_comprehension(self, node):
        self.generic_visit(node)
        node.iter = _meter_call("tick", [node.iter])
        return node


def instrument_source(source: str, filename: str = "<candidate>"):
    """Return a code object for `source` with fuel accounting woven in.

    Raises FuelModelError for any construct with no explicit cost rule.
    """
    tree = ast.parse(source, filename=filename)
    tree = _Instrumenter().visit(tree)
    ast.fix_missing_locations(tree)
    return compile(tree, filename, "exec")


def load_instrumented(path, limit: int | None = None):
    """Exec a candidate file under a fresh meter. Returns (module, meter).

    A FRESH module object every call: a candidate that memoised results
    across calls would otherwise make later (larger) n artificially cheap
    and manufacture a sub-quadratic slope.
    """
    source = open(path).read()
    code = instrument_source(source, str(path))
    meter = FuelMeter(limit=limit)
    module = types.ModuleType("fuel_candidate")
    module.__dict__[METER_NAME] = meter
    module.__dict__["__file__"] = str(path)
    meter.module_globals = module.__dict__
    exec(code, module.__dict__)
    return module, meter


def load_plain(path):
    """Exec a candidate file with NO instrumentation, fresh module.

    Used for the correctness gates (~50x cheaper than the instrumented
    build) and for the differential test that instrumentation preserves
    semantics.
    """
    spec = importlib.util.spec_from_file_location("plain_candidate", str(path))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def measure_fuel(path, n: int, limit: int | None = None) -> tuple[int, int, int]:
    """Return (call_fuel, value, setup_fuel) for a fresh evaluation of
    center_cell(n).

    `setup_fuel` is the work done at MODULE level, before center_cell is
    called, and it is reported separately rather than folded into the total.
    Both halves matter and they must not be mixed:

      * Folding setup into the total would make the fuel count of an
        algorithmically identical program depend on incidental module-level
        code (`initial_program.py` has an `if __name__ == "__main__"` block,
        `candidate_a_correct.py` does not), which would break the exact
        baseline-equals-baseline identity that is this instrument's sharpest
        calibration check.
      * Discarding setup silently would leave a hiding place: because a
        fresh module is exec'd per n, a candidate could precompute a table
        at import time and report a near-constant call fuel. Setup fuel is
        therefore surfaced in the evaluator's metrics, where a nonzero value
        on a candidate that should have none is visible.
    """
    module, meter = load_instrumented(path, limit=limit)
    setup = meter.fuel
    value = module.center_cell(n)
    return meter.fuel - setup, value, setup
