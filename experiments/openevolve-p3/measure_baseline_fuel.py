"""Measure the fuel-scaling baseline from initial_program.py and write
baseline_fuel.json (the fuel analogue of baseline_exponent.json).

`baseline_exponent.json` is NOT touched -- the wall-clock baseline stays
exactly as pre-registered.
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))

import evaluator_fuel as ef  # noqa: E402

OUT = HERE / "baseline_fuel.json"

if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else str(HERE / "initial_program.py")
    scaling = ef.measure_scaling_fuel(target)
    if not scaling["correct"]:
        print("BASELINE PROGRAM FAILED CORRECTNESS:", scaling["correctness_detail"])
        sys.exit(1)
    record = {
        "source": Path(target).name,
        "instrument": "fuel.py word-RAM counter",
        "word_bits": __import__("fuel").WORD_BITS,
        "scaling_ns_config": ef.CFG["scaling_ns"],
        "usable_ns": scaling["usable_ns"],
        "fuels": scaling["fuels"],
        "setup_fuels": scaling.get("setup_fuels"),
        "tail_exponent": scaling["tail_exponent"],
        "exponent": scaling["exponent"],
        "r2": scaling["r2"],
        "tail_consistency": scaling.get("tail_consistency"),
        "window_exponents": scaling.get("window_exponents"),
        "dropped": scaling["dropped"],
        "repeats": 1,
    }
    data = json.loads(OUT.read_text()) if OUT.exists() else {}
    data[ef.PROFILE] = record
    OUT.write_text(json.dumps(data, indent=2) + "\n")
    print(json.dumps({ef.PROFILE: record}, indent=2))
