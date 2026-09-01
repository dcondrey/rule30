#!/usr/bin/env python3
"""Signed contact/toggle and carry-tile divergence search."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from scipy.optimize import Bounds, LinearConstraint, linprog, milp

from carry_transducer import (
    State,
    active_symbols,
    carry_step,
    decode,
    gray_macro,
    reachable_states,
)
from runlength_search import boundary_gaps


N_LOCAL = 16 + 4 + 8  # carry/input tiles, input symbols, A/V contacts
N_ENDPOINT = 12        # terminal carry, shallow symbol, deep symbol


def feature(state: State) -> np.ndarray:
    symbols = active_symbols(state)  # shallow to deep
    result = np.zeros(N_LOCAL + N_ENDPOINT, dtype=np.int64)
    carry = (0, 0)
    for symbol in reversed(symbols):
        incoming = 2 * carry[0] + carry[1]
        result[4 * incoming + symbol] += 1
        carry, _ = carry_step(carry, symbol)
    for symbol in symbols:
        result[16 + symbol] += 1
    # Ordered touching-color pairs for A and aligned B, including deep zero.
    for component in range(2):
        bits = [((symbol >> 1) if component == 0 else (symbol & 1)) for symbol in symbols]
        bits.append(0)
        for left, right in zip(bits, bits[1:]):
            result[20 + 4 * component + 2 * left + right] += 1
    offset = N_LOCAL
    result[offset + 2 * carry[0] + carry[1]] = 1
    result[offset + 4 + symbols[0]] = 1
    result[offset + 8 + symbols[-1]] = 1
    return result


def signed_measures(state: State) -> tuple[int, ...]:
    _, A, B = state
    V = 1 | (B << 1)
    height = max(A.bit_length(), V.bit_length())
    mask = (1 << height) - 1
    ones_A = A.bit_count()
    ones_V = (V & mask).bit_count()
    runs_A = len(boundary_gaps(A))
    runs_V = len(boundary_gaps(V))
    contacts_A = height - runs_A
    contacts_V = height - runs_V
    return (
        ones_A - ones_V,
        runs_A - runs_V,
        contacts_A - contacts_V,
        abs(ones_A - ones_V),
        abs(runs_A - runs_V),
        ones_A + runs_A - ones_V - runs_V,
    )


@dataclass(frozen=True)
class Transition:
    before: State
    after: State
    origin: tuple[int, int, int]


def transitions(max_seed: int = 16, max_follow: int = 128) -> tuple[list[Transition], dict[State, tuple[int, int, int]]]:
    origins = reachable_states(max_seed, max_follow)
    result = []
    seen = set()
    for state in sorted(origins, key=lambda value: origins[value]):
        pin, nxt = gray_macro(state)
        if pin and (state, nxt) not in seen:
            seen.add((state, nxt))
            result.append(Transition(state, nxt, origins[state]))
    return result, origins


def delta(transition: Transition) -> np.ndarray:
    return feature(transition.after) - feature(transition.before)


def dominating_transition(items: list[Transition]) -> Transition | None:
    for transition in items:
        change = delta(transition)
        if np.all(change[:N_LOCAL] >= 0) and np.all(change[N_LOCAL:] == 0):
            return transition
    return None


def farkas_certificate(
    items: list[Transition],
) -> tuple[list[Transition], np.ndarray, np.ndarray] | None:
    representatives: dict[tuple[int, ...], Transition] = {}
    for transition in items:
        key = tuple(delta(transition).tolist())
        representatives.setdefault(key, transition)
    keys = list(representatives)
    matrix = np.asarray(keys, dtype=float)
    local = matrix[:, :N_LOCAL]
    endpoint = matrix[:, N_LOCAL:]
    count = len(keys)
    result = linprog(
        np.zeros(count),
        A_ub=-local.T,
        b_ub=np.zeros(N_LOCAL),
        A_eq=np.vstack((endpoint.T, np.ones(count))),
        b_eq=np.concatenate((np.zeros(N_ENDPOINT), np.ones(1))),
        bounds=(0, None),
        method='highs',
    )
    if not result.success:
        return None
    support = np.flatnonzero(result.x > 1e-9)
    exact = np.asarray([keys[index] for index in support], dtype=np.int64)
    local_exact = exact[:, :N_LOCAL]
    endpoint_exact = exact[:, N_LOCAL:]
    integer = milp(
        c=np.ones(len(support)),
        integrality=np.ones(len(support)),
        bounds=Bounds(np.zeros(len(support)), np.full(len(support), 65536.0)),
        constraints=[
            LinearConstraint(local_exact.T, np.zeros(N_LOCAL), np.inf),
            LinearConstraint(endpoint_exact.T, np.zeros(N_ENDPOINT), np.zeros(N_ENDPOINT)),
            LinearConstraint(np.ones((1, len(support))), np.ones(1), np.inf),
        ],
        options={'time_limit': 900},
    )
    if not integer.success:
        return None
    multiplicities = np.rint(integer.x).astype(np.int64)
    chosen = np.flatnonzero(multiplicities)
    multiplicities = multiplicities[chosen]
    exact = exact[chosen]
    aggregate = multiplicities @ exact
    assert np.all(aggregate[:N_LOCAL] >= 0)
    assert np.all(aggregate[N_LOCAL:] == 0)
    transitions_out = [representatives[keys[support[index]]] for index in chosen]
    return transitions_out, multiplicities, aggregate


def signed_diagnostics(items: list[Transition]) -> None:
    names = (
        'ones_A_minus_V',
        'boundaries_A_minus_V',
        'equal_contacts_A_minus_V',
        'abs_ones_difference',
        'abs_boundary_difference',
        'combined_signed_difference',
    )
    for index, name in enumerate(names):
        increase = next(
            (item for item in items if signed_measures(item.after)[index] > signed_measures(item.before)[index]),
            None,
        )
        decrease = next(
            (item for item in items if signed_measures(item.after)[index] < signed_measures(item.before)[index]),
            None,
        )
        print(
            f'{name}: increase={None if increase is None else increase.origin} '
            f'decrease={None if decrease is None else decrease.origin}'
        )


def main() -> None:
    items, _ = transitions()
    print(f'distinct exact accepting transitions: {len(items)}')
    signed_diagnostics(items)
    single = dominating_transition(items)
    print(f'single componentwise obstruction: {single is not None}')
    if single:
        print(f'  origin={single.origin} before={single.before} after={single.after}')
        change = delta(single)
        print(
            f'  local gain={int(change[:N_LOCAL].sum())}; '
            f'endpoint delta={tuple(change[N_LOCAL:])}'
        )
    certificate = farkas_certificate(items)
    print(f'Farkas multiset obstruction: {certificate is not None}')
    if certificate:
        chosen, multiplicities, aggregate = certificate
        print(
            f'  types={len(chosen)} total multiplicity={int(multiplicities.sum())} '
            f'aggregate local gain={int(aggregate[:N_LOCAL].sum())}'
        )
        for transition, multiplicity in zip(chosen, multiplicities):
            print(
                f'  mult={int(multiplicity)} origin={transition.origin} '
                f'before={transition.before} after={transition.after}'
            )


if __name__ == '__main__':
    main()
