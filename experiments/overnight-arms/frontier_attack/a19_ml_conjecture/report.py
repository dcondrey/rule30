"""Render mine_results.json as a clean table.  Run: uv run python report.py"""

from __future__ import annotations

import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))


def f(x, w=6):
    return "n/a".rjust(w) if x is None else f"{x:.4f}".rjust(w)


def main() -> None:
    d = json.load(open(os.path.join(HERE, "mine_results.json")))
    for rule in ("30", "90"):
        rs = [r for r in d if r["rule"] == rule]
        if not rs:
            continue
        r0 = rs[0]
        print(f"\n===== RULE {rule}   TRAIN {r0['train_range']}  "
              f"DEV {r0['dev_range']}  TEST(out of range) {r0['test_range']}")
        print(f"{'framing':46s} {'b':>2s} {'trainTblConflicts':>17s} "
              f"{'DEVacc':>6s} {'DEVcov':>6s} {'DEVbrk':>8s} "
              f"{'TSTacc':>6s} {'TSTcov':>6s} {'TSTbrk':>8s} "
              f"{'core':>6s} {'shell':>6s} {'gf2<=3'}")
        for r in rs:
            dv, te = r["dev_in_range"], r["test_out_of_range"]
            core = shell = None
            if "pin_core_c1" in te:
                core = te["pin_core_c1"]["acc_on_covered"]
                shell = te["shell_c0"]["acc_on_covered"]
            g = ""
            if "gf2_by_degree" in r:
                ok = [str(k) for k, v in r["gf2_by_degree"].items()
                      if v["exact_fit_exists"]]
                g = ",".join(ok) if ok else "NONE"
            print(f"{r['framing']:46s} {r['bits']:2d} "
                  f"{'CONSISTENT' if r['table_consistent_on_train'] else str(r['train_conflicted_patterns']):>17s} "
                  f"{f(dv['acc_on_covered'])} {dv['coverage']:6.3f} "
                  f"{str(dv['first_break_t']):>8s} "
                  f"{f(te['acc_on_covered'])} {te['coverage']:6.3f} "
                  f"{str(te['first_break_t']):>8s} "
                  f"{f(core)} {f(shell)} {g}")


if __name__ == "__main__":
    main()
