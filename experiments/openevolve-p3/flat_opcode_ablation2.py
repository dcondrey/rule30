"""Amended flat-opcode ablation: adds a second discriminating candidate.

Runs the AMENDMENT section of PREREG-flat-opcode-ablation.md.  Differences from
flat_opcode_ablation.py:

  * adds candidate (e), correct, wide-operand, true exponent 3;
  * compares each candidate against ITS OWN true exponent, not against 2.0 --
    the original rule would have scored the flat model's reading of (e) as
    inside the band while it was wrong by a full exponent-unit;
  * marks which candidates can discriminate at all, and decides the verdict on
    those only;
  * checks the WORD model too, so an instrument that fails to recover a known
    exponent away from 2 is caught rather than assumed away.

Nothing in fuel.py, evaluator_fuel.py or PREREGISTRATION.md is modified; the
size primitives are rebound on the module object and restored afterwards.

Usage:  uv run python flat_opcode_ablation2.py
"""

import json
import math
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
import fuel  # noqa: E402

FULL_LADDER = [125, 250, 500, 1000, 2000, 4000]
SHORT_LADDER = [125, 250, 500, 1000]  # Theta(n^3) is too slow past this.

CANDIDATES = {
    # label: (path, true exponent, discriminating?, ladder)
    "a_correct": ("sanity_candidates/candidate_a_correct.py", 2.0, False, FULL_LADDER),
    "c_bitpacked": ("sanity_candidates/candidate_c_bitpacked.py", 2.0, True, FULL_LADDER),
    "e_cubic": ("sanity_candidates/candidate_e_cubic.py", 3.0, True, SHORT_LADDER),
}
BAND = 0.3


def windows(ns, fs):
    return [
        {
            "from": ns[i - 1],
            "to": ns[i],
            "slope": (math.log(fs[i]) - math.log(fs[i - 1]))
            / (math.log(ns[i]) - math.log(ns[i - 1])),
        }
        for i in range(1, len(ns))
    ]


def measure(rel, ladder):
    fs = [fuel.measure_fuel(str(HERE / rel), n)[0] for n in ladder]
    ws = windows(ladder, fs)
    return {"ns": ladder, "fuels": fs, "window_exponents": ws, "tail": ws[-1]["slope"]}


def rising(ws):
    """True if adjacent-window slopes trend upward, i.e. converging from below."""
    return all(
        ws[i]["slope"] >= ws[i - 1]["slope"] - 1e-9 for i in range(1, len(ws))
    )


if __name__ == "__main__":
    out = {}

    for label, (rel, _, _, ladder) in CANDIDATES.items():
        out[f"{label}@word30"] = measure(rel, ladder)

    orig_bits, orig_elems = fuel._bits, fuel._elems
    fuel._bits = lambda x: 1
    fuel._elems = lambda x: 1
    try:
        for label, (rel, _, _, ladder) in CANDIDATES.items():
            out[f"{label}@flat"] = measure(rel, ladder)
    finally:
        fuel._bits, fuel._elems = orig_bits, orig_elems

    for key in sorted(out):
        print(key)
        for w in out[key]["window_exponents"]:
            print(f"    {w['from']:>5} -> {w['to']:<5} slope={w['slope']:.5f}")
        print(f"    tail={out[key]['tail']:.5f}")

    print("\n--- verdict, per the AMENDMENT in PREREG-flat-opcode-ablation.md ---")
    inside = {}
    for label, (_, true_exp, discr, _) in CANDIDATES.items():
        for arm in ("word30", "flat"):
            t = out[f"{label}@{arm}"]["tail"]
            ok = abs(t - true_exp) <= BAND
            inside[f"{label}@{arm}"] = ok
            mark = "discriminating" if discr else "NON-discriminating"
            print(f"{label}@{arm}: tail={t:.5f} vs true {true_exp} "
                  f"(delta {t - true_exp:+.5f}) -> {'inside' if ok else 'OUTSIDE'} "
                  f"[{mark}]")

    discriminators = [k for k, v in CANDIDATES.items() if v[2]]

    # New kill: the WORD model must recover an exponent away from 2.
    e_word = out["e_cubic@word30"]
    e_rising = rising(e_word["window_exponents"])
    word_fails_e = (not inside["e_cubic@word30"]) and (
        e_word["tail"] < 2.7 or not e_rising
    )

    flat_inside_all = all(inside[f"{k}@flat"] for k in discriminators)
    flat_outside_all = all(not inside[f"{k}@flat"] for k in discriminators)
    word_inside_all = all(inside[f"{k}@word30"] for k in CANDIDATES)

    if word_fails_e:
        verdict = ("NEW KILL FIRED: the WORD model does not recover exponent 3 on (e) "
                   f"(tail={e_word['tail']:.5f}, slopes rising={e_rising}). "
                   "This is a defect in fuel.py, not in the flat comparison, and puts "
                   "register row 92's 'instrument validated' status in question.")
    elif flat_inside_all:
        verdict = "KILL FIRED: flat opcode counter recovers every discriminating candidate"
    elif flat_outside_all and word_inside_all:
        verdict = ("STRONG OUTCOME: word model correct at both exponents 2 and 3; "
                   "flat model wrong on every discriminating candidate")
    else:
        verdict = "AMBIGUOUS"

    print(f"\n{verdict}")
    print(f"(e) word-model adjacent slopes rising toward 3: {e_rising}")

    out["_verdict"] = verdict
    out["_inside_band"] = inside
    out["_e_word_slopes_rising"] = e_rising
    print("\n" + json.dumps(out, indent=2))
