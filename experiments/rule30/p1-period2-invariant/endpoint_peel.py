#!/usr/bin/env python3
"""Moving-endpoint identities and the exact obstruction to a naive peel.

This checker is deliberately independent of the SAT encoding.  It verifies
the aligned-word Mealy tableau against the integer Gray macro, checks the
moving two-coordinate inverse-Gray identities, and exhaustively tests the
registered semantic implication behind a one-seed/two-follow peel.
"""

from __future__ import annotations

import argparse
from itertools import product

from bilateral_hardcore import (
    adversarial_control,
    check_local_identity,
    hard_core,
    hard_core_survival,
    rule90,
    update,
)
from carry_transducer import (
    active_symbols,
    carry_step,
    gray_inverse,
    gray_macro,
    seed_state,
    terminal,
)


def aligned_word(state: tuple[int, int, int]) -> tuple[int, ...]:
    """Return the active aligned word in deep-to-shallow order."""
    return tuple(reversed(active_symbols(state)))


def tableau_step(word: tuple[int, ...]) -> tuple[tuple[int, ...], int]:
    """Apply one exact deep-to-shallow Mealy row and append its terminal."""
    carry = (0, 0)
    output: list[int] = []
    for symbol in word:
        carry, emitted = carry_step(carry, symbol)
        output.append(emitted)
    last = terminal(carry)
    output.append(last)
    return tuple(output), last >> 1


def exhaustive_tableau_crosscheck(max_width: int) -> int:
    """Compare the independent word tableau with the Gray macro."""
    checked = 0
    for width in range(2, max_width + 1, 2):
        for A in range(1 << width):
            for B in range(1 << (width - 1)):
                state = (width, A, B)
                word = aligned_word(state)
                # Leading aligned zero symbols are inert from zero carry.  Add
                # them back so the tableau has the registered fixed width.
                padded = (0,) * (width - len(word)) + word
                successor_word, pin = tableau_step(padded)
                gray_pin, successor = gray_macro(state)
                expected = aligned_word(successor)
                expected = (0,) * (width + 1 - len(expected)) + expected
                if (pin, successor_word) != (gray_pin, expected):
                    raise AssertionError(
                        (width, A, B, padded, successor_word, expected, pin, gray_pin)
                    )
                if gray_pin and successor_word[-1] != 3:
                    raise AssertionError("a surviving row did not append terminal 3")
                checked += 1
    return checked


def kernel_entry(i: int, j: int) -> int:
    return (min(i, j) + 1) & 1


def check_kernel_block(max_width: int) -> int:
    """Check K_(w+2) blockwise; the loops are also an entrywise proof oracle."""
    checked = 0
    for width in range(0, max_width + 1, 2):
        for i in range(width + 2):
            for j in range(width + 2):
                if i < width and j < width:
                    expected = kernel_entry(i, j)
                elif i < width:
                    expected = (i + 1) & 1
                elif j < width:
                    expected = (j + 1) & 1
                else:
                    expected = ((1, 1), (1, 0))[i - width][j - width]
                if kernel_entry(i, j) != expected:
                    raise AssertionError((width, i, j, expected))
                checked += 1
    return checked


def check_inverse_gray_append(max_width: int) -> int:
    """Check P_(w+2)(x,a,b)=(P_w x+a+b,a+b,b)."""
    checked = 0
    for width in range(0, max_width + 1, 2):
        low_mask = (1 << width) - 1
        for x in range(1 << width):
            for a, b in product((0, 1), repeat=2):
                extended = x | (a << width) | (b << (width + 1))
                expected = gray_inverse(x) ^ (low_mask if a ^ b else 0)
                expected |= (a ^ b) << width
                expected |= b << (width + 1)
                actual = gray_inverse(extended)
                if actual != expected:
                    raise AssertionError((width, x, a, b, actual, expected))
                checked += 1
    return checked


def hard_core_seeds(length: int):
    for seed in range(1 << length):
        if hard_core(seed):
            yield seed


def mortality_profile(max_seed: int, cap: int) -> list[tuple[int, int, int, str]]:
    """Return (n, maximum, first witness, outcome), by full enumeration."""
    profile: list[tuple[int, int, int, str]] = []
    for length in range(1, max_seed + 1):
        best = (-1, 0, "")
        for seed in hard_core_seeds(length):
            survival, outcome, _ = hard_core_survival(seed, length, cap)
            if outcome == "cap":
                raise AssertionError(("continuation cap reached", length, seed))
            candidate = (survival, -seed, outcome)
            if candidate > (best[0], -best[1], best[2]):
                best = (survival, seed, outcome)
        profile.append((length, *best))
    return profile


def first_peel_obstruction(
    profile: list[tuple[int, int, int, str]], cap: int
) -> tuple[object, ...] | None:
    """Disprove the semantic implication (n,H)->(n-1,H-2), if possible."""
    for current, previous in zip(profile[1:], profile):
        n, survival, seed, outcome = current
        previous_n, previous_maximum, _, _ = previous
        assert previous_n == n - 1
        if survival > previous_maximum + 2:
            replay = hard_core_survival(seed, n, cap)
            if replay[0] != survival or replay[1] != outcome:
                raise AssertionError((current, replay))
            # A total semantics-preserving peel would turn this witness into a
            # length-(n-1) seed surviving survival-2, but exhaustive enumeration
            # proves the displayed maximum is smaller.
            return (
                n,
                seed,
                survival,
                outcome,
                previous_n,
                previous_maximum,
                survival - 2,
                seed_state(seed, n),
            )
    return None


def rule90_control(horizon: int = 128) -> None:
    row = {-1, 1}
    for time in range(horizon + 1):
        if 0 in row:
            raise AssertionError(("Rule 90 center became nonzero", time))
        row = update(row, rule90)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-word-width", type=int, default=8)
    parser.add_argument("--max-block-width", type=int, default=10)
    parser.add_argument("--max-seed", type=int, default=18)
    parser.add_argument("--cap", type=int, default=128)
    args = parser.parse_args()

    tableaus = exhaustive_tableau_crosscheck(args.max_word_width)
    block_entries = check_kernel_block(args.max_block_width)
    append_words = check_inverse_gray_append(args.max_block_width)
    print(f"aligned Mealy/Gray tableau cross-check: {tableaus} frontiers PASS")
    print(f"K_(w+2) moving-endpoint block identity: {block_entries} entries PASS")
    print(f"inverse-Gray two-bit append identity: {append_words} words PASS")

    profile = mortality_profile(args.max_seed, args.cap)
    print("mortality profile:")
    print("  " + ",".join(f"{n}:{maximum}" for n, maximum, _, _ in profile))
    obstruction = first_peel_obstruction(profile, args.cap)
    if obstruction is None:
        print("one-seed/two-follow semantic peel: no obstruction in range")
    else:
        (
            n,
            seed,
            survival,
            outcome,
            previous_n,
            previous_maximum,
            required,
            state,
        ) = obstruction
        print("one-seed/two-follow semantic peel: EXACT OBSTRUCTION")
        print(
            f"  length {n} seed={seed:#x} survives {survival} ({outcome}); "
            f"state={state}"
        )
        print(
            f"  a peel would require length {previous_n} survival {required}, "
            f"but the exhaustive maximum is {previous_maximum}"
        )

    checked, xor_counterexample = check_local_identity()
    if checked != 8 or xor_counterexample is None:
        raise AssertionError((checked, xor_counterexample))
    rho, adversarial_checks = adversarial_control()
    if adversarial_checks != 7:
        raise AssertionError((rho, adversarial_checks))
    rule90_control()
    print("Rule 30 right-column/no-11 control: 8/8 PASS")
    print(f"Rule 30 adversarial trace: {rho}, first fails at t=15 PASS")
    print("Rule 90 {-1,1}: zero center through t=128 PASS")


if __name__ == "__main__":
    main()
