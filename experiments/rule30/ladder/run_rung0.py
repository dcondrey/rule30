"""Rung-0 protocol runner for the periodicity ladder (route R7).

Order: soundness regressions, calibration A (Rule 30 p=1, both tails),
calibration B (Rule 90 control), then the open case p=2 tail 01 with
increasing right depth R.  Emits one JSON line per run plus a final table.
"""

import json
import sys
import time

from ladder import Params, decide, regression, verify_witness


def run(label, P, max_states=3_000_000):
    t0 = time.time()
    res = decide(P, max_states)
    dt = time.time() - t0
    if res["witness"] is not None:
        okv, note = verify_witness(res["witness"]["prefix"],
                                   res["witness"]["cycle"], P)
        res["witness_verified"] = okv
        res["witness_note"] = note
        assert okv, (label, note)
    row = dict(label=label, seconds=round(dt, 2), **{
        k: v for k, v in res.items() if k != "witness"})
    print(json.dumps(row), flush=True)
    return res


def main():
    print("# soundness regressions (T=300, zero tolerance)", flush=True)
    for rule in (30, 90):
        for R, k in ((1, 1), (2, 2), (3, 2), (4, 2), (5, 2)):
            mism, ok = regression(rule, R, k, T=300)
            assert mism == 0 and ok, (rule, R, k, mism, ok)
            print(f"regression rule={rule} R={R} k={k}: "
                  f"0 mismatches, safety run ok", flush=True)

    print("# calibration A: rule 30, p=1", flush=True)
    run("A1 w=1 q=1 R=1", Params(30, 1, 1, (1,), 1))
    run("A1 w=1 q=1 R=2", Params(30, 2, 1, (1,), 1))
    run("A2 w=0 q=1 R=1", Params(30, 1, 1, (0,), 1))
    run("A3 w=0 q=1 R=2", Params(30, 2, 1, (0,), 1))

    print("# calibration B: rule 90 control, must stay NONEMPTY", flush=True)
    for R in (1, 2, 3, 4, 5):
        run(f"B w=0 q=1 R={R}", Params(90, R, 1, (0,), 1))

    print("# open case: rule 30, p=2, tail 01", flush=True)
    verdicts = {}
    max_R = int(sys.argv[1]) if len(sys.argv) > 1 else 7
    for R in range(1, max_R + 1):
        # plain emptiness first (mode i), then Diff_q ladder (mode ii)
        res = run(f"p2 plain R={R}", Params(30, R, 2, (0, 1), None))
        verdicts[(R, None)] = res["verdict"]
        for q in (1, 2, 4, 8):
            res = run(f"p2 q={q} R={R}", Params(30, R, 2, (0, 1), q))
            verdicts[(R, q)] = res["verdict"]
            if res["verdict"] == "EMPTY":
                print(f"*** EMPTY at R={R}, q={q}: per-period exclusion "
                      f"candidate; re-verify soundness before claiming.",
                      flush=True)

    print("# verdict table (R x q)", flush=True)
    qs = [None, 1, 2, 4, 8]
    print("R  " + "  ".join(f"{'plain' if q is None else 'q='+str(q):>7}"
                            for q in qs))
    for R in range(1, max_R + 1):
        print(f"{R}  " + "  ".join(
            f"{verdicts.get((R, q), '-'):>7}" for q in qs))


if __name__ == "__main__":
    main()
