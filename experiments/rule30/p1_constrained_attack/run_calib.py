"""Calibration for the Q-conjunction encoding, then the cheapest
disconfirming test: p=2 at Q=1,2,3,4 on (R,k)=(2,2)."""
import json, time
from constrained import CParams, decide, regression, verify_witness

def run(label, P, cap=3_000_000):
    t0 = time.time(); r = decide(P, cap)
    if r["witness"]:
        ok, note = verify_witness(r["witness"]["prefix"], r["witness"]["cycle"], P)
        assert ok, (label, note)
        r["wv"] = note
    r.pop("witness", None)
    print(json.dumps(dict(label=label, sec=round(time.time()-t0, 2), **r)), flush=True)
    return r

print("# regression: true lone-seed word never rejected", flush=True)
for rule in (30, 90):
    for R, k in ((1,1),(2,2),(3,2),(4,2)):
        P = CParams(rule, R, k, (0,), 4)
        mism, ok, pins = regression(P)
        assert mism == 0 and ok, (rule, R, k, mism, ok)
        print(f"regression rule={rule} R={R} k={k}: 0 mismatches, accepted", flush=True)

print("# Q=1 must reproduce rung-0 fixed-q=1 verdicts", flush=True)
run("Q1 r30 w=1 R=1", CParams(30, 1, 1, (1,), 1))
run("Q1 r30 w=0 R=2", CParams(30, 2, 1, (0,), 1))
run("Q1 r30 w=01 R=2 k=2", CParams(30, 2, 2, (0,1), 1))
print("# rule 90 control: must stay NONEMPTY at every Q", flush=True)
for Q in (1, 2, 3, 4):
    run(f"ctrl r90 w=0 R=2 Q={Q}", CParams(90, 2, 1, (0,), Q))
print("# calibration: rule 30 p=1 must stay EMPTY at every Q", flush=True)
for Q in (2, 3, 4):
    run(f"cal r30 w=1 R=1 Q={Q}", CParams(30, 1, 1, (1,), Q))
    run(f"cal r30 w=0 R=2 Q={Q}", CParams(30, 2, 1, (0,), Q))
print("# OPEN: p=2 tail 01, climbing Q", flush=True)
for Q in (2, 3, 4, 5, 6):
    run(f"open r30 w=01 R=2 k=2 Q={Q}", CParams(30, 2, 2, (0,1), Q))
