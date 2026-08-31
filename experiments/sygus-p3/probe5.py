import time
from rule30 import truth_table
from synth import solve_k
tt = truth_table(30, 5)
for k in range(6, 14):
    r = solve_k(tt, 5, k)
    print(f"m=5 k={k:2d} {'SAT' if r.sat else 'UNSAT':>5} {r.seconds:9.2f}s  {r.n_clauses} clauses", flush=True)
    if r.sat: break
