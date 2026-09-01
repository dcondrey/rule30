"""Run the evaluator against the sanity_candidates/ and print results.
This is the "prove the evaluator works" step from the task brief: (a)
correct baseline must score the flat credit, (b) deliberately wrong must
score exactly 0.0, (c) bit-packed same-exponent must be recognized correct
but NOT get exponent-improvement credit. (d) is a bonus lookup-table cheat
attempt, also expected to score 0.0."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from evaluator import evaluate

CANDIDATES = [
    ("a_correct (expect: correct, flat ~0.2 credit)", "sanity_candidates/candidate_a_correct.py"),
    ("b_wrong (expect: 0.0)", "sanity_candidates/candidate_b_wrong.py"),
    ("c_bitpacked (expect: correct, flat ~0.2 credit, NOT exponent-band)", "sanity_candidates/candidate_c_bitpacked.py"),
    ("d_lookup_table [bonus] (expect: 0.0)", "sanity_candidates/candidate_d_lookup_table.py"),
]

for label, path in CANDIDATES:
    print(f"\n=== {label} ===")
    result = evaluate(str(Path(__file__).parent / path))
    print("metrics:", result.metrics)
    print("artifacts:", result.artifacts)
