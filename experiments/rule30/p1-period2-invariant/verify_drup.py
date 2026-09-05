#!/usr/bin/env python3
"""Small independent DRUP checker for the mortality experiment.

This deliberately shares no encoding code with ``mortality_sat.py``.  It
checks every proof addition by reverse unit propagation and supports the
deletion lines emitted by PySAT's Glucose wrapper.
"""

from __future__ import annotations

import argparse
from collections import defaultdict
from pathlib import Path


def canonical(clause: list[int] | tuple[int, ...]) -> tuple[int, ...]:
    return tuple(sorted(set(clause), key=lambda lit: (abs(lit), lit < 0)))


def parse_dimacs(path: Path) -> list[tuple[int, ...]]:
    clauses: list[tuple[int, ...]] = []
    pending: list[int] = []
    for raw in path.read_text().splitlines():
        line = raw.strip()
        if not line or line.startswith("c") or line.startswith("p"):
            continue
        for token in line.split():
            literal = int(token)
            if literal:
                pending.append(literal)
            else:
                clauses.append(canonical(pending))
                pending = []
    if pending:
        raise ValueError("unterminated DIMACS clause")
    return clauses


def parse_proof_line(raw: str) -> tuple[bool, tuple[int, ...]] | None:
    tokens = raw.strip().split()
    if not tokens or tokens[0] == "c":
        return None
    deletion = tokens[0] == "d"
    if deletion:
        tokens = tokens[1:]
    values = [int(token) for token in tokens]
    if not values or values[-1] != 0:
        raise ValueError(f"unterminated proof line: {raw!r}")
    return deletion, canonical(values[:-1])


class RupDatabase:
    """Clause database with persistent two-watched-literal positions."""

    def __init__(self, clauses: list[tuple[int, ...]]) -> None:
        self.clauses: list[tuple[int, ...]] = []
        self.active: list[bool] = []
        self.watched: list[list[int]] = []
        self.watchers: dict[int, set[int]] = defaultdict(set)
        self.units: set[int] = set()
        self.by_clause: dict[tuple[int, ...], list[int]] = defaultdict(list)
        for clause in clauses:
            self.add(clause)

    def add(self, clause: tuple[int, ...]) -> int:
        cid = len(self.clauses)
        self.clauses.append(clause)
        self.active.append(True)
        if not clause:
            positions: list[int] = []
        elif len(clause) == 1:
            positions = [0]
            self.watchers[clause[0]].add(cid)
            self.units.add(cid)
        else:
            positions = [0, 1]
            self.watchers[clause[0]].add(cid)
            self.watchers[clause[1]].add(cid)
        self.watched.append(positions)
        self.by_clause[clause].append(cid)
        return cid

    def delete(self, clause: tuple[int, ...]) -> bool:
        for cid in reversed(self.by_clause.get(clause, [])):
            if self.active[cid]:
                self.active[cid] = False
                self.units.discard(cid)
                return True
        return False

    def rup(self, candidate: tuple[int, ...]) -> bool:
        assignment: dict[int, bool] = {}
        queue: list[int] = []

        def value(literal: int) -> bool | None:
            current = assignment.get(abs(literal))
            if current is None:
                return None
            return current == (literal > 0)

        def assign(literal: int) -> bool:
            variable = abs(literal)
            wanted = literal > 0
            current = assignment.get(variable)
            if current is not None:
                return current == wanted
            assignment[variable] = wanted
            queue.append(literal)
            return True

        # A tautological candidate has contradictory negated assumptions.
        for literal in candidate:
            if not assign(-literal):
                return True

        for cid, clause in enumerate(self.clauses):
            if self.active[cid] and not clause:
                return True
        for cid in tuple(self.units):
            if self.active[cid] and not assign(self.clauses[cid][0]):
                return True

        cursor = 0
        while cursor < len(queue):
            made_true = queue[cursor]
            cursor += 1
            made_false = -made_true
            for cid in tuple(self.watchers.get(made_false, ())):
                if not self.active[cid]:
                    continue
                clause = self.clauses[cid]
                positions = self.watched[cid]
                if len(positions) == 1:
                    if value(clause[0]) is False:
                        return True
                    continue

                if clause[positions[0]] == made_false:
                    false_slot, other_slot = 0, 1
                elif clause[positions[1]] == made_false:
                    false_slot, other_slot = 1, 0
                else:
                    continue
                other_pos = positions[other_slot]
                other_lit = clause[other_pos]
                if value(other_lit) is True:
                    continue

                replacement = None
                for pos, literal in enumerate(clause):
                    if pos == other_pos:
                        continue
                    if value(literal) is not False:
                        replacement = pos
                        break
                if replacement is not None:
                    positions[false_slot] = replacement
                    self.watchers[made_false].discard(cid)
                    self.watchers[clause[replacement]].add(cid)
                    continue
                if value(other_lit) is False:
                    return True
                if not assign(other_lit):
                    return True
        return False


def check_proof(
    clauses: list[tuple[int, ...]], proof_lines: list[str]
) -> dict[str, int | bool]:
    database = RupDatabase(clauses)
    additions = deletions = 0
    max_width = 0
    empty_seen = False
    for line_number, raw in enumerate(proof_lines, start=1):
        parsed = parse_proof_line(raw)
        if parsed is None:
            continue
        deletion, clause = parsed
        if deletion:
            # Deliberately retain deleted clauses.  RUP is monotone under
            # adding already-derived clauses, so this is a sound checker
            # strategy and avoids depending on a producer's duplicate-clause
            # deletion convention.  It may accept a later step using a
            # retained lemma, but that lemma was itself checked and is a
            # logical consequence of the base formula.
            deletions += 1
            continue
        if not database.rup(clause):
            raise AssertionError(
                f"proof line {line_number} is not RUP: {' '.join(map(str, clause))}"
            )
        database.add(clause)
        additions += 1
        max_width = max(max_width, len(clause))
        empty_seen |= not clause
    if not empty_seen:
        raise AssertionError("proof contains no checked empty clause")
    return {
        "checked": True,
        "additions": additions,
        "deletions": deletions,
        "max_width": max_width,
        "empty_seen": empty_seen,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("cnf", type=Path)
    parser.add_argument("proof", type=Path)
    args = parser.parse_args()
    result = check_proof(parse_dimacs(args.cnf), args.proof.read_text().splitlines())
    print(result)


if __name__ == "__main__":
    main()
