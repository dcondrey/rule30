#!/usr/bin/env python3
"""Falsifiers for mortality after adding the uniform rho!=00000 theorem."""

from __future__ import annotations

import argparse

from carry_transducer import State, forced_macro, parity_or, seed_state


def legal(word: str) -> bool:
    return "11" not in word and "00000" not in word


def legal_words(length: int):
    def visit(prefix: str):
        if len(prefix) == length:
            yield prefix
            return
        for bit in "01":
            following = prefix + bit
            if legal(following):
                yield from visit(following)

    return visit("")


def replay(state: State, history: str, cap: int) -> tuple[int, str]:
    accepted = 0
    for _ in range(cap):
        rho = 1 ^ parity_or(state)
        history += str(rho)
        if not legal(history[-5:]):
            return accepted, "right-language"
        following = forced_macro(state)
        if following is None:
            return accepted, "pin"
        accepted += 1
        state = following
    return accepted, "cap"


def seed_replay(word: str, cap: int = 128) -> tuple[int, str]:
    seed = sum(int(bit) << index for index, bit in enumerate(word))
    return replay(seed_state(seed, len(word)), word, cap)


def enumerate_seeds(max_length: int) -> list[dict[str, object]]:
    rows = []
    for length in range(1, max_length + 1):
        count = 0
        best = (-1, "", "")
        for word in legal_words(length):
            count += 1
            survival, outcome = seed_replay(word)
            candidate = survival, word, outcome
            if candidate[0] > best[0]:
                best = candidate
        if best[0] >= 9:
            raise AssertionError(
                f"constant-eight counterexample n={length} rho={best[1]}"
            )
        rows.append(
            {
                "length": length,
                "legal_seeds": count,
                "maximum": best[0],
                "witness": best[1],
                "outcome": best[2],
            }
        )
    return rows


def arbitrary_core_control() -> tuple[State, str, int, str]:
    """A non-seed frontier showing that nine-step mortality is seed-specific."""
    state = (12, 81, 658)
    history = "0001"
    survival, outcome = replay(state, history, 32)
    assert survival == 10 and outcome == "right-language"

    seed_states = {
        seed_state(
            sum(int(bit) << index for index, bit in enumerate(word)), 6
        )
        for word in legal_words(6)
    }
    assert state not in seed_states
    return state, history, survival, outcome


def two_factor_counterexample() -> tuple[str, int, str]:
    """The first retained counterexample to constant-eight mortality."""
    word = "010101001010101010101000100010"
    assert legal(word)
    survival, outcome = seed_replay(word, 32)
    assert survival == 10 and outcome == "pin"
    # It refutes only the {11,00000} filter, not actual right realizability.
    assert "101001" in word
    return word, survival, outcome


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-length", type=int, default=24)
    args = parser.parse_args()

    print("n legal-seeds max-survival witness death")
    for row in enumerate_seeds(args.max_length):
        print(
            f"{row['length']:2d} {row['legal_seeds']:7d} "
            f"{row['maximum']:2d} {row['witness']} {row['outcome']}"
        )

    state, history, survival, outcome = arbitrary_core_control()
    print(
        "arbitrary-core control: "
        f"state={state} history={history} survival={survival} death={outcome}"
    )
    word, survival, outcome = two_factor_counterexample()
    print(
        "two-factor seed counterexample: "
        f"rho={word} survival={survival} death={outcome}; "
        "contains actual-right forbidden factor 101001"
    )


if __name__ == "__main__":
    main()
