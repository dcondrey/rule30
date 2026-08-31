"""SMT checks for the finite Boolean schemas used by the zero-tail proof.

This is not a substitute for the mathematical inductions in the paper.  It
asks Z3 for a counterexample to every local Boolean implication on which those
inductions depend: left permutivity, the C_m boundary cases, the zero- and
one-trace checkerboards, the Rule 30 OR latch, and the Rule 90 control.  Every
negated obligation must be UNSAT.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class ObligationResult:
    name: str
    solver_result: str


def build_certificate() -> dict[str, object]:
    try:
        from z3 import Bool, BoolVal, Not, Or, Solver, Xor
    except ModuleNotFoundError as error:
        raise RuntimeError(
            "z3-solver is required for this optional certificate"
        ) from error

    def rule30(left, center, right):
        return Xor(left, Or(center, right))

    def prove(name: str, proposition) -> ObligationResult:
        solver = Solver()
        solver.add(Not(proposition))
        result = str(solver.check())
        if result != "unsat":
            raise AssertionError(f"proof obligation {name!r} is {result}, not unsat")
        return ObligationResult(name, result)

    false = BoolVal(False)
    true = BoolVal(True)
    center = Bool("center")
    right = Bool("right")
    parity = Bool("parity")
    tail = Bool("tail")

    obligations = [
        prove(
            "rule30_left_permutive",
            rule30(false, center, right) != rule30(true, center, right),
        ),
        prove("c_m_gt_one_center_zero", rule30(false, false, false) == false),
        prove("c_m_right_zero_interior", rule30(false, false, false) == false),
        prove("c_m_right_front_moves_inward", rule30(false, false, true) == true),
        prove("c_m_left_zero_interior", rule30(false, false, false) == false),
        prove("c_m_left_front_moves_inward", rule30(true, false, false) == true),
        prove(
            "c_m_left_boundary_parity",
            rule30(Not(parity), true, false) == parity,
        ),
        prove(
            "c_m_alternating_tail",
            rule30(Not(parity), parity, Not(parity)) == parity,
        ),
        prove(
            "c_m_alternating_tail_boundary",
            rule30(Not(parity), parity, true) == parity,
        ),
        prove("c_1_center_zero", rule30(true, false, true) == false),
        prove("c_1_first_left_cell_fixed", rule30(false, true, false) == true),
        prove("c_1_right_or_latch", rule30(false, true, tail) == true),
        prove("one_trace_center_fixed", rule30(false, true, tail) == true),
        prove("one_trace_even_left_cell_fixed", rule30(false, true, false) == true),
        prove("one_trace_odd_left_cell_fixed", rule30(true, false, true) == false),
        prove("rule90_symmetric_center_control", Xor(tail, tail) == false),
        prove("prefix_or_odd_after_latch", Or(true, tail) == true),
        prove("prefix_or_even_after_latch", tail & Not(true) == false),
    ]
    return {
        "schema": "crosstalk.rule30.zero-tail-local-smt.v1",
        "status": "PASS",
        "interpretation": (
            "All finite Boolean schemas are UNSAT under negation; the paper's "
            "explicit inductions supply the unbounded argument."
        ),
        "obligations": [asdict(item) for item in obligations],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    report = build_certificate()
    print(json.dumps(report, indent=2, sort_keys=args.json))


if __name__ == "__main__":
    main()
