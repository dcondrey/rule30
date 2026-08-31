"""Single (rule, m, k) synthesis call, for running the m=5 bracket in parallel."""
import json, sys, time
from rule30 import truth_table
from synth import solve_k, verify_chain
name, m, k = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
tt = truth_table(int(name), m, 0)
r = solve_k(tt, m, k)
ok = verify_chain(r.chain, tt, m) if r.sat else None
rec = {"rule": int(name), "m": m, "k": k, "sat": r.sat, "seconds": round(r.seconds,2),
       "clauses": r.n_clauses, "chain_verified": ok,
       "chain": [[c[0], list(c[1]), list(c[2])] for c in r.chain] if r.chain else None}
print(json.dumps(rec), flush=True)
open(f"bracket_r{name}_m{m}_k{k}.json","w").write(json.dumps(rec, indent=1))
