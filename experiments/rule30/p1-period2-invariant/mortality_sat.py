#!/usr/bin/env python3
"""Exact variable-seed CNF for hard-core Gray-OR mortality.

``M(n,H)`` is SAT iff a hard-core rho seed of length ``n`` survives at least
``H`` forced post-seed macrosteps.  The encoding is a Tseitin expansion of
the shallow-to-deep frontier recurrence, not a truth table of precomputed
seed outcomes.
"""

from __future__ import annotations

import argparse
import json
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from pysat.solvers import Solver

from bilateral_hardcore import hard_core_survival
from verify_drup import check_proof


@dataclass(frozen=True)
class BitState:
    T: int
    A: tuple[int, ...]
    B: tuple[int, ...]


@dataclass
class Instance:
    n: int
    horizon: int
    clauses: list[list[int]]
    variables: int
    seed_literals: list[int]
    roles: dict[int, str]


class Encoder:
    def __init__(self) -> None:
        self.clauses: list[list[int]] = []
        self.roles: dict[int, str] = {}
        self.top = 0
        self.step_number = 0
        self.zero = self.new("constant.0")
        self.one = self.new("constant.1")
        self.add(-self.zero)
        self.add(self.one)

    def new(self, role: str) -> int:
        self.top += 1
        self.roles[self.top] = role
        return self.top

    def add(self, *literals: int) -> None:
        self.clauses.append(list(literals))

    def or_gate(self, left: int, right: int, role: str) -> int:
        output = self.new(role)
        self.add(-left, output)
        self.add(-right, output)
        self.add(left, right, -output)
        return output

    def xor_gate(self, left: int, right: int, role: str) -> int:
        output = self.new(role)
        self.add(-left, -right, -output)
        self.add(left, right, -output)
        self.add(left, -right, output)
        self.add(-left, right, output)
        return output

    def wf_step(self, state: BitState, value: int, label: str) -> BitState:
        """Tseitin-encode exactly ``carry_transducer.wf_step``."""
        assert state.T == len(state.A)
        assert len(state.B) == max(0, state.T - 1)
        step = self.step_number
        self.step_number += 1
        current = value
        word = [current]
        for j in range(1, state.T + 1):
            a = state.A[j - 1]
            if j == 1:
                b = self.one if ((state.T - 1) & 1) else self.zero
            else:
                b = state.B[j - 2]
            joined = self.or_gate(a, b, f"step.{step}.{label}.or.{j}")
            current = self.xor_gate(
                current, joined, f"step.{step}.{label}.frontier.{j}"
            )
            word.append(current)
        return BitState(state.T + 1, tuple(word), state.A)


def build_instance(
    n: int,
    horizon: int,
    *,
    constrain_deep: bool = True,
    constrain_hard_core: bool = True,
) -> Instance:
    if n < 1 or horizon < 0:
        raise ValueError("require n >= 1 and horizon >= 0")
    encoder = Encoder()
    rho = [encoder.new(f"seed.rho.{index}") for index in range(n)]
    if constrain_hard_core:
        for left, right in zip(rho, rho[1:]):
            encoder.add(-left, -right)

    state = BitState(0, (), ())
    for index, bit in enumerate(rho):
        state = encoder.wf_step(state, -bit, f"seed.{index}.zero")
        state = encoder.wf_step(state, encoder.one, f"seed.{index}.pin")

    previous_rho = rho[-1]
    for follow in range(horizon):
        feed = encoder.new(f"follow.{follow}.zero-feed")
        middle = encoder.wf_step(state, feed, f"follow.{follow}.zero")
        # The forced rho is NOT feed.  no-11 is therefore
        # NOT(previous_rho AND NOT(feed)).
        if constrain_hard_core:
            encoder.add(-previous_rho, feed)
        if constrain_deep:
            encoder.add(-middle.A[-1])

        following = encoder.wf_step(middle, encoder.one, f"follow.{follow}.pin")
        if constrain_deep:
            encoder.add(-following.A[-1])
        previous_rho = -feed
        state = following

    return Instance(n, horizon, encoder.clauses, encoder.top, rho, encoder.roles)


def solve(
    instance: Instance, *, solver_name: str = "cadical195", proof: bool = False
) -> tuple[bool, list[int] | None, list[str], dict[str, int | float]]:
    started = time.perf_counter()
    with Solver(
        name=solver_name,
        bootstrap_with=instance.clauses,
        with_proof=proof,
    ) as solver:
        satisfiable = solver.solve()
        model = solver.get_model() if satisfiable else None
        proof_lines = (solver.get_proof() or []) if proof else []
        stats = dict(solver.accum_stats())
    stats["seconds"] = time.perf_counter() - started
    return satisfiable, model, proof_lines, stats


def decode_seed(instance: Instance, model: Iterable[int]) -> int:
    positive = {literal for literal in model if literal > 0}
    return sum(
        (int(variable in positive) << index)
        for index, variable in enumerate(instance.seed_literals)
    )


def hard_core_seeds(n: int) -> Iterable[int]:
    """Generate exactly the Fibonacci many no-11 words, without 2**n scan."""
    def visit(index: int, previous: int, value: int) -> Iterable[int]:
        if index == n:
            yield value
            return
        yield from visit(index + 1, 0, value)
        if not previous:
            yield from visit(index + 1, 1, value | (1 << index))

    return visit(0, 0, 0)


def direct_maximum(n: int, cap: int) -> tuple[int, int, str]:
    best = (-1, 0, "")
    for seed in hard_core_seeds(n):
        survival, outcome, _ = hard_core_survival(seed, n, cap)
        candidate = (survival, -seed, outcome)
        if candidate > (best[0], -best[1], best[2]):
            best = (survival, seed, outcome)
    return best


def validate(max_n: int = 16) -> list[dict[str, object]]:
    records: list[dict[str, object]] = []
    for n in range(1, max_n + 1):
        maximum, witness, outcome = direct_maximum(n, 128)
        for horizon in range(maximum + 2):
            instance = build_instance(n, horizon)
            sat, model, _, _ = solve(instance)
            expected = horizon <= maximum
            if sat != expected:
                raise AssertionError(
                    f"threshold mismatch n={n} H={horizon}: SAT={sat}, max={maximum}"
                )
            decoded = None
            if sat:
                assert model is not None
                decoded = decode_seed(instance, model)
                survived, _, _ = hard_core_survival(decoded, n, max(128, horizon))
                if survived < horizon:
                    raise AssertionError(
                        f"model replay failed n={n} H={horizon} seed={decoded:#x}"
                    )
        records.append(
            {
                "n": n,
                "maximum": maximum,
                "first_witness": witness,
                "death": outcome,
                "threshold_checks": maximum + 2,
            }
        )
        print(
            f"validate n={n:2d}: max={maximum:2d}, "
            f"SAT through H={maximum}, UNSAT at H={maximum + 1} PASS"
        )

    # Negative control: once the finite-left/deep-output constraints are
    # dropped, arbitrary feeds can maintain a hard-core continuation.
    control = build_instance(max_n, 2 * max_n + 2, constrain_deep=False)
    sat, model, _, _ = solve(control)
    if not sat or model is None:
        raise AssertionError("dropped-deep-boundary control unexpectedly UNSAT")
    print("dropped deep-left constraints: SAT PASS")
    return records


def direct_sweep(max_n: int, cap: int = 512) -> list[dict[str, object]]:
    records: list[dict[str, object]] = []
    for n in range(1, max_n + 1):
        maximum, witness, outcome = direct_maximum(n, cap)
        record = {
            "n": n,
            "maximum": maximum,
            "witness": witness,
            "death": outcome,
            "cap": cap,
        }
        records.append(record)
        print(
            f"direct n={n:2d}: max={maximum:2d}, witness={witness:#x}, "
            f"death={outcome}"
        )
        if outcome == "cap":
            break
    return records


def threshold_sweep(max_n: int, proof_dir: Path) -> list[dict[str, object]]:
    """Exploratory minimal-horizon certificates after primary proof blow-up.

    An UNSAT proof for M(n,m+1) also proves the registered M(n,2n+2)
    whenever m+1 <= 2n+2, because the latter contains the former as its
    exact prefix plus additional clauses.
    """
    proof_dir.mkdir(parents=True, exist_ok=True)
    records: list[dict[str, object]] = []
    for n in range(1, max_n + 1):
        maximum, witness, outcome = direct_maximum(n, 512)
        if outcome == "cap":
            raise AssertionError(f"continuation cap reached at n={n}, seed={witness:#x}")
        horizon = maximum + 1
        instance = build_instance(n, horizon)
        sat, model, proof_lines, stats = solve(
            instance, solver_name="glucose4", proof=True
        )
        if sat:
            decoded = decode_seed(instance, model or [])
            raise AssertionError(
                f"threshold formula unexpectedly SAT n={n} H={horizon} seed={decoded:#x}"
            )
        cnf_path = proof_dir / f"threshold-n{n:02d}-h{horizon:02d}.cnf"
        proof_path = proof_dir / f"threshold-n{n:02d}-h{horizon:02d}.drup"
        write_dimacs(instance, cnf_path)
        write_proof(proof_lines, proof_path)
        checked = check_proof(
            [tuple(clause) for clause in instance.clauses], proof_lines
        )
        record: dict[str, object] = {
            "n": n,
            "maximum": maximum,
            "witness": witness,
            "death": outcome,
            "threshold": horizon,
            "implies_primary": horizon <= 2 * n + 2,
            "variables": instance.variables,
            "clauses": len(instance.clauses),
            "proof_lines_raw": len(proof_lines),
            "proof_check": checked,
            **stats,
        }
        records.append(record)
        print(
            f"threshold n={n:2d}: max={maximum:2d} witness={witness:#x}; "
            f"UNSAT H={horizon} checked, proof={len(proof_lines)}, "
            f"seconds={stats['seconds']:.3f}"
        )
    return records


def write_dimacs(instance: Instance, path: Path) -> None:
    lines = [f"p cnf {instance.variables} {len(instance.clauses)}"]
    lines.extend(" ".join(map(str, clause)) + " 0" for clause in instance.clauses)
    path.write_text("\n".join(lines) + "\n")


def write_proof(lines: list[str], path: Path) -> None:
    path.write_text("\n".join(lines) + "\n")


def primary_sweep(max_n: int, proof_dir: Path) -> list[dict[str, object]]:
    proof_dir.mkdir(parents=True, exist_ok=True)
    records: list[dict[str, object]] = []
    for n in range(1, max_n + 1):
        horizon = 2 * n + 2
        instance = build_instance(n, horizon)
        sat, model, proof_lines, stats = solve(
            instance, solver_name="glucose4", proof=True
        )
        seed = decode_seed(instance, model) if sat and model is not None else None
        checked: dict[str, int | bool] | None = None
        if not sat:
            cnf_path = proof_dir / f"mortality-n{n:02d}-h{horizon:02d}.cnf"
            proof_path = proof_dir / f"mortality-n{n:02d}-h{horizon:02d}.drup"
            write_dimacs(instance, cnf_path)
            write_proof(proof_lines, proof_path)
            checked = check_proof(
                [tuple(clause) for clause in instance.clauses], proof_lines
            )
        record: dict[str, object] = {
            "n": n,
            "horizon": horizon,
            "sat": sat,
            "seed": seed,
            "variables": instance.variables,
            "clauses": len(instance.clauses),
            "proof_lines_raw": len(proof_lines),
            "proof_check": checked,
            **stats,
        }
        records.append(record)
        print(
            f"primary n={n:2d} H={horizon:2d}: "
            f"{'SAT seed=' + hex(seed or 0) if sat else 'UNSAT checked'}; "
            f"vars={instance.variables}, clauses={len(instance.clauses)}, "
            f"proof={len(proof_lines)}, seconds={stats['seconds']:.3f}"
        )
    return records


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--validate", action="store_true")
    parser.add_argument("--direct", action="store_true")
    parser.add_argument("--sweep", action="store_true")
    parser.add_argument("--threshold-sweep", action="store_true")
    parser.add_argument("--max-validate", type=int, default=16)
    parser.add_argument("--max-n", type=int, default=24)
    parser.add_argument("--proof-dir", type=Path, default=Path("mortality-proofs"))
    parser.add_argument("--out", type=Path)
    args = parser.parse_args()
    if not any((args.validate, args.direct, args.sweep, args.threshold_sweep)):
        parser.error("choose --validate, --direct, --sweep, and/or --threshold-sweep")

    output: dict[str, object] = {}
    if args.validate:
        output["validation"] = validate(args.max_validate)
    if args.direct:
        output["direct"] = direct_sweep(args.max_n)
    if args.sweep:
        output["primary"] = primary_sweep(args.max_n, args.proof_dir)
    if args.threshold_sweep:
        output["threshold"] = threshold_sweep(args.max_n, args.proof_dir)
    if args.out:
        args.out.write_text(json.dumps(output, indent=2, sort_keys=True) + "\n")
        print(f"wrote {args.out}")


if __name__ == "__main__":
    main()
