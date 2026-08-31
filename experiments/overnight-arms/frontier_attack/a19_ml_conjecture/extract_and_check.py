"""a19 step 2: extract the surviving candidates EXPLICITLY, test universality,
exact-check them out of range, and take a model-class ceiling on target B.

Nothing here reports an accuracy without an exact check beside it.

Run: uv run python extract_and_check.py
"""

from __future__ import annotations

import json
import os

import numpy as np

from mine import (DEV, TEST, TRAIN, col_history, left_window, pack,
                  exact_table, check_table)
from substrate import windows

HERE = os.path.dirname(os.path.abspath(__file__))
WMAX = 24
N = TEST[1]
out: dict = {"train": list(TRAIN), "dev": list(DEV), "test": list(TEST)}


# --------------------------------------------------------------- universality


def _next_center(cm1: int, c0: int, r: int, rule: str) -> int:
    if rule == "30":
        return cm1 ^ (c0 | r)
    if rule == "90":
        return cm1 ^ r
    raise ValueError(rule)


def universal_targetA(table: dict, Wl: int, rule: str = "30") -> dict:
    """Which entries of a target-A left-window table are FORCED by the local rule?

    c_{t+1} = s(t,-1) XOR (c_t OR s(t,1)).  The only free bit is s(t,1).  An
    entry (pattern -> v) is universal iff both values of s(t,1) give v.
    Enumerated exhaustively over all 2^(Wl+1) patterns.
    """
    universal, orbit_only, contradicted = 0, 0, 0
    detail = []
    for code, v in table.items():
        bits = [(code >> j) & 1 for j in range(Wl + 1)]
        # bits[j] = s(t, -Wl + j); so s(t,0) = bits[Wl], s(t,-1) = bits[Wl-1]
        c0, cm1 = bits[Wl], bits[Wl - 1]
        vals = {_next_center(cm1, c0, r, rule) for r in (0, 1)}
        if len(vals) == 1:
            if vals.pop() == v:
                universal += 1
                detail.append((code, v, "universal"))
            else:
                contradicted += 1  # impossible unless the pipeline is broken
        else:
            orbit_only += 1
    assert contradicted == 0, "extracted entry contradicts the Rule 30 local law"
    return {"entries": len(table), "universal": universal,
            "orbit_specific": orbit_only, "contradicted": contradicted,
            "detail_head": detail[:8]}


# ------------------------------------------------------------------- run both


for rule in ("30", "90"):
    A = windows(N, WMAX, rule)
    c = A[:, WMAX].astype(np.int8)
    n = len(c)
    t_all = np.arange(n)
    yA = np.zeros(n, dtype=np.int8)
    yA[:-1] = c[1:]
    tr = np.arange(*TRAIN)
    te = np.arange(*TEST)
    rec: dict = {}

    # ---- the one surviving target-A candidate, made explicit -------------
    for Wl in (2, 8, 12):
        X = left_window(A, WMAX, Wl)
        codes = pack(X)
        table, npat, nconf = exact_table(codes[tr], yA[tr])
        u = universal_targetA(table, Wl, rule)
        # keep ONLY the universal entries and exact-check them out of range
        uni = {k: v for k, v in table.items()
               if len({_next_center((k >> (Wl - 1)) & 1, (k >> Wl) & 1, r, rule)
                       for r in (0, 1)}) == 1}
        orb = {k: v for k, v in table.items() if k not in uni}
        # exact break witness for the orbit-specific (accidental) sub-table
        witness = None
        if orb:
            ok = np.fromiter(orb.keys(), dtype=np.int64, count=len(orb))
            ov = np.fromiter(orb.values(), dtype=np.int64, count=len(orb))
            o = np.argsort(ok)
            ok, ov = ok[o], ov[o]
            ix = np.clip(np.searchsorted(ok, codes[te]), 0, len(ok) - 1)
            covm = ok[ix] == codes[te]
            bad = covm & (ov[ix] != yA[te])
            if bad.any():
                j = int(np.flatnonzero(bad)[0])
                tb = int(t_all[te][j])
                pat = int(codes[te][j])
                witness = {
                    "t": tb,
                    "window_s(t,-W..0)": "".join(
                        str((pat >> b) & 1) for b in range(Wl + 1)),
                    "predicted_c_{t+1}": int(ov[ix][j]),
                    "actual_c_{t+1}": int(yA[te][j]),
                    "n_train_rows_supporting_this_pattern": int(
                        (codes[tr] == pat).sum()),
                }
        rec[f"A/left-window W={Wl}"] = {
            "orbit_specific_break_witness": witness,
            "table_entries": len(table), "train_conflicts": nconf,
            "universality": u,
            "universal_subtable_TEST": check_table(uni, codes[te], yA[te],
                                                   t_all[te]),
            "orbit_specific_subtable_TEST": check_table(orb, codes[te], yA[te],
                                                        t_all[te]),
        }

    # ---- the explicit pin statement, verified exhaustively ---------------
    # PATH.md section 1: s(t,x)=1 => s(t,x-1) = NOT s(t+1,x).
    B = A.astype(int)
    ones = B[:-1, 1:] == 1
    lhs = B[:-1, :-1]                      # s(t, x-1)
    rhs = 1 - B[1:, 1:]                    # NOT s(t+1, x)
    viol = int((ones & (lhs != rhs)).sum())
    rec["PIN identity s(t,x)=1 => s(t,x-1)=NOT s(t+1,x)"] = {
        "columns_checked": f"x in [-{WMAX-1}, {WMAX}]",
        "rows_checked": n - 1,
        "ones_tested": int(ones.sum()),
        "violations": viol,
    }

    # ---- target B model-class ceiling (accuracy ONLY, exact check follows)
    yB = A[:, WMAX + 1].astype(np.int8)
    zs = c == 0
    itr, ite = tr[zs[tr]], te[zs[te]]
    ceiling = {}
    if len(itr) > 500 and len(ite) > 500:
        from sklearn.ensemble import RandomForestClassifier
        from sklearn.linear_model import LogisticRegression
        from sklearn.neural_network import MLPClassifier
        from sklearn.tree import DecisionTreeClassifier, export_text
        Xb = np.hstack([left_window(A, WMAX, 16), col_history(c, 16)])
        models = {
            "logistic": LogisticRegression(max_iter=2000),
            "tree_d6": DecisionTreeClassifier(max_depth=6, random_state=0),
            "tree_d14": DecisionTreeClassifier(max_depth=14, random_state=0),
            "forest_200": RandomForestClassifier(n_estimators=200, random_state=0,
                                                 n_jobs=-1),
            "mlp_64x64": MLPClassifier((64, 64), max_iter=300, random_state=0),
        }
        for nm, mdl in models.items():
            mdl.fit(Xb[itr], yB[itr])
            a_tr = float((mdl.predict(Xb[itr]) == yB[itr]).mean())
            a_te = float((mdl.predict(Xb[ite]) == yB[ite]).mean())
            ceiling[nm] = {"train_acc": a_tr, "TEST_out_of_range_acc": a_te}
        # the only extractable one: read the depth-6 tree out as a rule set and
        # exact-check every leaf out of range.
        t6 = models["tree_d6"]
        leaves_tr = t6.apply(Xb[itr])
        pred_tr = t6.predict(Xb[itr])
        pure = {}
        for lf in np.unique(leaves_tr):
            m = leaves_tr == lf
            if len(np.unique(yB[itr][m])) == 1:
                pure[int(lf)] = int(yB[itr][m][0])
        leaves_te = t6.apply(Xb[ite])
        cov = np.isin(leaves_te, list(pure.keys()))
        predv = np.array([pure.get(int(l), -1) for l in leaves_te])
        wrong = cov & (predv != yB[ite])
        ceiling["tree_d6_pure_leaf_extraction"] = {
            "pure_leaves_on_train": len(pure),
            "TEST_coverage": float(cov.mean()),
            "TEST_errors_on_covered": int(wrong.sum()),
            "TEST_acc_on_covered": float(1 - wrong.sum() / max(1, int(cov.sum()))),
            "first_break_t": int(t_all[ite][wrong][0]) if wrong.any() else None,
        }
        ceiling["tree_d6_rules_head"] = export_text(t6, max_depth=3)[:1200]
        ceiling["base_rate_r_on_zeroset_TEST"] = float(yB[ite].mean())
    rec["targetB_model_ceiling"] = ceiling

    # ---- why target-B framings that see c_{t-1} sit near 0.75, not 0.5 ----
    # s(t,1) = s(t-1,0) XOR (s(t-1,1) OR s(t-1,2)) is the local rule, so the
    # naive predictor  s(t,1) := NOT c_{t-1}  is right exactly when
    # s(t-1,1) OR s(t-1,2) = 1.  Measured, not asserted.
    if rule == "30":
        zs1 = zs.copy()
        zs1[0] = False
        i = np.flatnonzero(zs1[TEST[0]:TEST[1]]) + TEST[0]
        orv = (A[i - 1, WMAX + 1] | A[i - 1, WMAX + 2]).astype(int)
        naive = 1 - A[i - 1, WMAX].astype(int)
        rec["targetB_0.75_explanation"] = {
            "range": list(TEST),
            "P(s(t-1,1) OR s(t-1,2) = 1 | c_t = 0)": float(orv.mean()),
            "acc of naive predictor s(t,1) := NOT c_{t-1} on {c_t=0}":
                float((naive == yB[i]).mean()),
            "base rate P(s(t,1)=1 | c_t=0)": float(yB[i].mean()),
        }
    out[f"rule{rule}"] = rec
    print(f"== rule {rule} done")

with open(os.path.join(HERE, "extract_results.json"), "w") as f:
    json.dump(out, f, indent=1, default=str)
print(json.dumps({k: v for k, v in out.items() if k.startswith("rule")},
                 indent=1, default=str)[:6000])
