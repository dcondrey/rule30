"""a19 addendum: where does target B's above-chance accuracy come from?

The models reach ~0.75-0.80 on target B out of range.  This script decomposes
that exactly, so no reader mistakes it for structure.

Three exact measurements, all on TEST = the out-of-range range, restricted to
the zero-set {c_t = 0}:

  (1) chance                : base rate of s(t,1)
  (2) one-step local-rule   : s(t,1) = c_{t-1} XOR (s(t-1,1) OR s(t-1,2)) is the
                              CA rule; guessing the OR term as 1 gives the naive
                              predictor s(t,1) := NOT c_{t-1}
  (3) exact MAJORITY table  : the empirically Bayes-optimal predictor over each
                              feature set, fitted on TRAIN.  CAVEAT, stated
                              because it matters: this bounds a model from above
                              only IN-RANGE.  Out of range a wide feature set
                              memorises, so the full table can be BEATEN by a
                              regularised model (see the depth-6 tree at 33
                              bits).  It is a ceiling on the narrow feature sets
                              and a memorisation diagnostic on the wide ones.
  (4) exact UNANIMOUS table : the only discrete CANDIDATE, with its break point.

(3) is an accuracy and is reported only next to (4)'s exact check.

Run: uv run python ceiling.py
"""

from __future__ import annotations

import json
import os

import numpy as np

from mine import TEST, TRAIN, check_table, col_history, exact_table, left_window, pack
from substrate import windows

HERE = os.path.dirname(os.path.abspath(__file__))
WMAX = 24


def majority_table(codes, y):
    order = np.argsort(codes, kind="stable")
    cs, ys = codes[order], y[order]
    b = np.flatnonzero(np.diff(cs)) + 1
    st = np.concatenate(([0], b))
    en = np.concatenate((b, [len(cs)]))
    return {int(cs[s]): int(round(float(ys[s:e].mean()))) for s, e in zip(st, en)}


def apply_table(table, codes, default=0):
    if not table:
        return np.full(len(codes), default)
    k = np.fromiter(table.keys(), dtype=np.int64, count=len(table))
    v = np.fromiter(table.values(), dtype=np.int64, count=len(table))
    o = np.argsort(k)
    k, v = k[o], v[o]
    i = np.clip(np.searchsorted(k, codes), 0, len(k) - 1)
    return np.where(k[i] == codes, v[i], default)


def main() -> None:
    A = windows(TEST[1], WMAX, "30")
    c = A[:, WMAX].astype(np.int8)
    yB = A[:, WMAX + 1].astype(np.int8)
    t_all = np.arange(len(c))
    zs = c == 0
    zs[0] = False
    tr = np.arange(*TRAIN)[zs[np.arange(*TRAIN)]]
    te = np.arange(*TEST)[zs[np.arange(*TEST)]]

    out = {"train": list(TRAIN), "test_out_of_range": list(TEST),
           "restricted_to": "{c_t = 0}"}
    out["1_chance_base_rate"] = float(max(yB[te].mean(), 1 - yB[te].mean()))
    naive = 1 - A[te - 1, WMAX].astype(int)
    out["2_one_step_local_rule_naive_NOT_c_{t-1}"] = float((naive == yB[te]).mean())

    feats = {
        "left-window W=16 only": left_window(A, WMAX, 16),
        "col-history K=16 only": col_history(c, 16),
        "left-window W=16 + col-history K=16":
            np.hstack([left_window(A, WMAX, 16), col_history(c, 16)]),
        "left-window W=8 + col-history K=8":
            np.hstack([left_window(A, WMAX, 8), col_history(c, 8)]),
    }
    rows = {}
    for name, X in feats.items():
        if X.shape[1] > 62:
            continue
        codes = pack(X)
        maj = majority_table(codes[tr], yB[tr])
        dflt = int(round(float(yB[tr].mean())))
        pm = apply_table(maj, codes[te], dflt)
        uni, _, nconf = exact_table(codes[tr], yB[tr])
        chk = check_table(uni, codes[te], yB[te], t_all[te])
        rows[name] = {
            "bits": int(X.shape[1]),
            "3_majority_table_TEST_acc_CEILING": float((pm == yB[te]).mean()),
            "4_unanimous_table_TEST": {
                "coverage": chk["coverage"],
                "acc_on_covered": chk["acc_on_covered"],
                "first_break_t": chk["first_break_t"],
                "train_conflicted_patterns": nconf,
            },
        }
    out["by_feature_set"] = rows
    with open(os.path.join(HERE, "ceiling_results.json"), "w") as f:
        json.dump(out, f, indent=1)
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
