#!/usr/bin/env python3
"""Exact local closure audit for the proposed coupled mode machine.

The three suggested coordinates advance on different axes:

* corner boundary modes advance when a spatial core symbol is peeled;
* matched/defect states advance when the seed length/interval changes; and
* right-filter phases advance when a rho bit is emitted.

This script constructs each exact local transition relation separately and
asks whether the recorded finite vocabularies are closed.  It emits a
counterexample as soon as a coordinate leaves its vocabulary; it never
splices the three axes into an unjustified product transition.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from carry_transducer import forced_macro, parity_or, seed_state
from core_discharge import FORWARD, SWAP, peel_boundary
from defect_restart_cocycle import build_result as full_cocycle_result
from interval_annihilator_audit import build_result as interval_result


@dataclass(frozen=True, order=True)
class BoundaryMode:
    """An exact ultimately periodic sequence ``prefix period^infinity``."""

    prefix: tuple[int, ...]
    period: tuple[int, ...]

    def value(self, time: int) -> int:
        if time < len(self.prefix):
            return self.prefix[time]
        return self.period[(time - len(self.prefix)) % len(self.period)]

    def key(self) -> str:
        prefix = "".join(map(str, self.prefix)) or "empty"
        period = "".join(map(str, self.period))
        return f"{prefix}|({period})*"


def primitive_period(period: tuple[int, ...]) -> tuple[int, ...]:
    for size in range(1, len(period) + 1):
        if len(period) % size == 0 and all(
            period[index] == period[index % size]
            for index in range(len(period))
        ):
            return period[:size]
    raise AssertionError("nonempty period has no primitive divisor")


def normalize_mode(
    prefix: tuple[int, ...], period: tuple[int, ...]
) -> BoundaryMode:
    """Return the unique least-preperiod representation with fixed phase."""

    if not period:
        raise ValueError("period must be nonempty")
    prefix = tuple(prefix)
    period = primitive_period(tuple(period))
    while prefix and prefix[-1] == period[-1]:
        symbol = prefix[-1]
        prefix = prefix[:-1]
        period = (symbol,) + period[:-1]
    return BoundaryMode(prefix, primitive_period(period))


def peel_mode(mode: BoundaryMode, symbol: int) -> BoundaryMode:
    """Apply the corner-peel recurrence to an infinite boundary mode."""

    output = [FORWARD[symbol][mode.value(0)]]
    seen: dict[tuple[int, int], int] = {}
    time = 0
    while True:
        if time >= len(mode.prefix):
            phase = (time - len(mode.prefix)) % len(mode.period)
            state = phase, output[-1]
            if state in seen:
                start = seen[state]
                return normalize_mode(
                    tuple(output[:start]), tuple(output[start:time])
                )
            seen[state] = time
        time += 1
        following_symbol = SWAP[output[-1]]
        output.append(FORWARD[following_symbol][mode.value(time)])


NAMED_MODES: dict[str, BoundaryMode] = {
    "ZERO": normalize_mode((), (0,)),
    "ONE": normalize_mode((), (1,)),
    "TWO": normalize_mode((), (2,)),
    "THREE": normalize_mode((), (3,)),
    "THREE_THEN_ONE": normalize_mode((3,), (1,)),
    "ALT_02": normalize_mode((), (0, 2)),
    "ALT_20": normalize_mode((), (2, 0)),
}


def boundary_transition_table() -> tuple[list[dict[str, Any]], dict[str, Any]]:
    names_by_mode = {mode: name for name, mode in NAMED_MODES.items()}
    transitions = []
    for source_name, source in NAMED_MODES.items():
        for symbol in range(4):
            destination = peel_mode(source, symbol)
            finite_source = tuple(source.value(time) for time in range(128))
            finite_destination = peel_boundary(finite_source, symbol)
            assert finite_destination == tuple(
                destination.value(time) for time in range(128)
            )
            transitions.append(
                {
                    "source": source_name,
                    "symbol": symbol,
                    "destination": names_by_mode.get(
                        destination, destination.key()
                    ),
                    "inside_named_vocabulary": destination in names_by_mode,
                }
            )

    zero = NAMED_MODES["ZERO"]
    first = peel_mode(zero, 1)
    second = peel_mode(first, 0)
    third = peel_mode(second, 0)
    assert first == NAMED_MODES["TWO"]
    assert second == NAMED_MODES["THREE_THEN_ONE"]
    assert third == normalize_mode((), (2, 3))
    assert third not in names_by_mode
    escape = {
        "word": "100",
        "path": [
            NAMED_MODES["ZERO"].key(),
            first.key(),
            second.key(),
            third.key(),
        ],
        "destination": third.key(),
    }
    return transitions, escape


def cut_feed(states: tuple[int, ...], symbol: int) -> tuple[int, ...]:
    """Independent finite-prefix implementation of one boundary peel."""

    following = list(states)
    for layer in range(len(following)):
        following[layer] = FORWARD[symbol][following[layer]]
        symbol = SWAP[following[layer]]
    return tuple(following)


def reachable_cuts(horizon: int) -> set[tuple[int, ...]]:
    reached = {(0,) * horizon}
    frontier = reached
    for _ in range(max(0, horizon - 2)):
        frontier = {
            cut_feed(states, symbol)
            for states in frontier
            for symbol in range(4)
        }
        reached |= frontier
    return reached


def boundary_growth(max_depth: int) -> list[dict[str, Any]]:
    """Enumerate exact modes only to falsify closure, never as a proof."""

    zero = NAMED_MODES["ZERO"]
    witness: dict[BoundaryMode, str] = {zero: ""}
    frontier = {zero}
    records = []
    for depth in range(1, max_depth + 1):
        following = set()
        for mode in sorted(frontier):
            for symbol in range(4):
                destination = peel_mode(mode, symbol)
                if destination not in witness:
                    witness[destination] = witness[mode] + str(symbol)
                    following.add(destination)
        frontier = following

        horizon = depth + 2
        truncated = {
            tuple(mode.value(index) for index in range(horizon))
            for mode in witness
        }
        # This is the exact local identity between repeated corner peeling
        # and the independently implemented vertical-cut feed operation.
        assert truncated == reachable_cuts(horizon)

        maximal = max(
            witness,
            key=lambda mode: (
                len(mode.prefix),
                len(mode.period),
                witness[mode],
            ),
        )
        records.append(
            {
                "peel_depth": depth,
                "new_modes": len(frontier),
                "total_modes": len(witness),
                "reachable_cut_horizon": horizon,
                "reachable_cut_count": len(truncated),
                "maximum_preperiod": max(
                    len(mode.prefix) for mode in witness
                ),
                "maximum_period": max(len(mode.period) for mode in witness),
                "max_preperiod_witness_word": witness[maximal],
                "max_preperiod_mode": maximal.key(),
            }
        )
    return records


FILTER_PATTERNS = ("11", "00000")
FILTER_PREFIXES = ("", "0", "00", "000", "0000", "1")
FILTER_REJECT = "REJECT"


def right_filter_step(phase: str, bit: int) -> str:
    if phase == FILTER_REJECT:
        return FILTER_REJECT
    word = phase + str(bit)
    if any(word.endswith(pattern) for pattern in FILTER_PATTERNS):
        return FILTER_REJECT
    return max(
        (prefix for prefix in FILTER_PREFIXES if word.endswith(prefix)),
        key=len,
    )


def right_filter_audit() -> dict[str, Any]:
    phases = FILTER_PREFIXES + (FILTER_REJECT,)
    table = {
        phase or "START": {
            str(bit): right_filter_step(phase, bit) or "START"
            for bit in (0, 1)
        }
        for phase in phases
    }

    word = "010101001010101010101000100010"
    state = seed_state(
        sum(int(bit) << index for index, bit in enumerate(word)),
        len(word),
    )
    history = word
    accepted = 0
    while True:
        bit = 1 ^ parity_or(state)
        history += str(bit)
        assert all(pattern not in history for pattern in FILTER_PATTERNS)
        successor = forced_macro(state)
        if successor is None:
            break
        accepted += 1
        state = successor
    assert accepted == 10
    assert "101001" in history
    return {
        "patterns": list(FILTER_PATTERNS),
        "transition_table": table,
        "closed": True,
        "complete_for_actual_right_language": False,
        "insufficiency_control": {
            "rho_history": history,
            "accepted_macros": accepted,
            "death": "pin",
            "contains_longer_actual_right_forbidden_factor": "101001",
        },
    }


def defect_graph_audit() -> dict[str, Any]:
    result = interval_result()
    transitions = result["matched_extension_transitions"]
    ranks = [
        (
            item["shorter_n"],
            item["longer_n"],
            item["matched_rank"],
            item["defect_rank"],
        )
        for item in transitions
    ]
    assert ranks == [
        (10, 11, 6, 0),
        (11, 12, 6, 0),
        (12, 13, 6, 5),
        (13, 14, 11, 0),
    ]
    labels = {
        item["label"] for item in result["compact_annihilator_states"]
    }
    assert labels == {
        "A_10",
        "A_11",
        "A_12",
        "A_13",
        "A_14",
        "B_13",
        "B_14",
    }
    edges = [
        {"source": "A_10", "kind": "matched", "destination": "A_11"},
        {"source": "A_11", "kind": "matched", "destination": "A_12"},
        {"source": "A_12", "kind": "matched", "destination": "A_13"},
        {"source": "A_12", "kind": "defect", "destination": "B_13"},
        {"source": "A_13", "kind": "matched", "destination": "A_14"},
        {"source": "B_13", "kind": "matched", "destination": "B_14"},
    ]
    full = full_cocycle_result()
    conclusion = full["conclusion"]
    assert conclusion["exact_full_driver_cocycle_built"]
    assert not conclusion["indicator_plus_period_three_phase_is_closed"]
    assert not conclusion["well_founded_uniform_rank_found"]
    collision = full["indicator_phase_closure_collision"]
    assert collision["left_offset"] == 5
    assert collision["right_offset"] == 8
    return {
        "recorded_type_dictionary": {
            "nodes": sorted(labels),
            "edges": edges,
            "terminally_unclassified_nodes": ["A_14", "B_14"],
            "closed": False,
        },
        "full_driver_cocycle": {
            "state": "F_m=(S_m, previous forced rho, P_m)",
            "closed": True,
            "finite_dimensional": False,
            "frontier_growth": "two symbolic coordinates per macro",
            "compressed_indicator_phase_closed": False,
            "compressed_summary_collision": {
                "summary": collision["summary"],
                "left_offset": collision["left_offset"],
                "right_offset": collision["right_offset"],
                "phase_mod_3": collision["shared_phase_mod_3"],
                "shared_indicator_rank": collision["shared_indicator"][
                    "principal_rank"
                ],
            },
        },
        "finite_type_graph_closed": False,
        "reason": (
            "A generic exact successor exists only after restoring the full "
            "width-growing frontier driver; the finite A/B type dictionary "
            "and its indicator/phase compression do not close."
        ),
        "uniform_matched_extension_lemma_verified": result[
            "conclusion"
        ]["matched_extension_shift_is_uniform"],
    }


def build_audit(max_depth: int) -> dict[str, Any]:
    boundary_transitions, escape = boundary_transition_table()
    growth = boundary_growth(max_depth)
    right = right_filter_audit()
    defect = defect_graph_audit()
    return {
        "schema": "rule30.coupled-mode-closure-audit.v1",
        "axes": {
            "boundary_mode": "spatial peel depth",
            "matched_defect": "seed length and interval origin",
            "right_filter": "emitted rho time",
        },
        "boundary": {
            "named_modes": {
                name: mode.key() for name, mode in NAMED_MODES.items()
            },
            "transitions": boundary_transitions,
            "closed": False,
            "first_escape": escape,
            "growth": growth,
        },
        "right_filter": right,
        "matched_defect": defect,
        "product": {
            "closed": False,
            "infinite_valid_paths_decided": False,
            "reasons": [
                "the seven named boundary modes are not closed",
                "the finite A/B dictionary is partial and the closed replacement is width-growing",
                "the {11,00000} DFA is not the complete actual-right language",
                "the three coordinates advance on different axes without a proved scheduler",
            ],
        },
        "conclusion": (
            "The proposed finite three-part trap is not closed; no mortality "
            "or period-two theorem follows."
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-depth", type=int, default=10)
    parser.add_argument("--json", type=Path)
    args = parser.parse_args()
    audit = build_audit(args.max_depth)
    boundary = audit["boundary"]
    growth = boundary["growth"]
    print(
        "named corner modes: NOT CLOSED; first escape word="
        f"{boundary['first_escape']['word']} destination="
        f"{boundary['first_escape']['destination']}"
    )
    print(
        f"exact boundary modes through depth {args.max_depth}: "
        f"{growth[-1]['total_modes']} "
        f"(cut cross-check H={growth[-1]['reachable_cut_horizon']} PASS)"
    )
    print("right {11,00000} filter: CLOSED BUT INSUFFICIENT")
    print("finite A/B graph: NOT CLOSED; exact full cocycle: WIDTH-GROWING")
    print("coupled finite-state trap: NOT CLOSED")
    print("period-two mortality: OPEN")
    if args.json is not None:
        args.json.write_text(json.dumps(audit, indent=2, sort_keys=True) + "\n")
        print(f"wrote {args.json}")


if __name__ == "__main__":
    main()
