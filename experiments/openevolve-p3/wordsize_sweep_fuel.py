"""Word-size invariance sweep for the fuel instrument.

Backs section 5 of RESULTS-openevolve-p3-fuel.md with a saved artifact.
WORD_BITS is a module constant in fuel.py; this rebinds it and re-measures
candidates (a) and (c) over the same ladder at each word size. Adjacent-window
slopes use the same formula as evaluator_fuel.measure_scaling_fuel.

Usage:  wordsize_sweep_fuel.py
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
WORD_SIZES = [30, 64]


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


if __name__ == "__main__":
    out = {}
    for wb in WORD_SIZES:
        fuel.WORD_BITS = wb
        for label, rel in CANDIDATES.items():
            path = str(HERE / rel)
            fs = [fuel.measure_fuel(path, n)[0] for n in NS]
            out[f"{label}@{wb}"] = {
                "word_bits": wb,
                "ns": NS,
                "fuels": fs,
                "window_exponents": windows(NS, fs),
            }
            print(f"{label} @ WORD_BITS={wb}")
            for w in out[f"{label}@{wb}"]["window_exponents"]:
                print(f"    {w['from']:>5} -> {w['to']:<5} slope={w['slope']:.5f}")
    print(json.dumps(out, indent=2))
