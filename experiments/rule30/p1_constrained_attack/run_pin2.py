"""Pin variants: cascade corollary vs full 1-pin, alone and with the
Q-conjunction.  The pin is a Rule 30 theorem (PATH.md sec 1) and is NOT
entailed at the rightmost modelled column, where the forward rule is not
enforced; that is where it bites."""
import json, sys, time
from constrained import CParams, decide, regression, verify_witness

def run(tag, P, cap=3_000_000):
    t0 = time.time(); r = decide(P, cap)
    row = dict(tag=tag, sec=round(time.time()-t0,2), **r["params"],
               states=r["states"], pin_violations=r["pin_violations"],
               verdict=r["verdict"])
    if r["witness"]:
        ok, note = verify_witness(r["witness"]["prefix"], r["witness"]["cycle"], P)
        assert ok, (tag, note)
        row["cycle_len"] = len(r["witness"]["cycle"]); row["wv"] = note
    print(json.dumps(row), flush=True)
    return row

def necklaces(p):
    seen, out = set(), []
    for n in range(1 << p):
        w = tuple((n >> i) & 1 for i in range(p))
        if any(all(w[i]==w[(i+d)%p] for i in range(p)) for d in range(1,p) if p%d==0):
            continue
        rots = frozenset(tuple(w[(i+r)%p] for i in range(p)) for r in range(p))
        if rots in seen: continue
        seen.add(rots); out.append(w)
    return out

mode = sys.argv[1]
if mode == "sound":
    print("# soundness: true lone-seed word must survive both pin modes", flush=True)
    for rule in (30, 90):
        for R,k in ((2,2),(3,2),(4,2),(3,3)):
            for pa,pf in ((True,False),(False,True)):
                m,ok,h = regression(CParams(rule,R,k,(0,),2,pin_audit=pa,pin_full=pf))
                print(f"rule={rule} R={R} k={k} cascade={pa} full={pf}: "
                      f"{m} mismatches, accepted={ok}, hits={h}", flush=True)
    print("# calibration under pins: r30 p=1 EMPTY, r90 w=0 NONEMPTY", flush=True)
    for pa,pf in ((True,False),(False,True)):
        run(f"cal r30 w=1 cascade={pa} full={pf}", CParams(30,1,1,(1,),2,pin_audit=pa,pin_full=pf))
        run(f"cal r30 w=0 cascade={pa} full={pf}", CParams(30,2,1,(0,),2,pin_audit=pa,pin_full=pf))
        run(f"ctrl r90 w=0 cascade={pa} full={pf}", CParams(90,2,1,(0,),2,pin_audit=pa,pin_full=pf))
elif mode == "climb":
    print("# p=2, full pin + Q-conjunction climb", flush=True)
    for Q in range(1, 15):
        r = run(f"pinfull Q={Q}", CParams(30,2,2,(0,1),Q,pin_full=True))
        if r["verdict"] != "NONEMPTY": break
elif mode == "sweep":
    print("# necklaces p=2..8, R=2 k=2, Q=4, full pin", flush=True)
    for p in range(2, 9):
        for w in necklaces(p):
            run(f"p={p} w={''.join(map(str,w))}", CParams(30,2,2,w,4,pin_full=True))
