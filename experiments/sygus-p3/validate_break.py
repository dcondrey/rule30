"""Unconditional validation of the distinct-fanin-pair symmetry break.

(1) All 256 three-bit functions: full k_min with the break on and off must
    agree.  Complete across every k at that arity.
(2) Rule 30, m=4, k=1..4 with the break DISABLED: verifies the actual claimed
    m=4 theorem (k_min=5, i.e. UNSAT at k=4) without relying on the break.
"""
import json
from rule30 import truth_table
from synth import k_min, solve_k

diff = []
for f in range(256):
    tt = [(f >> t) & 1 for t in range(8)]
    a, _ = k_min(tt, 3, kmax=5, distinct_pairs=True, colex=True)
    b, _ = k_min(tt, 3, kmax=5, distinct_pairs=False, colex=False)
    if a != b:
        diff.append((f, a, b))
print(json.dumps({"m3_all256_mismatches": diff}), flush=True)

tt = truth_table(30, 4, 0)
rows = []
for k in range(1, 5):
    r = solve_k(tt, 4, k, distinct_pairs=False, colex=False)
    rows.append({"k": k, "sat": r.sat, "s": round(r.seconds, 2)})
    print(rows[-1], flush=True)
r5 = solve_k(tt, 4, 5, distinct_pairs=False, colex=False)
rows.append({"k": 5, "sat": r5.sat, "s": round(r5.seconds, 2)})
print(rows[-1], flush=True)
json.dump({"m3_all256_mismatches": diff, "rule30_m4_no_breaks": rows},
          open("validate_break.json", "w"), indent=1)
