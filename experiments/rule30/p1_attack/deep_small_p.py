"""Push (R,k,q) on representative p=3..5 tails, to test whether the p=2
no-tightening finding (sweep_k.py) is p-uniform."""
import json, time
from ladder import Params, decide, verify_witness
WORDS = [(1,0,0),(1,1,0),(1,0,0,0),(1,1,0,0),(1,1,1,0),(1,0,1,0,0),(1,1,0,1,0)]
for w in WORDS:
    for (R, k, q) in ((4,3,1),(4,3,2),(3,5,1),(5,2,4)):
        P = Params(30, R, k, w, q); t0 = time.time()
        r = decide(P, 2_000_000)
        if r["witness"] is not None:
            ok, note = verify_witness(r["witness"]["prefix"], r["witness"]["cycle"], P)
            assert ok, (w, R, k, q, note)
        print(json.dumps({"w": "".join(map(str,w)), "R": R, "k": k, "q": q,
                          "states": r["states"], "sec": round(time.time()-t0,2),
                          "verdict": r["verdict"]}), flush=True)
