"""Determinism check for the fuel instrument.

Runs each sanity candidate's fuel measurement in a SEPARATE PROCESS, N
times, and asserts the counts are bit-identical. Separate processes matter:
same-process repeats cannot fail on hash-seed-dependent iteration order or
on module-level cache state, so they would not test what needs testing.
PYTHONHASHSEED is left at its default (randomised per process) on purpose.

Usage:  determinism_check_fuel.py [repeats]
        determinism_check_fuel.py --worker <path> <n> ...   (internal)
"""
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).parent
PY = sys.executable

CANDIDATES = {
    "a_correct": "sanity_candidates/candidate_a_correct.py",
    "c_bitpacked": "sanity_candidates/candidate_c_bitpacked.py",
    "seed_initial_program": "initial_program.py",
}


def worker(path, ns):
    sys.path.insert(0, str(HERE))
    import fuel
    out = {}
    for n in ns:
        f, v, setup = fuel.measure_fuel(path, n)
        out[str(n)] = [f, v, setup]
    print(json.dumps(out))


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--worker":
        worker(sys.argv[2], [int(x) for x in sys.argv[3:]])
        sys.exit(0)

    repeats = int(sys.argv[1]) if len(sys.argv) > 1 else 3
    ns = [250, 500, 1000, 2000, 4000]
    all_ok = True
    for label, rel in CANDIDATES.items():
        path = str(HERE / rel)
        runs = []
        for _ in range(repeats):
            p = subprocess.run(
                [PY, str(HERE / "determinism_check_fuel.py"), "--worker", path]
                + [str(n) for n in ns],
                capture_output=True, text=True, check=True,
            )
            runs.append(json.loads(p.stdout))
        identical = all(r == runs[0] for r in runs)
        all_ok &= identical
        print(f"{label}: {repeats} separate processes, bit-identical = {identical}")
        for n in ns:
            print(f"    n={n:>5}  fuel={runs[0][str(n)][0]:>14,}  c(n)={runs[0][str(n)][1]}  "
                  f"distinct values across runs = {len({tuple(r[str(n)]) for r in runs})}")
        if not identical:
            print("    RUNS:", json.dumps(runs, indent=2))
    print("\nALL BIT-IDENTICAL" if all_ok else "\nNON-DETERMINISM DETECTED")
    sys.exit(0 if all_ok else 1)
