"""The k-comparable invariant of the R7 ladder: never computed before.

`RESULTS-ladder-rung1.md` section 4 measures the accepting tail system's
bisimulation-class count against the RIGHT depth R and finds `~R^2.75`, the
same exponent with and without the pin.  `RESULTS-ladder-rung0.md` section 3
sweeps the LEFT depth k but reports only raw product-state counts, which rung 0
itself says prove nothing: they are dominated by the `4^(R+k)` alphabet factor,
flat at `states / 4^(R+k) ~ 5.4` in both directions.

So the k-comparable quantity has never been computed.  This file computes it,
at fixed R = 2, using rung 1's own `tail_language`, which accepts arbitrary
Params and is not restricted to the R sweep its driver performs.

Reading, fixed in advance:

  * classes grow in k about as they grow in R  ->  left and right truncation are
    the same defect; the free boundary has a left twin.
  * classes do not grow in k  ->  report exactly that and nothing more.
    Bisimulation classes are coarser than the minimized language (rung 1 section
    4 method note) and class count is not monotone under language inclusion
    (rung 1 section 4, third consequence), so a flat count is CONSISTENT with
    the language still shrinking in k.  The inverse-limit conclusion ("a genuine
    word exists at every left depth") does NOT follow and must not be written.

Rule 90 filter: the identical sweep runs on the rule-90 ladder with its own true
eventually-zero centre word, plain (rung 1 Lemma 1' -- rule 90's extendability
condition is vacuous, so rule 30's pin is never applied to it).  Rule 90's
language provably contains a genuine realizable word.  If the two k-exponents
agree the way rung 1's two R-exponents did, the growth is a property of the
encoding and separates nothing.

Note `Params.x_min` is `-max(k, 1)` when `diff_q` is set, so k = 0 and k = 1 are
the same automaton in mode (ii).  The fit starts at k = 2.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import math
import sys

_LADDER_DIR = "/Volumes/A/researchpapers/13-rule30/experiments/rule30/ladder"
sys.path.insert(0, _LADDER_DIR)


def _load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


LAD = _load(f"{_LADDER_DIR}/ladder.py", "ladder")
R1 = _load(f"{_LADDER_DIR}/rung1.py", "rung1")
Params = LAD.Params


def loglog_fit(xs, ys):
    """Least-squares slope of log y against log x."""
    pts = [(math.log(x), math.log(y)) for x, y in zip(xs, ys) if y > 0]
    if len(pts) < 2:
        return None
    n = len(pts)
    mx = sum(p[0] for p in pts) / n
    my = sum(p[1] for p in pts) / n
    num = sum((p[0] - mx) * (p[1] - my) for p in pts)
    den = sum((p[0] - mx) ** 2 for p in pts)
    return num / den if den else None


def sweep(rule, word, q, R, ks, pin, max_states):
    rows = []
    for k in ks:
        P = Params(rule=rule, right_depth=R, left_depth=k,
                   period_word=tuple(int(c) for c in word), diff_q=q)
        res = R1.tail_language(P, pin, max_states)
        if res.get("capped"):
            rows.append({"rule": rule, "w": word, "R": R, "k": k,
                         "capped": True})
            print(json.dumps(rows[-1]), flush=True)
            continue
        raw = res.get("raw_states", 0)
        row = {
            "rule": rule, "w": word, "q": q, "R": R, "k": k, "pin": pin,
            "x_min": P.x_min,
            "empty": res.get("empty", False),
            "raw_states": raw,
            "tail_nodes": res.get("tail_nodes"),
            "bisim_classes": res.get("bisim_classes"),
            "raw_over_alphabet": round(raw / (4 ** (R + abs(P.x_min))), 3),
        }
        rows.append(row)
        print(json.dumps(row), flush=True)
    return rows


def summarise(rows, fit_from=2):
    ok = [r for r in rows if not r.get("capped") and not r.get("empty")
          and r["k"] >= fit_from and r.get("bisim_classes")]
    if len(ok) < 2:
        return {"exponent": None, "n_points": len(ok)}
    ks = [r["k"] for r in ok]
    cs = [r["bisim_classes"] for r in ok]
    ratios = [round(cs[i + 1] / cs[i], 3) for i in range(len(cs) - 1)]
    return {"exponent": round(loglog_fit(ks, cs), 3), "n_points": len(ok),
            "ks": ks, "bisim_classes": cs, "successive_ratios": ratios}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("-R", type=int, default=2)
    ap.add_argument("--kmin", type=int, default=1)
    ap.add_argument("--kmax", type=int, default=6)
    ap.add_argument("--max-states", type=int, default=3_000_000)
    ap.add_argument("--out", default=None)
    args = ap.parse_args()
    ks = list(range(args.kmin, args.kmax + 1))

    out = {"args": vars(args), "sweeps": {}, "fits": {}}
    cases = [
        ("rule30_p2_plain", 30, "01", 1, False),
        ("rule30_p2_pin", 30, "01", 1, True),
        ("rule90_control_plain", 90, "0", 1, False),
    ]
    for name, rule, w, q, pin in cases:
        print(f"--- {name} ---", flush=True)
        rows = sweep(rule, w, q, args.R, ks, pin, args.max_states)
        out["sweeps"][name] = rows
        out["fits"][name] = summarise(rows)
        print(f"FIT {name}: {json.dumps(out['fits'][name])}", flush=True)

    path = args.out or f"k_language_sweep_R{args.R}.json"
    with open(path, "w") as f:
        json.dump(out, f, indent=1)
    print("written", path)


if __name__ == "__main__":
    main()
