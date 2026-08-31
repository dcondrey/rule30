"""Two-directional sanity tests for the exact synthesiser.

An unsound encoding (too few constraints) and an over-constrained one fail in
opposite directions, so both are checked:

  LOWER SIDE  -- a function must not come back SAT below its known minimum.
                 Catches an under-constrained encoding, which would make
                 every reported k_min too small.
  UPPER SIDE  -- no m-bit function may come back UNSAT at k >= u(m), the
                 known maximum combinational complexity over all m-bit
                 functions.  Catches an over-constrained encoding, which
                 would make every reported UNSAT worthless.

Known minima over the full B2 basis (Knuth, TAOCP 4A, 7.1.2):
  u(2) = 1, u(3) = 4, u(4) = 7, u(5) = 12.
  C(XOR2) = 1, C(MAJ3) = 4, C(parity_m) = m - 1.

The optional symmetry breaks (distinct fanin pairs, colex step ordering) are
validated by running the whole suite with them on and off and requiring the
same k_min from both.
"""

import itertools

from synth import k_min, solve_k, verify_chain


def tt_from_fn(fn, m):
    return [fn([(t >> (m - 1 - j)) & 1 for j in range(m)]) for t in range(1 << m)]


CASES = [
    ("xor2", 2, tt_from_fn(lambda v: v[0] ^ v[1], 2), 1),
    ("and2", 2, tt_from_fn(lambda v: v[0] & v[1], 2), 1),
    ("maj3", 3, tt_from_fn(lambda v: sum(v) >= 2, 3), 4),
    ("parity3", 3, tt_from_fn(lambda v: v[0] ^ v[1] ^ v[2], 3), 2),
    ("parity4", 4, tt_from_fn(lambda v: v[0] ^ v[1] ^ v[2] ^ v[3], 4), 3),
    ("and4", 4, tt_from_fn(lambda v: v[0] & v[1] & v[2] & v[3], 4), 3),
    ("maj3_of_4ignored", 4, tt_from_fn(lambda v: sum(v[:3]) >= 2, 4), 4),
]

U = {2: 1, 3: 4, 4: 7, 5: 12}


def run(**kw):
    ok = True
    for name, m, tt, expect in CASES:
        k, trace = k_min(tt, m, kmax=expect + 2, **kw)
        good = k == expect
        ok &= good
        chain_ok = verify_chain(trace[-1].chain, tt, m) if trace and trace[-1].sat else False
        print(f"  {name:18s} m={m} k_min={k} expected={expect} "
              f"{'OK' if good else 'FAIL'} chain_verified={chain_ok}")
        if not chain_ok:
            ok = False
    return ok


def upper_side(**kw):
    """No 3-bit function may be UNSAT at k = u(3) = 4.  Exhaustive: all 256."""
    bad = []
    for f in range(256):
        tt = [(f >> t) & 1 for t in range(8)]
        r = solve_k(tt, 3, U[3], **kw)
        if not r.sat and not all(v == tt[0] for v in tt):
            # constants genuinely have no length-4 chain with no dead step
            bad.append(f)
    return bad


if __name__ == "__main__":
    for kw in ({"distinct_pairs": True, "colex": True},
               {"distinct_pairs": False, "colex": False}):
        print(f"symmetry breaks {kw}:")
        ok = run(**kw)
        print(f"  lower side: {'PASS' if ok else 'FAIL'}")
    print("upper side, all 256 three-bit functions at k=u(3)=4:")
    bad = upper_side(distinct_pairs=True, colex=True)
    print(f"  functions UNSAT at k=4 (excluding constants): {len(bad)}"
          f"{'' if not bad else ' -> ' + str(bad[:10])}")
