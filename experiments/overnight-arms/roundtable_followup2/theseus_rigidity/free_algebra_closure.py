"""Confirm, by exhaustive truth table, that the free Boolean algebra on one
generator s has exactly 4 elements {0, 1, s, not-s} and is closed under
AND, OR, XOR, NOT -- i.e. any Boolean formula built from a single atom s
using these connectives is semantically one of these four functions.

Representation: a 1-variable Boolean function is identified with the pair
(f(0), f(1)).  0 -> (0,0), 1 -> (1,1), s -> (0,1), not-s -> (1,0).
"""

ELEMENTS = {
    "0": (0, 0),
    "1": (1, 1),
    "s": (0, 1),
    "not s": (1, 0),
}
INV = {v: k for k, v in ELEMENTS.items()}


def op(f, g, fn):
    return tuple(fn(f[i], g[i]) for i in range(2))


def unop(f, fn):
    return tuple(fn(f[i]) for i in range(2))


def main():
    names = list(ELEMENTS)
    print("Closure check for AND / OR / XOR over {0,1,s,not s}:")
    for name_op, fn in [("AND", lambda a, b: a & b), ("OR", lambda a, b: a | b), ("XOR", lambda a, b: a ^ b)]:
        ok = True
        for a in names:
            for b in names:
                r = op(ELEMENTS[a], ELEMENTS[b], fn)
                if r not in INV:
                    ok = False
                    print(f"  FAIL: {a} {name_op} {b} = {r} not in algebra")
        print(f"  {name_op}: closed = {ok}")
    ok = True
    for a in names:
        r = unop(ELEMENTS[a], lambda x: 1 - x)
        if r not in INV:
            ok = False
    print(f"  NOT: closed = {ok}")
    print()
    print("Since Rule 30's local update new = left XOR (center OR right) and")
    print("Rule 90's is new = left XOR right, both are built purely from XOR")
    print("and OR (Rule 30) or XOR alone (Rule 90). Starting every cell's")
    print("formal value as a constant (0) except the seed cell (= s), closure")
    print("under these connectives means EVERY cell at EVERY time step is,")
    print("as a formal function of s, restricted to this 4-element algebra --")
    print("for any single-seed 2-state CA built from AND/OR/XOR/NOT, not just")
    print("Rule 30 or Rule 90. This is forced by construction, not measured.")


if __name__ == "__main__":
    main()
