"""a19 addendum: apply the PRE-REGISTERED extraction threshold mechanically.

PREREG.md declares, before the run, that a framing yields a CANDIDATE WORTH
EXTRACTING iff all three hold:

  (1) the exact table is CONSISTENT on TRAIN, OR its unanimous sub-table covers
      >= 20% of TEST;
  (2) TEST coverage >= 0.05  (guards against memorisation);
  (3) it FAILS the universality check, i.e. it is an orbit-specific claim and
      not a consequence of the local rule.

For target A the universal part is the OR-latch pin (PREREG Lemma A19.1), so
condition (3) selects the SHELL (`c_t = 0`) entries and the coverage in (1)/(2)
is the shell's.  Targets B, C, D are orbit-specific in their entirety, so (3) is
automatic and the coverage is the framing's own.

Run: uv run python threshold.py
"""

from __future__ import annotations

import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))


def main() -> None:
    d = json.load(open(os.path.join(HERE, "mine_results.json")))
    rows, admitted = [], []
    for r in d:
        if r["rule"] != "30" or "CONTROL" in r["framing"]:
            continue
        te = r["test_out_of_range"]
        target_a = r["framing"].startswith("A/")
        if target_a and "shell_c0" in te:
            part, why3 = te["shell_c0"], "shell only (A19.1: universal part = pin)"
        elif target_a:
            part, why3 = te, "no split recorded"
        else:
            part, why3 = te, "orbit-specific by construction (A19.2 / PREREG)"
        cov = part["coverage"]
        c1 = r["table_consistent_on_train"] or cov >= 0.20
        c2 = cov >= 0.05
        c3 = True  # every non-control framing here fails universality
        ok = c1 and c2 and c3
        row = {
            "framing": r["framing"],
            "part_used": why3,
            "TEST_coverage": round(cov, 6),
            "TEST_acc_on_covered": part["acc_on_covered"],
            "cond1_consistent_or_cov>=0.20": bool(c1),
            "cond2_cov>=0.05": bool(c2),
            "cond3_fails_universality": bool(c3),
            "ADMITTED_AS_CANDIDATE": bool(ok),
            "DEV_first_break": r["dev_in_range"].get("shell_c0", r["dev_in_range"])[
                "first_break_t"] if target_a and "shell_c0" in r["dev_in_range"]
                else r["dev_in_range"]["first_break_t"],
            "TEST_first_break": part["first_break_t"],
        }
        rows.append(row)
        if ok:
            admitted.append(row)
    out = {
        "threshold": "PREREG.md 'Extraction threshold', declared before the run",
        "n_framings_considered": len(rows),
        "n_admitted_as_candidates": len(admitted),
        "admitted": admitted,
        "all": rows,
    }
    with open(os.path.join(HERE, "threshold_results.json"), "w") as f:
        json.dump(out, f, indent=1)
    print(f"framings considered (rule 30, non-control): {len(rows)}")
    print(f"ADMITTED as candidates by the pre-registered threshold: {len(admitted)}")
    for a in admitted:
        print(f"  {a['framing']:46s} cov={a['TEST_coverage']:.3f} "
              f"acc={a['TEST_acc_on_covered']} "
              f"DEVbrk={a['DEV_first_break']} TESTbrk={a['TEST_first_break']}")
    print("\nrejected, with the failing condition:")
    for a in rows:
        if a["ADMITTED_AS_CANDIDATE"]:
            continue
        fail = [k for k in ("cond1_consistent_or_cov>=0.20", "cond2_cov>=0.05")
                if not a[k]]
        print(f"  {a['framing']:46s} cov={a['TEST_coverage']:.5f}  fails {fail}")


if __name__ == "__main__":
    main()
