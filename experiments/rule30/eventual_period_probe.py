"""Exact bounded certificates for eventual-periodic Rule 30 center traces.

An eventually ``p``-periodic center trace from a finite configuration can be
shifted to a finite row ``y`` satisfying

    Tr_0(y) = Tr_0(F^p(y)).

Conversely, this same-orbit trace collision makes ``Tr_0(y)`` ``p``-periodic
from time zero.  The unbounded exclusion of such collisions is open.  This
module encodes bounded instances symbolically: the initial row is supported in
``[-w,w]``, every Rule 30 spacetime cell is a Boolean variable constrained by
the exact local rule, and period equalities are added incrementally.  An UNSAT
result is an exhaustive finite-radius certificate; a SAT result returns an
explicit row and independently checked trace.

Finite certificates are lemma generators and falsifiers.  They are not
evidence that the unbounded Rule 30 statement is true.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass
from typing import Iterable


RULE_30 = 30
RULE_90 = 90


def _eca_output(rule: int, left: int, center: int, right: int) -> int:
    neighborhood = (left << 2) | (center << 1) | right
    return rule >> neighborhood & 1


def direct_center_trace(
    rule: int,
    initial_offsets: Iterable[int],
    horizon: int,
) -> tuple[int, ...]:
    """Independently evolve a finite row and return its center trace."""
    if rule < 0 or rule > 255:
        raise ValueError("rule must be an ECA number")
    if rule & 1:
        raise ValueError("finite-set evolution requires a quiescent zero")
    if horizon < 0:
        raise ValueError("horizon must be non-negative")
    row = set(initial_offsets)
    trace: list[int] = []
    for _ in range(horizon + 1):
        trace.append(int(0 in row))
        if not row:
            continue
        next_row: set[int] = set()
        for position in range(min(row) - 1, max(row) + 2):
            output = _eca_output(
                rule,
                int(position - 1 in row),
                int(position in row),
                int(position + 1 in row),
            )
            if output:
                next_row.add(position)
        row = next_row
    return tuple(trace)


@dataclass(frozen=True)
class PeriodSearchCertificate:
    rule: int
    support_radius: int
    proposed_period: int
    require_nonconstant_word: bool
    exact_nonzero_rows_covered: int
    maximum_certified_periodic_horizon: int
    first_unsatisfiable_time: int | None
    irreducible_core_times: tuple[int, ...]
    extremal_witness_offsets: tuple[int, ...]
    extremal_witness_trace: tuple[int, ...]
    stopped_at_search_horizon: bool


def _load_z3():
    try:
        import z3
    except ModuleNotFoundError as error:
        raise RuntimeError(
            "z3-solver is required for the eventual-period certificate"
        ) from error
    return z3


def exact_period_search(
    rule: int,
    support_radius: int,
    period: int,
    search_horizon: int,
    *,
    require_nonconstant_word: bool = True,
) -> PeriodSearchCertificate:
    """Incrementally solve one exact finite-support periodicity instance.

    The returned horizon is the largest absolute time ``H`` for which a
    nonzero row can satisfy ``c(t)=c(t-period)`` at every
    ``period <= t <= H``.  When ``require_nonconstant_word`` is true, the first
    period block must contain both symbols.  If no conflict is reached by the
    caller's cap, the explicit witness is the only certified conclusion.
    """
    if rule not in (RULE_30, RULE_90):
        raise ValueError("the symbolic recurrence currently supports Rules 30 and 90")
    if support_radius < 1:
        raise ValueError("support_radius must be positive")
    if period < 1:
        raise ValueError("period must be positive")
    if require_nonconstant_word and period < 2:
        raise ValueError("a nonconstant period word requires period at least two")
    if search_horizon < period:
        raise ValueError("search_horizon must be at least period")

    z3 = _load_z3()
    false = z3.BoolVal(False)
    solver = z3.Solver()

    rows: list[dict[int, object]] = [
        {
            position: z3.Bool(f"x_0_{position:+d}")
            for position in range(-support_radius, support_radius + 1)
        }
    ]
    solver.add(z3.Or(*rows[0].values()))

    def cell(row: dict[int, object], position: int):
        return row.get(position, false)

    for time in range(search_horizon):
        prior = rows[-1]
        current: dict[int, object] = {}
        extent = support_radius + time + 1
        for position in range(-extent, extent + 1):
            value = z3.Bool(f"x_{time + 1}_{position:+d}")
            left = cell(prior, position - 1)
            center = cell(prior, position)
            right = cell(prior, position + 1)
            if rule == RULE_30:
                update = z3.Xor(left, z3.Or(center, right))
            else:
                update = z3.Xor(left, right)
            solver.add(value == update)
            current[position] = value
        rows.append(current)

    centers = [cell(row, 0) for row in rows]
    if require_nonconstant_word:
        solver.add(z3.Or(*(centers[phase] != centers[0] for phase in range(1, period))))

    base_result = solver.check()
    if base_result != z3.sat:
        raise AssertionError("the unconstrained nonconstant period block is unexpectedly UNSAT")

    labels: list[object] = []
    label_times: dict[str, int] = {}
    last_model = solver.model()
    maximum = period - 1
    first_unsat: int | None = None
    core_times: tuple[int, ...] = ()

    for time in range(period, search_horizon + 1):
        label = z3.Bool(f"period_eq_{time}")
        labels.append(label)
        label_times[str(label)] = time
        solver.add(z3.Implies(label, centers[time] == centers[time - period]))
        result = solver.check(*labels)
        if result == z3.sat:
            maximum = time
            last_model = solver.model()
            continue
        if result != z3.unsat:
            raise AssertionError(f"unexpected solver result: {result}")

        first_unsat = time
        core = list(solver.unsat_core())
        # Greedy deletion makes the returned set inclusion-minimal.  It is not
        # claimed to have minimum cardinality.
        index = 0
        while index < len(core):
            trial = core[:index] + core[index + 1 :]
            if solver.check(*trial) == z3.unsat:
                core = trial
            else:
                index += 1
        core_times = tuple(sorted(label_times[str(item)] for item in core))
        break

    initial = rows[0]
    witness = tuple(
        position
        for position in range(-support_radius, support_radius + 1)
        if z3.is_true(last_model.eval(initial[position], model_completion=True))
    )
    witness_trace = direct_center_trace(rule, witness, maximum)
    if require_nonconstant_word and len(set(witness_trace[:period])) != 2:
        raise AssertionError("solver witness does not have a nonconstant period word")
    if any(
        witness_trace[time] != witness_trace[time - period]
        for time in range(period, maximum + 1)
    ):
        raise AssertionError("independent evolution rejected the solver witness")

    return PeriodSearchCertificate(
        rule=rule,
        support_radius=support_radius,
        proposed_period=period,
        require_nonconstant_word=require_nonconstant_word,
        exact_nonzero_rows_covered=(1 << (2 * support_radius + 1)) - 1,
        maximum_certified_periodic_horizon=maximum,
        first_unsatisfiable_time=first_unsat,
        irreducible_core_times=core_times,
        extremal_witness_offsets=witness,
        extremal_witness_trace=witness_trace,
        stopped_at_search_horizon=first_unsat is None,
    )


def build_report(
    max_radius: int,
    max_period: int,
    search_horizon: int,
) -> dict[str, object]:
    if max_radius < 1:
        raise ValueError("max_radius must be positive")
    if max_period < 2:
        raise ValueError("max_period must be at least two")
    certificates = [
        exact_period_search(RULE_30, radius, period, search_horizon)
        for period in range(2, max_period + 1)
        for radius in range(1, max_radius + 1)
    ]
    rule90 = exact_period_search(
        RULE_90,
        support_radius=1,
        period=1,
        search_horizon=search_horizon,
        require_nonconstant_word=False,
    )
    return {
        "status": "EXACT COMPUTATION",
        "reduction": (
            "An eventual period p is equivalent, after shifting to its tail, "
            "to Tr_0(y)=Tr_0(F^p(y)) for a nonzero finite row y."
        ),
        "scope_warning": (
            "Each UNSAT result excludes only its stated support radius and period; "
            "finite certificates do not prove the unbounded conjecture."
        ),
        "rule30_certificates": [asdict(item) for item in certificates],
        "rule90_constant_zero_control": asdict(rule90),
        "spending_usd": {"modal": 0, "model_providers": 0},
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-radius", type=int, default=6)
    parser.add_argument("--max-period", type=int, default=6)
    parser.add_argument("--search-horizon", type=int, default=32)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    report = build_report(args.max_radius, args.max_period, args.search_horizon)
    print(json.dumps(report, indent=2, sort_keys=args.json))


if __name__ == "__main__":
    main()
