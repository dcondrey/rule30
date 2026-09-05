#!/usr/bin/env python3
"""Resolution cores and exact cut interpolants for small diagonal CNFs.

For ``C(m,m+1)`` at m=4,5,6 this script writes:

* the original DIMACS formula and an independently RUP-checked DRUP proof;
* a deletion-irreducible subset of the original clauses and its own checked
  DRUP proof; and
* a minimum-clause CNF interpolant over the vertical-cut variables.

The interpolant is calculated from the exact projections ``R_H`` and ``S_H``
of the clean cut partition.  Thus it is a Craig interpolant for that
partition, although it is not claimed to be the particular syntactic
interpolant induced by Glucose's unlabelled DRUP trace.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from itertools import combinations
from pathlib import Path
from typing import Iterable

from pysat.card import CardEnc, EncType
from pysat.examples.rc2 import RC2
from pysat.formula import WCNF
from pysat.solvers import Solver

from core_interpolant_probe import accepting_cut, bit_mask, feed, reachable_cut
from core_mortality_sat import CoreInstance, build_core_instance
from verify_drup import check_proof


Clause = tuple[int, ...]
Cut = tuple[int, ...]
TemplateLiteral = tuple[int, int, int]
Template = tuple[TemplateLiteral, ...]


def write_dimacs(
    path: Path,
    variables: int,
    clauses: Iterable[Clause],
    roles: dict[int, str] | None = None,
) -> None:
    clauses = list(clauses)
    lines = ["c exact Rule 30 active-core diagonal CNF"]
    if roles:
        lines.extend(
            f"c var {variable} {roles[variable]}" for variable in sorted(roles)
        )
    lines.append(f"p cnf {variables} {len(clauses)}")
    lines.extend(" ".join(map(str, clause)) + " 0" for clause in clauses)
    path.write_text("\n".join(lines) + "\n")


def write_proof(path: Path, proof: list[str]) -> None:
    path.write_text("\n".join(proof) + "\n")


def checked_drup(clauses: list[Clause]) -> tuple[list[str], dict[str, int | bool]]:
    with Solver(
        name="glucose4",
        bootstrap_with=clauses,
        with_proof=True,
    ) as solver:
        assert not solver.solve()
        proof = solver.get_proof() or []
    check = check_proof(clauses, proof)
    return proof, check


def irreducible_clause_core(
    clauses: list[Clause], variables: int
) -> list[int]:
    """Return indices of a deletion-irreducible UNSAT clause subset."""

    selectors = list(range(variables + 1, variables + 1 + len(clauses)))
    guarded = [
        list(clause) + [-selector]
        for clause, selector in zip(clauses, selectors)
    ]
    with Solver(name="cadical195", bootstrap_with=guarded) as solver:
        assert not solver.solve(assumptions=selectors)
        initial = set(solver.get_core() or [])
        core = [selector for selector in selectors if selector in initial]
        index = 0
        while index < len(core):
            trial = core[:index] + core[index + 1 :]
            if not solver.solve(assumptions=trial):
                core = trial
            else:
                index += 1

        assert not solver.solve(assumptions=core)
        for index in range(len(core)):
            assert solver.solve(assumptions=core[:index] + core[index + 1 :])

    selector_to_index = {selector: index for index, selector in enumerate(selectors)}
    return [selector_to_index[selector] for selector in core]


def clause_satisfied(assignment: int, clause: Clause) -> bool:
    return any(
        bool(assignment & (1 << (abs(literal) - 1))) == (literal > 0)
        for literal in clause
    )


def prime_cut_clauses(
    reached: list[int], accepting: list[int], variables: int, cap: int = 6
) -> dict[Clause, int]:
    """Enumerate prime clauses valid on R and false on at least one S point."""

    clauses: dict[Clause, int] = {}
    for target in accepting:
        valid_supports: list[int] = []
        for width in range(1, cap + 1):
            for support in combinations(range(variables), width):
                mask = sum(1 << variable for variable in support)
                if any(previous & mask == previous for previous in valid_supports):
                    continue
                if not all((state ^ target) & mask for state in reached):
                    continue
                valid_supports.append(mask)
                clause = tuple(
                    -(variable + 1)
                    if target & (1 << variable)
                    else variable + 1
                    for variable in support
                )
                covered = sum(
                    1 << index
                    for index, state in enumerate(accepting)
                    if not (state ^ target) & mask
                )
                clauses[clause] = clauses.get(clause, 0) | covered
    return clauses


def minimum_cnf_interpolant(
    reached: list[int], accepting: list[int], variables: int
) -> tuple[list[tuple[Clause, int]], int]:
    candidates = sorted(
        prime_cut_clauses(reached, accepting, variables).items(),
        key=lambda item: (len(item[0]), item[0]),
    )
    formula = WCNF()
    for target in range(len(accepting)):
        covering = [
            index + 1
            for index, (_, covered) in enumerate(candidates)
            if covered & (1 << target)
        ]
        assert covering
        formula.append(covering)

    # Lexicographically minimize clause count and then total literal count.
    large = sum(len(clause) for clause, _ in candidates) + 1
    for index, (clause, _) in enumerate(candidates, start=1):
        formula.append([-index], weight=large + len(clause))
    with RC2(formula) as optimizer:
        model = set(optimizer.compute() or [])
    selected = [
        candidate
        for index, candidate in enumerate(candidates, start=1)
        if index in model
    ]

    # Independently prove that no interpolant using fewer candidate clauses
    # can cover S while remaining valid on R.
    hard = [
        [
            index + 1
            for index, (_, covered) in enumerate(candidates)
            if covered & (1 << target)
        ]
        for target in range(len(accepting))
    ]
    if len(selected) > 1:
        cardinality = CardEnc.atmost(
            lits=list(range(1, len(candidates) + 1)),
            bound=len(selected) - 1,
            top_id=len(candidates),
            encoding=EncType.seqcounter,
        )
        with Solver(
            name="cadical195",
            bootstrap_with=hard + cardinality.clauses,
        ) as solver:
            assert not solver.solve()

    assert all(
        all(clause_satisfied(state, clause) for clause, _ in selected)
        for state in reached
    )
    assert all(
        any(not clause_satisfied(state, clause) for clause, _ in selected)
        for state in accepting
    )
    return selected, len(candidates)


def literal_name(literal: int) -> str:
    bit = abs(literal) - 1
    position, component = divmod(bit, 2)
    name = f"{'h' if component == 0 else 'l'}_{position}"
    return name if literal > 0 else f"not {name}"


def clause_text(clause: Clause) -> str:
    return "(" + " or ".join(map(literal_name, clause)) + ")"


def normalized_template(clause: Clause) -> tuple[Template, int]:
    literals = []
    for literal in clause:
        bit = abs(literal) - 1
        position, component = divmod(bit, 2)
        literals.append((position, component, 1 if literal > 0 else -1))
    shift = min(position for position, _, _ in literals)
    return tuple(
        (position - shift, component, sign)
        for position, component, sign in literals
    ), shift


def template_text(template: Template, shift: str = "i") -> str:
    terms = []
    for offset, component, sign in template:
        subscript = shift if offset == 0 else f"{shift}+{offset}"
        name = f"{'h' if component == 0 else 'l'}_({subscript})"
        terms.append(name if sign > 0 else f"not {name}")
    return "(" + " or ".join(terms) + ")"


def template_satisfied(cut: Cut, template: Template, shift: int) -> bool:
    for offset, component, sign in template:
        state = cut[shift + offset]
        bit = (state >> 1) & 1 if component == 0 else state & 1
        if bool(bit) == (sign > 0):
            return True
    return False


def reachable_witnesses(horizon: int) -> dict[Cut, tuple[int, ...]]:
    witnesses: dict[Cut, tuple[int, ...]] = {(0,) * horizon: ()}
    frontier = {(0,) * horizon}
    for _ in range(max(0, horizon - 2)):
        following: set[Cut] = set()
        for cut in sorted(frontier):
            for symbol in range(4):
                successor = feed(cut, symbol)
                if successor not in witnesses:
                    witnesses[successor] = witnesses[cut] + (symbol,)
                    following.add(successor)
        frontier = following
    assert set(witnesses) == reachable_cut(horizon)
    return witnesses


def motif_audit(
    prime_by_horizon: dict[int, dict[Clause, int]], maximum_horizon: int = 12
) -> dict[str, object]:
    templates_by_horizon = {
        horizon: {normalized_template(clause)[0] for clause in clauses}
        for horizon, clauses in prime_by_horizon.items()
    }
    common = sorted(set.intersection(*templates_by_horizon.values()))
    witnesses_by_horizon = {
        horizon: reachable_witnesses(horizon)
        for horizon in range(5, maximum_horizon + 1)
    }
    records = []
    for template in common:
        span = max(offset for offset, _, _ in template)
        validity: dict[str, list[int]] = {}
        counterexamples: dict[str, list[dict[str, object]]] = {}
        for horizon, witnesses in witnesses_by_horizon.items():
            valid = []
            failed = []
            for shift in range(horizon - span):
                bad = [
                    (prefix, cut)
                    for cut, prefix in witnesses.items()
                    if not template_satisfied(cut, template, shift)
                ]
                if not bad:
                    valid.append(shift)
                    continue
                prefix, cut = min(bad, key=lambda item: (len(item[0]), item[0], item[1]))
                failed.append(
                    {
                        "shift": shift,
                        "prefix": "".join(map(str, prefix)) or "empty",
                        "cut": "".join(map(str, cut)),
                    }
                )
            validity[str(horizon)] = valid
            if horizon == 8:
                counterexamples[str(horizon)] = failed
        records.append(
            {
                "template": [list(literal) for literal in template],
                "formula": template_text(template),
                "valid_translations": validity,
                "h8_counterexamples": counterexamples.get("8", []),
            }
        )
    return {
        "common_prime_templates_h5_h7": records,
        "conclusion": (
            "All common translated prime-clause templates from H=5,6,7 "
            "have no valid translation at H=8."
        ),
    }


def file_digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def instance_artifacts(
    output: Path, length: int
) -> tuple[dict[str, object], dict[Clause, int]]:
    horizon = length + 1
    stem = f"c-m{length:02d}-h{horizon:02d}"
    instance: CoreInstance = build_core_instance(length, horizon)
    clauses = [tuple(clause) for clause in instance.encoder.clauses]

    proof, proof_check = checked_drup(clauses)
    core_indices = irreducible_clause_core(clauses, instance.encoder.top)
    core_clauses = [clauses[index] for index in core_indices]
    core_proof, core_proof_check = checked_drup(core_clauses)

    paths = {
        "cnf": output / f"{stem}.cnf",
        "drup": output / f"{stem}.drup",
        "core_cnf": output / f"{stem}-core.cnf",
        "core_drup": output / f"{stem}-core.drup",
        "interpolant": output / f"{stem}-interpolant.json",
    }
    write_dimacs(
        paths["cnf"],
        instance.encoder.top,
        clauses,
        instance.encoder.roles,
    )
    write_proof(paths["drup"], proof)
    write_dimacs(
        paths["core_cnf"],
        instance.encoder.top,
        core_clauses,
        instance.encoder.roles,
    )
    write_proof(paths["core_drup"], core_proof)

    reached = sorted(map(bit_mask, reachable_cut(horizon)))
    accepting = sorted(map(bit_mask, accepting_cut(horizon)))
    selected, candidate_count = minimum_cnf_interpolant(
        reached, accepting, 2 * horizon
    )
    all_prime = prime_cut_clauses(reached, accepting, 2 * horizon)
    interpolant = {
        "length": length,
        "horizon": horizon,
        "partition": {
            "A": "cuts reachable from zero by at most H-2 prefix symbols",
            "B": "inverse-terminal-cone hard-core accepting cuts",
            "shared_variables": [
                name
                for position in range(horizon)
                for name in (f"h_{position}", f"l_{position}")
            ],
        },
        "reachable_count": len(reached),
        "accepting_count": len(accepting),
        "prime_candidate_count": candidate_count,
        "minimum_clause_count": len(selected),
        "minimum_total_width_at_that_count": sum(
            len(clause) for clause, _ in selected
        ),
        "clauses": [
            {
                "dimacs": list(clause),
                "formula": clause_text(clause),
                "accepting_points_excluded": covered.bit_count(),
            }
            for clause, covered in selected
        ],
        "verified": {
            "A_implies_I": True,
            "B_implies_not_I": True,
            "fewer_candidate_clauses_unsat": True,
        },
    }
    paths["interpolant"].write_text(
        json.dumps(interpolant, indent=2, sort_keys=True) + "\n"
    )

    record: dict[str, object] = {
        "length": length,
        "horizon": horizon,
        "variables": instance.encoder.top,
        "clauses": len(clauses),
        "full_proof_lines": len(proof),
        "full_proof_check": proof_check,
        "irreducible_core_clauses": len(core_clauses),
        "irreducible_core_indices_one_based": [
            index + 1 for index in core_indices
        ],
        "core_proof_lines": len(core_proof),
        "core_proof_check": core_proof_check,
        "interpolant_clause_count": len(selected),
        "interpolant_widths": [len(clause) for clause, _ in selected],
        "files": {
            key: {
                "path": path.name,
                "sha256": file_digest(path),
            }
            for key, path in paths.items()
        },
    }
    return record, all_prime


def generate(output: Path) -> dict[str, object]:
    output.mkdir(parents=True, exist_ok=True)
    instances = []
    prime_by_horizon = {}
    for length in (4, 5, 6):
        record, prime = instance_artifacts(output, length)
        instances.append(record)
        prime_by_horizon[length + 1] = prime
        print(
            f"C({length},{length + 1}) UNSAT: "
            f"core={record['irreducible_core_clauses']} clauses, "
            f"interpolant={record['interpolant_clause_count']} clauses"
        )

    manifest = {
        "status": "finite exact certificates; no uniform theorem",
        "instances": instances,
        "motif_audit": motif_audit(prime_by_horizon),
    }
    manifest_path = output / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n")
    print(manifest["motif_audit"]["conclusion"])
    print(f"wrote {manifest_path}")
    return manifest


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(__file__).with_name("core-diagonal-interpolants"),
    )
    args = parser.parse_args()
    generate(args.output)


if __name__ == "__main__":
    main()
