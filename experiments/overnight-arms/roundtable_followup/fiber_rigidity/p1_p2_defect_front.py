"""Reuse the repo's existing left-permutive inverse machinery
(experiments/rule30/inverse_trace_probe.py, already-existing code, not new
here) to check whether a single-bit right-boundary defect against a p=1 or
p=2 periodic centre trace ever gets absorbed as it propagates left for Rule
30, and never for Rule 90 (rule90_screen.py in this directory).

This is the "attempt the mechanism" step: the panel's proposal wants
Rule-30-specific interface creation/conservation from the OR nonlinearity.
What actually exists, and what this reproduces, is the already-published pin
law (PATH.md section 0.5, RESULTS-eventual-period.md): a single defect is
erased the step it meets a centre value of 1 (the OR saturates) and survives
unattenuated forever whenever it only ever meets centre value 0. This holds
identically at p=1 (constant centre) and p=2 (period-01 centre); period does
not change the erasure law at all, only how often a 1 comes up in the trace.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "rule30"))

from inverse_trace_probe import rotated_defect_front  # noqa: E402


def main() -> None:
    cases = [
        ("p=1 constant-0, perturb t=64 (centre=0 there)", (0,), 64),
        ("p=1 constant-1, perturb t=64 (centre=1 there)", (1,), 64),
        ("p=2 word=01, perturb t=64 (centre=0 there)", (0, 1), 64),
        ("p=2 word=01, perturb t=65 (centre=1 there)", (0, 1), 65),
    ]
    for label, word, pert in cases:
        front = rotated_defect_front(word, pert, 40)
        erased = front[0] is None
        print(f"{label}: erased_immediately={erased}  front[:6]={front[:6]}")


if __name__ == "__main__":
    main()
