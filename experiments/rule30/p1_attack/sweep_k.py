"""Does left_depth k tighten the ladder language?  run_rung0.py fixes k=2 and
sweeps only R; k imposes additional wedge/edge constraints on deeper columns
and is the untested knob."""
import json, sys, time
from ladder import Params, decide, verify_witness

for k in (2, 3, 4, 5, 6):
    for R in (2, 3, 4):
        t0 = time.time()
        r = decide(Params(30, R, k, (0, 1), 1), 2_000_000)
        if r["witness"] is not None:
            ok, note = verify_witness(r["witness"]["prefix"], r["witness"]["cycle"],
                                      Params(30, R, k, (0, 1), 1))
            assert ok, (k, R, note)
        print(json.dumps(dict(k=k, R=R, sec=round(time.time()-t0, 2),
                              states=r["states"], verdict=r["verdict"])), flush=True)
