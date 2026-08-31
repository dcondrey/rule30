"""Primitive-necklace sweep under the boundary-pin tightening."""

import itertools
import sys
import time

from boundary_pin import BParams, bdecide, regression_boundary_pin


def primitive_necklaces(p):
    """One representative per rotation class of primitive words of length p."""
    out = []
    seen = set()
    for bits in itertools.product((0, 1), repeat=p):
        # primitive: not a repetition of a shorter block
        prim = True
        for d in range(1, p):
            if p % d == 0 and bits == bits[:d] * (p // d):
                prim = False
                break
        if not prim:
            continue
        key = min(bits[i:] + bits[:i] for i in range(p))
        if key in seen:
            continue
        seen.add(key)
        out.append(key)
    return out


def main():
    pmax = int(sys.argv[1]) if len(sys.argv) > 1 else 6
    rmax = int(sys.argv[2]) if len(sys.argv) > 2 else 4
    cap = int(sys.argv[3]) if len(sys.argv) > 3 else 4_000_000

    print("== soundness: boundary pin on true diagram, T=300 ==", flush=True)
    for R in range(1, rmax + 1):
        a30, b30 = regression_boundary_pin(30, R)
        a90, b90 = regression_boundary_pin(90, R)
        assert b30 == 0, (R, b30)
        print(f"  R={R}: rule30 {a30} antecedents / {b30} violations | "
              f"rule90 {a90} / {b90} (constraint is rule-30-specific)",
              flush=True)

    print("== rule 90 control: base pipeline, pin OFF (r90 has no pin) ==",
          flush=True)
    for R in range(1, min(rmax, 4) + 1):
        P = BParams(rule=90, right_depth=R, left_depth=1, period_word=(0,),
                    diff_q=1, boundary_pin=False)
        res, wit = bdecide(P, cap)
        print(f"  r90 w=0 R={R}: {res['verdict']} states={res['states']}",
              flush=True)
        assert res["verdict"] == "NONEMPTY", res

    print("== calibration: rule 30 p=1, pin ON ==", flush=True)
    for w, R in (((1,), 1), ((0,), 1), ((0,), 2)):
        P = BParams(rule=30, right_depth=R, left_depth=1, period_word=w,
                    diff_q=1, boundary_pin=True)
        res, _ = bdecide(P, cap)
        print(f"  w={w[0]} R={R}: {res['verdict']} states={res['states']}",
              flush=True)

    print("== primitive necklace sweep, pin ON ==", flush=True)
    table = {}
    for p in range(2, pmax + 1):
        for w in primitive_necklaces(p):
            ws = "".join(map(str, w))
            for R in range(1, rmax + 1):
                for q in (1, 2, 4):
                    P = BParams(rule=30, right_depth=R, left_depth=2,
                                period_word=w, diff_q=q, boundary_pin=True)
                    t0 = time.time()
                    res, _ = bdecide(P, cap)
                    table[(ws, R, q)] = res["verdict"]
                    print(f"  p={p} w={ws} R={R} q={q}: {res['verdict']} "
                          f"states={res['states']} t={time.time()-t0:.1f}s",
                          flush=True)

    print("== summary: any EMPTY ==", flush=True)
    empties = [k for k, v in table.items() if v == "EMPTY"]
    print(f"  {len(empties)} EMPTY cells: {empties[:40]}")


if __name__ == "__main__":
    main()
