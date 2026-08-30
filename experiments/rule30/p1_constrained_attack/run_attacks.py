"""Agent 1 (right-wedge), Agent 2 (pin cascade), Agent 3 (Q-conjunction)."""
import json, sys, time
from constrained import CParams, decide, regression, verify_witness

def run(tag, P, cap=3_000_000):
    t0 = time.time(); r = decide(P, cap)
    row = dict(tag=tag, sec=round(time.time()-t0, 2), **r["params"],
               states=r["states"], pin_violations=r["pin_violations"],
               verdict=r["verdict"])
    if r["witness"]:
        ok, note = verify_witness(r["witness"]["prefix"], r["witness"]["cycle"], P)
        assert ok, (tag, note)
        row["cycle_len"] = len(r["witness"]["cycle"])
        row["wv"] = note
    print(json.dumps(row), flush=True)
    return row

def necklaces(p):
    seen, out = set(), []
    for n in range(1 << p):
        w = tuple((n >> i) & 1 for i in range(p))
        if any(all(w[i] == w[(i+d) % p] for i in range(p))
               for d in range(1, p) if p % d == 0):
            continue
        rots = frozenset(tuple(w[(i+r) % p] for i in range(p)) for r in range(p))
        if rots in seen:
            continue
        seen.add(rots); out.append(w)
    return out

which = sys.argv[1]

if which == "wedge":
    # AGENT 1: the right wedge is already imposed.  Disabling it must loosen.
    print("# right-wedge ON vs OFF, identical params otherwise", flush=True)
    for w in ((0,1), (1,0,0), (1,1,0,0)):
        for R, k in ((2,2), (3,2), (4,2)):
            for wr in (True, False):
                run(f"wedge w={''.join(map(str,w))} R={R} k={k} wr={wr}",
                    CParams(30, R, k, w, 1, wedge_right=wr))

elif which == "pin":
    # AGENT 2: pin cascade as an explicit safety filter.  Entailed => no change.
    print("# pin audit OFF vs ON; pin_violations must be 0 and states equal",
          flush=True)
    for rule in (30,):
        for R, k in ((2,2), (3,2), (4,2), (3,3)):
            mism, ok, pins = regression(CParams(rule, R, k, (0,), 2,
                                                pin_audit=True))
            print(f"regression rule={rule} R={R} k={k} pin_audit: "
                  f"{mism} mismatches, accepted={ok}, pin_hits={pins}",
                  flush=True)
    for p in (2, 3, 4):
        for w in necklaces(p):
            for pa in (False, True):
                run(f"pin w={''.join(map(str,w))} pa={pa}",
                    CParams(30, 2, 2, w, 2, pin_audit=pa))

elif which == "qclimb":
    # AGENT 3: climb Q on p=2, recording the witness cycle length.
    print("# Q-conjunction climb, p=2 tail 01, R=2 k=2", flush=True)
    for Q in range(1, 17):
        r = run(f"qclimb Q={Q}", CParams(30, 2, 2, (0,1), Q))
        if r["verdict"] != "NONEMPTY":
            break

elif which == "qsweep":
    # AGENT 3: necklace sweep under the conjunction.
    print("# Q=4 conjunction, all primitive necklaces p=2..6, R=2 k=2",
          flush=True)
    for p in range(2, 7):
        for w in necklaces(p):
            run(f"qsweep p={p} w={''.join(map(str,w))}",
                CParams(30, 2, 2, w, 4))
