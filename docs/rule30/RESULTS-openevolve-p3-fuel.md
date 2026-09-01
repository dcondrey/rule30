# A deterministic fuel counter for the OpenEvolve P3 harness — instrument built, sanity gate passed

Date: 2026-08-31. Companion to `RESULTS-openevolve-p3.md`, which records why
the wall-clock instrument was rejected. Harness:
`experiments/openevolve-p3/`.

**Scope.** This is instrument work only. Nothing here is a claim about Rule
30, no search was launched, and no LLM call was made. `evaluator.py`,
`PREREGISTRATION.md` and `baseline_exponent.json` are untouched; `PATH.md`
is untouched. The new instrument is a *parallel* evaluator
(`evaluator_fuel.py`) that imports the pre-registered scoring function,
correctness gates, trap set and literal scan rather than re-stating them, so
no threshold can drift.

**Headline.** Under the wall clock, the naive `O(n^2)` control — the same
program the stored baseline was measured from — scored 0.2667, 0.2957 and
**0.7896** against its own baseline across three runs, i.e. the evaluator
credited the baseline with beating itself by 0.41 exponent-units. Under the
fuel counter it scores **0.2000**, with a tail exponent of
`1.999459168018799` against a stored baseline of `1.999459168018799` —
**equal in every printed digit, improvement exactly 0.000000**.

---

## 1. Arm 3's instrument was read and NOT reused

Register row 12 (`RESULTS-arm3-run1.md`) metered `fuel_consumed` from
**wasmtime**, driven by the Rust `crosstalk-lab` binary over sealed
tournaments of `.wasm` modules (`experiments/rule30/naive.wasm`,
`bitparallel.wasm`, `constant.wasm`). It is a sound instrument and it
recovered the known exponent to three decimals.

It cannot port here, for a reason worth stating precisely because it is the
same reason the cost model below has to exist:

> WebAssembly has only fixed-width `i32`/`i64` operations. Every wasmtime
> instruction genuinely is `O(1)` work, so metering one unit per instruction
> is already correct and **no proportional cost model is needed**. OpenEvolve
> mutates **Python**, where a single opcode — `row << 1` on a `(2n+3)`-bit
> integer — performs `n` bits of work.

Reusing Arm 3 would mean compiling every LLM-proposed Python candidate to
WASM, which is neither what OpenEvolve emits nor something the harness can
verify. So: **new instrument, same principle.** The validation *pattern* is
reused directly — recover a known exponent on controls before believing
anything, exactly as row 12 did.

## 2. The cost model

`experiments/openevolve-p3/fuel.py`. The candidate's source is rewritten at
the AST level so every cost-bearing construct routes through a `FuelMeter`
method:

```
a + b            ->  __fuel__.binop('Add', a, b)
-a               ->  __fuel__.unop('USub', a)
a < b            ->  __fuel__.cmp('Lt', a, b)
v[k]             ->  __fuel__.getitem(v, k)
v[k] = x         ->  __fuel__.setitem(v, k, x)
v[k] += x        ->  __fuel__.augitem(v, k, 'Add', x)
f(x)             ->  __fuel__.call(f, x)
for t in it:     ->  for t in __fuel__.tick(it):        (1 per iteration)
while c:         ->  while __fuel__.tick1(c):           (1 per iteration)
[e for x in it]  ->  [e for x in __fuel__.tick(it)]     (1 per iteration)
f"{v}"           ->  f"{__fuel__.fmt(v)}"
```

### 2.1 The unit: a word-RAM model, `WORD_BITS = 30`

An operation on a value fitting in one machine word costs **1**; an
operation on a `k`-word big integer costs **`k`**. The word is 30 bits,
which is CPython's actual bignum digit size (`PyLong` stores base-2^30
digits and its bitwise/additive routines are linear in digit count), so the
model's unit is the unit the interpreter really operates on.

This choice is load-bearing and was found empirically. Charging by raw
**bit** length instead puts a spurious `log n` factor on every loop-index
operation (`i - 1`, `i + 1 < width`), and the naive `O(n^2)` simulation then
fits **2.151 / 2.140 / 2.129 / 2.119** across its windows — an instrument
that cannot recover a known exponent is not an instrument. Under the word
model the same program fits 1.9957 -> 1.9995. Index arithmetic is `O(1)` as
it is on real hardware, while a bitwise op on a `(2n+3)`-bit packed row
still costs `~n/30`, i.e. still proportional to `n`. Section 5 shows the
verdict is invariant to the word size.

**The other direction, measured 2026-08-31.** The bit ablation above shows only
that charging *too finely* breaks the fit. The obvious alternative in the
opposite direction — a **flat opcode counter** charging `1` per operation
regardless of operand width, which is what `sys.settrace`, `cProfile` and a WASM
fuel meter each give for free — was rejected in section 1 by argument, and
rejecting the strong incumbent by argument is not rejecting it. It has now been
run, pre-registered, in `experiments/openevolve-p3/PREREG-flat-opcode-ablation.md`:

| candidate | true | word model | flat opcode |
|---|---|---|---|
| (a) `candidate_a_correct` | 2 | 1.99946 | 1.99947 |
| (c) `candidate_c_bitpacked` | 2 | 1.99410 | **0.99938** |
| (e) `candidate_e_cubic` | 3 | **2.97449** | **1.99690** |

The flat counter is wrong by a full exponent-unit on both candidates that put a
wide operand in front of it. Candidate (a) agrees to five decimals and is
**non-discriminating by construction** — it iterates per cell, so every operand
already fits one word and the two models charge the identical thing. It is not
evidence for the flat counter.

Candidate (e) is new and exists because every test of this instrument before it,
including the bit ablation above, checked it against a true exponent of **2 and
only 2**; an instrument biased toward 2 would have passed all of them. It is
correct (identical to (a) and (c) for all `n < 120`) and deliberately
`Theta(n^3)`. The word model reads it 2.97449 with adjacent slopes rising
2.90164 -> 2.96786 -> 2.97449, converging toward 3 from below as the exact cost's
lower-order quadratic term predicts.

So granularity is the controlling variable, shown in both directions: too coarse
loses a full exponent-unit, too fine adds a spurious `log n` worth 0.12-0.15,
and the word model recovers two distinct known exponents to within 0.03.

### 2.2 Charging rules, in full

`_bits(x)` below means **words**: `ceil(bit_length / 30)`, minimum 1.
`_elems(x)` means element count (`len`, or `.size` for array-likes).

| construct | charge | rationale |
|---|---|---|
| `for`/comprehension iteration | 1 per element yielded | loops are one of the three channels unbounded work can flow through |
| `while` test | 1 per evaluation | ditto |
| call to a function defined in the candidate | 1 (its body meters itself) | frame cost; the body is instrumented |
| **int** `+ - & \| ^ << >>` | `max(_bits(a), _bits(b), _bits(result))` | linear in the widest operand **or result** — the result term is what catches `mask = (1 << width) - 1`, where both inputs are one word and the result is `n/30` words |
| **int** `* / // % **` | `_bits(a) * _bits(b) + _bits(result)` | schoolbook bound; see 2.3 |
| **int** unary `- + ~` | `max(_bits(a), _bits(result))` | linear |
| **int** comparisons | `max(_bits(a), _bits(b))` | linear |
| `not` | 1 | truthiness |
| sequence `*` (`[0] * width`) | `_elems(result)` | allocation is linear |
| sequence `+` (concat) | `_elems(result)` | linear |
| set/dict `\| & - ^` | `_elems(a) + _elems(b) + _elems(result)` | linear in both sides |
| `str`/`bytes` `%` | `_elems(a) + _elems(result)` | linear |
| float/complex arithmetic | 1 | fixed width |
| array-like (`.size` + `.shape`, i.e. numpy) any binop/unop/compare | `_elems(a) + _elems(b) [+ _elems(result)]` | a vectorised op is **not** one unit; this is the numpy analogue of the bigint hazard |

Note on the array-like row, because it can read as a contradiction against
section 2.4: the briefed numpy hazard is closed **twice, by two different
mechanisms**, and today only the second one fires. `import numpy` is refused
outright by the import allowlist (2.4, gate 3), so no candidate can currently
reach an array at all. The proportional charge above is the fallback that
becomes load-bearing only if the allowlist is ever widened, plus it covers an
array arriving by some other route. Denial is the live defence; proportional
charging is the standing one.
| `v[i]` on list/tuple/str/bytes/range | 1 | O(1) index |
| `v[a:b]` (slice, load or store) | `_elems(result)` / `_elems(value)` | copies |
| `v[k]` on dict | `_bits(k)` for int keys, else 1 | hashing is proportional to key width |
| `v[k]` on an array-like | `_elems(result)` if the result is an array, else 1 | fancy indexing is not O(1) |
| `x in container` — set/dict | `_bits(x)` for int, else 1 | hash cost |
| `x in container` — list/tuple | `_elems(container)` | linear scan |
| `x in container` — str/bytes | `_elems(container) * _elems(x)` | naive substring search |
| `x in range(...)` | 1 | arithmetic membership |
| `len`, `range`, `bool`, `float`, `isinstance` | 1 | O(1) / lazy |
| `int(s)` from a `d`-char string | `d^2` | schoolbook base conversion |
| `int(x)` from an int | `_bits(x)` | copy |
| `str`/`repr`/`format` of an int | `_bits(x)^2` | base conversion is superlinear |
| `bin`/`oct`/`hex`/`abs` of an int | `_bits(x)` | power-of-two bases are linear |
| f-string interpolation of an int | `_bits(v)^2` | same conversion |
| `pow(a, b)` | `_bits(a) * b + _bits(result)` | repeated squaring bound |
| `divmod(a, b)` | `_bits(a) * _bits(b)` | as division |
| `list`/`tuple`/`set`/`dict`/`frozenset`/`bytes`/`bytearray(...)` | `_elems(result)` | materialisation is linear |
| `sum`/`min`/`max`/`any`/`all` over a sized container | `sum of element widths` | **a C-level reduction over bigints must not cost `len`** |
| `sum`/`min`/`max`/`any`/`all` over a lazy iterator | **denied** | elements cannot be weighed without consuming them |
| `sorted(seq)` | `sum of element widths * ceil(log2 len)` | `n log n` comparisons, each proportional to element width |
| `enumerate`/`zip`/`map`/`filter`/`reversed`/`iter`/`next` | 1 | lazy; every element they yield is charged by `tick` in the loop that consumes them |
| `list.append`, `dict.get/setdefault/pop`, `set.add/discard/remove`, `int.bit_length` | 1 | O(1) |
| `list.pop/insert/copy/reverse/sort/index/count/remove/clear` | `_elems(self)` | linear |
| `list.extend`, `dict.update`, `set.update`, `bytearray.extend` | `_elems(arg)` | linear in what is added |
| `int.to_bytes`, `int.bit_count` | `_bits(self)` | linear in width |
| `int.from_bytes` | `_elems(arg)` | linear |
| `str/bytes.join` | `_elems(result)` | linear |
| `str/bytes .split/.replace/.translate/.count/.find/.index/.strip/.encode/.decode` | `_elems(self)` | linear scans |
| `str.zfill/.format` | `_elems(result)` | linear |
| straight-line code between the above | 0 | `O(1)`; cannot carry `n`-dependent work |

### 2.3 What is deliberately **over**-charged

Big-integer `*`, `/`, `//`, `%` are charged `_bits(a) * _bits(b)`, the
schoolbook bound. CPython switches to Karatsuba above ~2100 bits, so for
very large operands this over-charges by roughly `max_words^0.415`. That is
conservative **against** a multiplication-based candidate: it can only make
such a candidate look worse, never better, which is the safe direction for a
gate whose job is to refuse false positives.

**Re-derivation trigger, stated so it is not forgotten:** if a search ever
produces a winner whose fuel is dominated by big-integer multiplication,
this rule must be replaced with a Karatsuba/FFT-aware one *before* the
result is believed. None of the four sanity candidates, the seed program, or
either reference implementation multiplies, so the rule is inert today.

### 2.4 Default deny — the part that makes it auditable

The table above is exhaustive because everything outside it is a hard
failure, not a silent charge of 1. Three separate gates:

1. **AST node types.** An explicit whitelist. Anything else raises
   `FuelModelError` naming the node type and line. `async def`, `await`,
   `yield`, `match` and `del v[k]` are all denied this way. (`del lst[0]` is
   `O(len)` and `del d[k]` is `O(1)`; rather than guess, it is refused.)
2. **Callables.** A callable is chargeable only if it is (i) a function
   defined inside the instrumented candidate module, (ii) in `COST_TABLE`
   / `METHOD_COST` above, or (iii) an exception class. Anything else raises,
   naming it. This is what makes `numpy.convolve` impossible to sneak
   through: an unmodelled vectorised call is rejected, not charged 1.
   `eval`, `exec`, `compile`, `__import__`, `getattr`, `setattr`,
   `globals`, `locals`, `vars` are absent from the table by construction —
   these are transformer *escapes* (they would run uninstrumented code), a
   different hole from undercharging, and they are closed by the same
   default-deny.
3. **Imports.** An allowlist containing only `__future__`. A candidate
   cannot reach an unmetered C extension at all. Extending this list
   requires adding cost rules for everything the module exposes.

### 2.5 Soundness argument

Any Python program's unbounded work must flow through exactly one of three
channels: a loop, a (possibly recursive) call, or a single primitive
operation on a variable-width value. Loops are charged per iteration by
`tick`/`tick1`; calls are charged per invocation and the callee is either
instrumented, tabulated, or denied; primitives are charged by operand and
result size. Straight-line code between them is `O(1)` and cannot carry
`n`-dependent work. Therefore no `n`-dependent work is uncharged.

### 2.6 Setup fuel is reported, never folded in and never discarded

A fresh module is exec'd for every `n` — a candidate that memoised across
calls would otherwise make later, larger `n` artificially cheap and
manufacture a sub-quadratic slope. That re-import creates a second hazard:
work done at *module level* would be repeated per point but is not part of
`center_cell`. `measure_fuel` therefore returns call fuel and setup fuel
**separately**, and the evaluator surfaces `max_setup_fuel` in its metrics
and `setup_fuel_per_point` in its artifacts.

Both halves matter, and the lookup-table cheat shows why (at `n = 137`):

| program | call fuel | setup fuel |
|---|---|---|
| `initial_program.py` (seed) | 531,299 | 8 |
| `candidate_a_correct.py` | 531,299 | 0 |
| `candidate_c_bitpacked.py` | 6,974 | 0 |
| `candidate_d_lookup_table.py` | **2** | **31,999** |

Folding setup in would break the exact baseline identity (the seed's 8 units
are its `if __name__ == "__main__"` block; candidate (a) has no such block,
and the two are algorithmically identical). Discarding setup would leave
candidate (d)'s 31,999 units of table construction invisible behind a call
cost of 2.

Candidate (d)'s row is re-measured across the full scoring ladder in
`setup_fuel_d_20260831.log`: setup fuel is **31,999 at every one of
`n` = 250, 500, 1000, 2000, 4000**, flat because the table is built once at
module level, against a call fuel of 2 (1 at `n=4000`). A constant setup
cost independent of `n`, next to a call cost that does not grow, is the
signature `max_setup_fuel` exists to expose.

### 2.7 Other structural consequences of determinism

* `repeats` is **1**. Repeating an exact measurement adds nothing.
* The per-point wall-clock timeout is replaced by a **fuel budget**
  (`2e9`). A point is dropped for exceeding a budget that is a property of
  the candidate, not of the machine — so the window-truncation failure that
  wrecked the wall-clock gate (the naive control losing `n = 16000` to a
  180s timeout while the 50x-faster bit-packed control kept it, leaving the
  two scored over different `n`-windows) **cannot occur**.
* Correctness gates run on the **uninstrumented** module, ~50x cheaper.
  Only the scaling measurement is instrumented, and a differential test
  (`check_instrumentation`, run inside `evaluate()`) asserts the
  instrumented build returns exactly what the uninstrumented one returns at
  `n` in `{0,1,2,3,7,20,61,137,250}`. A transformer bug that changed
  semantics would otherwise be invisible.

## 3. Baseline exponent — ground-truth check on the instrument

`baseline_fuel.json`, measured from `initial_program.py`, profile
`fuel_wide` (`n` in 250, 500, 1000, 2000, 4000):

| n | fuel |
|---|---|
| 250 | 1,760,513 |
| 500 | 7,021,013 |
| 1000 | 28,042,013 |
| 2000 | 112,084,013 |
| 4000 | 448,168,013 |

Global log-log fit **1.99806**, `r^2 = 0.9999998600615513`, tail exponent
**1.999459168018799**, tail-consistency 0.00054.

The wall clock gave 2.2147 for this same program, and 1.9289 / 2.1635 /
1.8069 on re-measurement. The known answer is 2.0.

### 3.1 Every adjacent window, not just the tail

The wall-clock instrument needed `n` up to 16000 to escape a transient in
which the bit-packed control read `~1.1`. That transient was **Python
interpreter overhead**, which fuel does not charge at all, so it should be
absent here — and the way to show that is to sweep every window rather than
assert it:

| window | (a) naive `O(n^2)` | (c) bit-packed | gap |
|---|---|---|---|
| 250 -> 500 | 1.995683 | 1.970835 | 0.024848 |
| 500 -> 1000 | 1.997839 | 1.976652 | 0.021187 |
| 1000 -> 2000 | 1.998919 | 1.992552 | 0.006367 |
| 2000 -> 4000 | **1.999459** | **1.994105** | **0.005354** |

Both controls are already within 0.03 of 2.0 in the *smallest* window and
both climb monotonically toward it. There is no transient regime to escape.
That is what licenses a 4000-point ladder where the wall clock needed 16000,
and it is a consequence of the instrument, not a compromise.

## 4. The sanity gate under the fuel instrument

`RULE30_P3_FUEL_PROFILE=fuel_wide run_sanity_tests_fuel.py`, 2026-08-31
12:40-12:45 PDT, load average 38.08 on 10 cores. Raw log:
`experiments/openevolve-p3/fuel_gate_20260831.log`.

| candidate | required | `combined_score` | tail exponent | `r2` | verdict |
|---|---|---|---|---|---|
| (a) correct naive | correct, flat ~0.2, no exponent win | **0.200000** | 1.999459168018799 | 0.99999986 | **PASS** |
| (b) deliberately wrong | exactly 0.0 | **0.0** (`evolve` gate, n=15: got 0, expected 1) | — | — | **PASS** |
| (c) bit-packed, constant-factor | correct, **NOT** an exponent win | **0.214234** | 1.994104692887 | 0.99999266 | **PASS** |
| (d) lookup-table cheat | exactly 0.0 | **0.0** (`evolve` gate, n=157: got 1, expected 0) | — | — | **PASS** |

Compare the wall-clock run of the same four candidates on the same machine
four hours earlier: (a) **0.2957 FAIL**, (c) **0.9335 FAIL**.

**(a) is the sharpest calibration check available and it is exact.**
Candidate (a) is algorithmically identical to the program the baseline was
measured from, so its fuel must equal the stored baseline digit for digit.
It does: tail `1.999459168018799` against baseline `1.999459168018799`,
`improvement = 0.000000`, score `0.200000` — the flat correctness credit and
nothing above it. The wall-clock instrument credited this same program with
beating itself by **0.41 exponent-units** (score 0.7896).

**(c) is the whole ballgame, and it lands where the pre-registration says it
should.** Its fuel at `n = 4000` is 5,349,874 against the naive control's
448,168,013 — an 84x constant-factor win, which is real and is exactly what
big-integer bit-packing buys. Its *exponent* is 1.9941 against 1.9995:
`improvement = 0.005354`, `bonus = 0.01785`, `confidence = 0.99689`,
`score = 0.2 + 0.8 * 0.01785 * 0.99689 = 0.21423`. The pre-registration
documents 0.210 as the correct score for this candidate; 0.214 is that
number. **The 84x speedup is invisible to `combined_score`, which is the
entire design intent.**

The pre-registered full-credit bar is 0.3 exponent-units of improvement.
(c)'s 0.0054 is **56x below it**, and the noise band the kill condition
quotes (`+/-0.2-0.3`) is now 37-56x wider than the instrument's largest
observed discrepancy rather than *smaller* than its scatter, which is what
blocked the wall-clock run.

## 5. Invariance to the word size

`WORD_BITS = 30` is justified by CPython's bignum representation, not by the
number it produces. To show the verdict does not depend on it, the same two
controls under `WORD_BITS = 64`:

`experiments/openevolve-p3/wordsize_sweep_fuel.py`, logged to
`wordsize_sweep_20260831.log`. `WORD_BITS` is a plain module constant, so the
script rebinds it and re-measures; both sizes now run `n` = 125..4000. Note
this is a **wider diagnostic sweep than the scoring ladder**, which is
`n` = 250..4000 (`baseline_fuel.json`, `scaling_ns_config`). The extra
`125 -> 250` row below is there to show the constant-factor candidate's
approach from below and takes no part in any `combined_score`.

| window | (a) @ 64 | (c) @ 64 | (a) @ 30 | (c) @ 30 |
|---|---|---|---|---|
| 125 -> 250 | 1.99139 | 1.89091 | 1.99139 | 1.90938 |
| 250 -> 500 | 1.99568 | 1.94293 | 1.99568 | 1.97084 |
| 500 -> 1000 | 1.99784 | 1.97079 | 1.99784 | 1.97665 |
| 1000 -> 2000 | 1.99892 | 1.97640 | 1.99892 | 1.99255 |
| 2000 -> 4000 | 1.99946 | 1.99260 | 1.99946 | 1.99410 |

Candidate (a)'s counts are **identical** at both word sizes — not merely
close, the same integers `[442763, 1760513, 7021013, 28042013, 112084013,
448168013]` — because no integer in a plain list-based simulation ever
exceeds 30 bits, so the word size cannot touch it. Only (c) moves, and only
in the constant: its gap below (a) is 0.02252 at 64-bit and 0.00637 at
30-bit in the `1000 -> 2000` window, narrowing to 0.00686 and 0.00535 in the
`2000 -> 4000` window. All four are far inside the flat-credit band —
0.02252, the widest, scores 0.26 against a 0.3-exponent-unit full-credit
bar. The verdict — **(c) is a constant-factor win, not an exponent win** —
holds at both word sizes. The word size changes the constant, not the
conclusion.

## 6. Determinism check

`experiments/openevolve-p3/determinism_check_fuel.py`, logged to
`determinism_fuel_20260831.log`.

**Three** candidates are checked, not the four of section 4:
`candidate_a_correct.py`, `candidate_c_bitpacked.py`, and the seed
`initial_program.py`. (b) and (d) are excluded because they fail correctness
and so never produce a fuel ladder to compare; there is nothing for a
determinism check to bite on. The seed is included in their place, which
also covers the file the stored baseline was measured from.

Each of the three is measured in **three separate processes**,
`PYTHONHASHSEED` left at its default (randomised per process), while the
machine carried other jobs. Separate processes matter: same-process repeats
cannot fail on hash-seed-dependent iteration order or on module-level cache
state, so they would not test what needs testing.

Nine worker processes in total, run 13:07-13:38 while the machine carried
other jobs, load average **20.3 to 34.8** over the window (`uptime` logged on
both sides of the run). Result: **ALL BIT-IDENTICAL**.

| candidate | n=250 | n=500 | n=1000 | n=2000 | n=4000 | distinct values across the 3 processes |
|---|---|---|---|---|---|---|
| (a) `candidate_a_correct.py` | 1,760,513 | 7,021,013 | 28,042,013 | 112,084,013 | 448,168,013 | 1 at every `n` |
| (c) `candidate_c_bitpacked.py` | 21,874 | 85,745 | 337,474 | 1,342,945 | 5,349,874 | 1 at every `n` |
| seed `initial_program.py` | 1,760,513 | 7,021,013 | 28,042,013 | 112,084,013 | 448,168,013 | 1 at every `n` |

(a) and the seed agree exactly, which is the expected result rather than a
coincidence: (a) *is* the program the stored baseline was measured from. The
(a)/(c) ratio at `n=4000` is 448,168,013 / 5,349,874 = **83.8x**, which is
the constant-factor win section 4 reports `combined_score` correctly
declining to credit as an exponent improvement.

Two further cross-process data came free, from processes that were not part
of this check at all. The `measure_baseline_fuel.py` run of
`initial_program.py` (13:40 the previous run, stored in `baseline_fuel.json`)
and the `wordsize_sweep_fuel.py` run of `candidate_a_correct.py` (13:15-13:28)
both produced `[1760513, 7021013, 28042013, 112084013, 448168013]` — different
files, different scripts, different processes, hours apart under different
load, identical in every digit.

Contrast the wall clock, where the *same* program measured 1.9289, 2.1635
and 1.8069 (spread 0.357) and the paired gap against (c) read 0.590 in one
pair and 0.034 in the next nine minutes later.

## 7. Test pins

`experiments/openevolve-p3/test_fuel.py`, 71 tests, all passing. The ones
that earn their place:

* `test_bigint_ops_are_charged_by_width` and
  `test_bigint_charge_scales_linearly_with_width` — **if these regress, a
  bit-packed constant-factor candidate reads as an algorithmic
  breakthrough.** They assert a shift/xor on a 100,000-bit integer costs
  more than `100000/WORD_BITS`, and that doubling the width doubles the
  charge.
* `test_small_int_arithmetic_is_word_cost_not_bit_cost` — pins the word-RAM
  unit, i.e. the fix for the spurious `log n` factor of section 2.1.
* `test_unmodelled_constructs_are_denied` — `import numpy`, `from os import
  path`, `eval(...)`, `async def`, `yield` all rejected.
* `test_instrumentation_preserves_semantics` — differential test across six
  programs (four sanity candidates, the seed, and `simple_reference.py`) at
  nine values of `n`.
* `test_module_level_work_is_reported_as_setup_not_folded_into_the_call` —
  pins section 2.6.

## 8. Verdict, including what is NOT closed

**The instrument is trustworthy as a measurement of asymptotic cost.** It
recovers the known `O(n^2)` exponent to 1.9995 with `r^2 = 0.9999999`,
scores the baseline against itself at exactly 0.200000 with improvement
0.000000, holds the constant-factor control to 0.214 against a documented
0.210, is bit-identical across processes under load, and its cost model
denies by default rather than undercharging by omission.

**One gap must be closed before a real search, and it is not a measurement
problem.** The fuel ladder tops out at `n = 4000`; the wall-clock profile
reached 16000. The scaling-range correctness check is the harness's principal
defence against a precomputed lookup table (`PREREGISTRATION.md` gate 4 says
so explicitly: "this is the only check that reaches beyond n=3000"), and a
4000-point ladder shortens its reach by 4x. A table covering `n <= 4000`
would pass evolve, holdout and trap (all `n <= 3000`) *and* every scaling
point, and would read a slope near 0. The `_scan_literals` backstop does not
catch a dict *comprehension*, as the pre-registration itself notes.

Two candidate fixes, deliberately **not** implemented here because the brief
says stop after validation, and because either one is a pre-registration
question rather than an instrument question:

1. Add a scaling point far above any plausible embedded table (the fuel
   cost of one extra point is predictable in advance from the fit, unlike
   wall clock).
2. Treat a near-zero slope, or a large `setup_fuel`, as suspicious in its
   own right — `max_setup_fuel` is already reported for exactly this, and
   candidate (d) shows it reads 31,999 against 0 for every honest candidate.

Until one of those is in place, this instrument measures scaling correctly
but the *anti-table* gate is weaker than the pre-registered one. That is the
open decision, and it is the user's.

## 9. Register row (merged into `PATH.md` section 7.1 on 2026-08-31)

Numbered **92**, not 78.  Corrected 2026-08-31 on merge: 78 was already taken by
FINDINGS row 78 ("P2 nontrivial density bounds").  See the numbering note in
`RESULTS-openevolve-p3.md` section 7 for why the register's canonical stream is
the one in `experiments/overnight-arms/frontier_attack/FINDINGS.md` section 3.

| # | Approach | Prize | Status | Why it stopped | Where |
|---|---|---|---|---|---|
| 92 | Deterministic fuel counter replacing the wall clock in the OpenEvolve P3 evaluator (the instrument row 91 was blocked on) | 3 | **INSTRUMENT VALIDATED, search not run** | Arm 3's wasmtime fuel meter (row 12) was read and rejected for reuse: WASM has only fixed-width ops so one instruction is genuinely `O(1)`, whereas OpenEvolve mutates Python where `row << 1` on a `(2n+3)`-bit int is one opcode doing `n` bits of work. Built a new AST-rewriting word-RAM counter (`fuel.py`, `WORD_BITS = 30` = CPython's bignum digit) that charges every variable-width operation proportionally and **denies by default** — unmodelled AST node, callable or import is a hard failure, not a silent charge of 1. Charging by raw bits instead of words was measured to inflate the naive control to 2.12-2.15 via a spurious `log n` on loop indices; the word model recovers **1.99946** with `r^2 = 0.9999999`. All four pre-registered sanity candidates pass under the new instrument, against two failures under the wall clock: (a) **0.200000** with tail equal to the stored baseline **in every printed digit**, improvement exactly 0.0 (the wall clock credited this same program with beating itself by 0.41 exponent-units, score 0.7896); (b) 0.0; (c) bit-packed **0.214234**, tail 1.9941 vs baseline 1.9995 — an 84x constant-factor win rendered invisible to `combined_score`, against 0.9335 under the wall clock; (d) 0.0. Bit-identical across three separate processes for each of three candidates -- (a), (c) and the seed `initial_program.py`; (b) and (d) fail correctness and so never produce a fuel ladder to compare -- under load average 20.3-34.8 on 10 cores (`determinism_fuel_20260831.log`). `evaluator.py`, `PREREGISTRATION.md` and `baseline_exponent.json` untouched — this is a parallel evaluator that imports the pre-registered scoring, gates and thresholds rather than restating them. Not a claim about Rule 30; no search launched, no LLM call. Open before a search: the 4000-point ladder shortens the pre-registration's only above-n=3000 anti-lookup-table check by 4x. | `RESULTS-openevolve-p3-fuel.md`; `experiments/openevolve-p3/fuel.py`, `evaluator_fuel.py`, `test_fuel.py` |
