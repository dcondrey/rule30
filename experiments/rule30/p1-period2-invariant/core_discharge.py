#!/usr/bin/env python3
"""Exact reverse carry cascade and local-factor obstruction controls."""

from __future__ import annotations

from itertools import product

from carry_transducer import (
    State,
    carry_step,
    decode,
    encode,
    forced_macro,
    parity_or,
    seed_state,
)
from tail_density import aligned_word, append_macro


SWAP = (0, 2, 1, 3)
FORWARD = tuple(
    tuple(encode(carry_step(decode(state), symbol)[0]) for state in range(4))
    for symbol in range(4)
)
INVERSE = []
for transition in FORWARD:
    inverse = [0] * 4
    for state, successor in enumerate(transition):
        inverse[successor] = state
    INVERSE.append(tuple(inverse))
INVERSE = tuple(INVERSE)


def state_from_aligned(word: tuple[int, ...]) -> State:
    """Decode a shallow-to-deep aligned word at even depth."""
    depth = len(word)
    assert depth % 2 == 0
    if not word:
        return 0, 0, 0
    assert word[0] & 1 == 1
    first = sum((symbol >> 1) << index for index, symbol in enumerate(word))
    second = sum(
        (symbol & 1) << (index - 1)
        for index, symbol in enumerate(word)
        if index >= 1
    )
    return depth, first, second


def reverse_append(state: State, rho: int) -> tuple[State, tuple[int, int]]:
    """Append one seed macro by reading the old word shallow-to-deep.

    The prescribed shallow carry is `(1-rho,rho)`.  Every input action is a
    permutation, so the old word can be traversed in reverse and the final
    deep carry is exactly the pair of newly reconstructed tail bits.
    """
    carry = 1 if rho else 2
    successor = [3]
    for symbol in aligned_word(state):
        successor.append(SWAP[carry])
        carry = INVERSE[symbol][carry]
    emitted = (carry >> 1, carry & 1)
    successor.append(SWAP[carry])
    return state_from_aligned(tuple(successor)), emitted


def reverse_crosscheck(max_depth: int = 6) -> int:
    checked = 0
    for depth in range(0, max_depth + 1, 2):
        for first in range(1 << depth):
            for second in range(1 << max(0, depth - 1)):
                state = (depth, first, second)
                for rho in (0, 1):
                    assert reverse_append(state, rho) == append_macro(state, rho)
                    checked += 1
    return checked


def cascade_feed(
    states: tuple[int, ...], symbol: int, start: int = 0
) -> tuple[int, ...]:
    """Feed one shallow-to-deep symbol through a reverse-macro cascade."""
    following = list(states)
    for layer in range(start, len(following)):
        output = SWAP[following[layer]]
        following[layer] = INVERSE[symbol][following[layer]]
        symbol = output
    return tuple(following)


def cascade_initial(rho: tuple[int, ...]) -> tuple[int, ...]:
    """Build the exact shallow boundary state for a fixed rho word."""
    states = tuple(1 if bit else 2 for bit in rho)
    for layer in range(len(states) - 1, 0, -1):
        states = cascade_feed(states, 3, layer)
    return states


def cascade_finish(states: tuple[int, ...]) -> tuple[int, ...]:
    """Flush all deep emitted symbols; return their carry encodings."""
    following = states
    for layer in range(len(following) - 1):
        following = cascade_feed(
            following, SWAP[following[layer]], layer + 1
        )
    return following


def cascade_crosscheck(max_horizon: int = 5, max_depth: int = 4) -> int:
    checked = 0
    for horizon in range(1, max_horizon + 1):
        for rho in product((0, 1), repeat=horizon):
            if any(left == right == 1 for left, right in zip(rho, rho[1:])):
                continue
            for depth in range(0, max_depth + 1, 2):
                for first in range(1 << depth):
                    for second in range(1 << max(0, depth - 1)):
                        state = (depth, first, second)
                        cascade = cascade_initial(rho)
                        for symbol in aligned_word(state):
                            cascade = cascade_feed(cascade, symbol)
                        observed = cascade_finish(cascade)

                        direct = []
                        for bit in rho:
                            state, emitted = append_macro(state, bit)
                            direct.append(2 * emitted[0] + emitted[1])
                        assert tuple(direct) == observed
                        checked += 1
    return checked


def seven_zero_seed_control() -> tuple[int, int]:
    """Replay a seed-generated seven-step zero-emission factor."""
    length = 22
    seed = 0x24A28
    state = seed_state(seed, length)
    for _ in range(7):
        assert 1 ^ parity_or(state) == 0
        appended, emitted = append_macro(state, 0)
        assert emitted == (0, 0)
        forced = forced_macro(state)
        assert forced is not None and appended == forced
        state = forced
    return length, seed


def alternating_seed_control() -> tuple[int, int, str]:
    """Replay both radius-seven windows of a negative alternating cycle."""
    length = 26
    seed = 0x892512
    continuation = "01010101"
    state = seed_state(seed, length)
    for bit in map(int, continuation):
        assert 1 ^ parity_or(state) == bit
        appended, emitted = append_macro(state, bit)
        assert emitted == (0, 0)
        forced = forced_macro(state)
        assert forced is not None and appended == forced
        state = forced
    return length, seed, continuation


def peel_boundary(beta: tuple[int, ...], initial_symbol: int) -> tuple[int, ...]:
    """Carry sequence exposed after deleting one deep word symbol."""
    gamma = [FORWARD[initial_symbol][beta[0]]]
    for following_beta in beta[1:]:
        gamma.append(FORWARD[SWAP[gamma[-1]]][following_beta])
    return tuple(gamma)


def peel_mode_controls() -> int:
    horizon = 16
    zero = (0,) * horizon
    assert peel_boundary(zero, 1) == (2,) * horizon
    assert peel_boundary(zero, 2) == (3,) * horizon
    assert peel_boundary((2,) * horizon, 1) == (1,) * horizon
    assert peel_boundary((2,) * horizon, 0) == (3,) + (1,) * (horizon - 1)
    assert peel_boundary((3,) * horizon, 1) == (0, 2) * (horizon // 2)
    assert peel_boundary((3,) * horizon, 0) == (2, 0) * (horizon // 2)
    return 6 * horizon


def main() -> None:
    reverse = reverse_crosscheck()
    cascade = cascade_crosscheck()
    length, seed = seven_zero_seed_control()
    alt_length, alt_seed, continuation = alternating_seed_control()
    peel_checks = peel_mode_controls()
    print(f"reverse append: {reverse} arbitrary frontiers PASS")
    print(f"reverse cascades: {cascade} arbitrary instances PASS")
    print(
        "radius-seven factor obstruction: "
        f"n={length} seed={seed:#x} forced-rho=0000000 "
        "emitted=00^7 PASS"
    )
    print(
        "alternating factor obstruction: "
        f"n={alt_length} seed={alt_seed:#x} forced-rho={continuation} "
        "emitted=00^8 PASS"
    )
    print(f"corner-peel boundary modes: {peel_checks} symbols PASS")


if __name__ == "__main__":
    main()
