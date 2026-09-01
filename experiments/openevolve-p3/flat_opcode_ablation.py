"""Flat-opcode ablation of the fuel cost model.

Runs the pre-registration in PREREG-flat-opcode-ablation.md.  The flat model is
the word model with both size primitives pinned to 1, i.e. O(1) charge per
operation regardless of operand width -- what a bytecode-instruction counter
measures.  Nothing in fuel.py, evaluator_fuel.py or PREREGISTRATION.md is
modified; the primitives are rebound on the module object for the duration of
the run and restored afterwards.

Usage:  uv run python flat_opcode_ablation.py
"""

import json
import math
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
import fuel  # noqa: E402

CANDIDATES = {
    "a_correct": "sanity_candidates/candidate_a_correct.py",
    "c_bitpacked": "sanity_candidates/candidate_c_bitpacked.py",
}
NS = [125, 250, 500, 1000, 2000, 4000]
BAND = 0.3
TARGET = 2.0


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


def measure(label, rel):
    fs = [fuel.measure_fuel(str(HERE / rel), n)[0] for n in NS]
    ws = windows(NS, fs)
    return {"ns": NS, "fuels": fs, "window_exponents": ws, "tail": ws[-1]["slope"]}


if __name__ == "__main__":
    out = {}

    # Reference arm: the word model as shipped, so both arms come from one process.
    for label, rel in CANDIDATES.items():
        out[f"{label}@word30"] = measure(label, rel)

    # Ablation arm: O(1) per operation, operand size ignored.
    orig_bits, orig_elems = fuel._bits, fuel._elems
    fuel._bits = lambda x: 1
    fuel._elems = lambda x: 1
    try:
        for label, rel in CANDIDATES.items():
            out[f"{label}@flat"] = measure(label, rel)
    finally:
        fuel._bits, fuel._elems = orig_bits, orig_elems

    for key in sorted(out):
        print(f"{key}")
        for w in out[key]["window_exponents"]:
            print(f"    {w['from']:>5} -> {w['to']:<5} slope={w['slope']:.5f}")
        print(f"    tail={out[key]['tail']:.5f}")

    # Verdict, per the pre-registration.  The kill fires only if BOTH candidates
    # land inside the band under the flat model.
    inside = {
        label: abs(out[f"{label}@flat"]["tail"] - TARGET) <= BAND
        for label in CANDIDATES
    }
    n_inside = sum(inside.values())
    if n_inside == len(CANDIDATES):
        verdict = "KILL FIRED: flat opcode counter recovers both exponents"
    elif n_inside == 0:
        verdict = "STRONG OUTCOME: flat opcode counter misses both exponents"
    else:
        verdict = "AMBIGUOUS: flat opcode counter recovers one candidate, not the other"
    print(f"\n{verdict}")
    for label, ok in sorted(inside.items()):
        d = out[f"{label}@flat"]["tail"] - TARGET
        print(f"    {label}: flat tail={out[f'{label}@flat']['tail']:.5f} "
              f"(delta {d:+.5f}, band +/-{BAND}) -> {'inside' if ok else 'outside'}")

    out["_verdict"] = verdict
    out["_inside_band"] = inside
    print("\n" + json.dumps(out, indent=2))
