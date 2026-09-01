#!/usr/bin/env python3
"""CEGIS for the preregistered fixed-locality additive frontier ranking.

The frontier recurrence is the one proved in RESULTS-alt-trace-fiber.md.
This script does not search deeper spacetime grids.  It asks whether counts of
fixed-radius words in the exact growing frontier admit a nonnegative integer
potential that strictly decreases on every reachable surviving macrostep.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from fractions import Fraction
from math import lcm

import numpy as np
from scipy.optimize import Bounds, LinearConstraint, linprog, milp


State = tuple[int, int, int]  # T, A, B


def wf_step(phase: int, state: State, v: int) -> State:
    """One exact alternating-fiber frontier step (copied algebraically)."""
    T, A, B = state
    C = v & 1
    prev = C
    for j in range(1, T + 1):
        right2 = ((T - 1 + phase) & 1) if j == 1 else ((B >> (j - 2)) & 1)
        cur = (A >> (j - 1)) & 1
        prev ^= cur | right2
        C |= prev << j
    return T + 1, C, A


def or_parity(phase: int, state: State) -> int:
    T, A, B = state
    o = A | ((B << 1) | ((T - 1 + phase) & 1))
    return (o & ((1 << T) - 1)).bit_count() & 1


def seed_state(seed: int, length: int, phase: int = 0) -> State:
    state: State = (0, 0, 0)
    if phase == 1:
        state = wf_step(phase, state, 1)
    for i in range(length):
        rho = (seed >> i) & 1
        state = wf_step(phase, state, 1 - rho)
        state = wf_step(phase, state, 1)
    return state


def forced_macro(phase: int, state: State) -> State | None:
    """Force the next zero output; return None at the next failed pin."""
    state = wf_step(phase, state, or_parity(phase, state))
    if or_parity(phase, state) != 1:
        return None
    return wf_step(phase, state, 1)


def frontier_word(phase: int, state: State) -> tuple[int, ...]:
    """Aligned symbols q_j=(A_j,B_{j-1}), encoded as 2*A_j+B_{j-1}."""
    T, A, B = state
    out = []
    for j in range(1, T + 1):
        a = (A >> (j - 1)) & 1
        b = ((T - 1 + phase) & 1) if j == 1 else ((B >> (j - 2)) & 1)
        out.append(2 * a + b)
    return tuple(out)


def word_counts(word: tuple[int, ...], locality: int) -> np.ndarray:
    size = 4**locality
    counts = np.zeros(size, dtype=np.int64)
    for start in range(len(word) - locality + 1):
        code = 0
        for symbol in word[start : start + locality]:
            code = 4 * code + symbol
        counts[code] += 1
    return counts


def endpoint_code(symbols: tuple[int, ...]) -> int:
    code = 0
    for symbol in symbols:
        code = 4 * code + symbol
    return code


def endpoints(word: tuple[int, ...], locality: int) -> tuple[int, int]:
    width = locality - 1
    if width == 0:
        return 0, 0
    assert len(word) >= width
    return endpoint_code(word[:width]), endpoint_code(word[-width:])


@dataclass(frozen=True)
class Transition:
    seed_length: int
    seed: int
    survival_step: int
    before: State
    after: State


def reachable_transitions(max_seed: int, max_follow: int, phase: int = 0) -> list[Transition]:
    transitions: list[Transition] = []
    seen: set[tuple[State, State]] = set()
    for length in range(1, max_seed + 1):
        for seed in range(1 << length):
            state = seed_state(seed, length, phase)
            for follow in range(max_follow):
                nxt = forced_macro(phase, state)
                if nxt is None:
                    break
                key = (state, nxt)
                if key not in seen:
                    seen.add(key)
                    transitions.append(Transition(length, seed, follow, state, nxt))
                state = nxt
    return transitions


def format_pattern(code: int, locality: int) -> str:
    symbols = [0] * locality
    for i in range(locality - 1, -1, -1):
        symbols[i] = code % 4
        code //= 4
    return " ".join(f"{s >> 1}{s & 1}" for s in symbols)


def same_endpoints(before: tuple[int, ...], after: tuple[int, ...], locality: int) -> bool:
    width = min(locality, len(before), len(after))
    return before[:width] == after[:width] and before[-width:] == after[-width:]


def dominating_counterexample(
    transitions: list[Transition], locality: int, require_same_endpoints: bool = True
) -> Transition | None:
    for tr in sorted(transitions, key=lambda item: (item.seed_length, item.seed, item.survival_step)):
        before = frontier_word(0, tr.before)
        after = frontier_word(0, tr.after)
        delta = word_counts(after, locality) - word_counts(before, locality)
        if np.all(delta >= 0) and (
            not require_same_endpoints or same_endpoints(before, after, locality)
        ):
            return tr
    return None


def full_feature_delta(tr: Transition, locality: int) -> np.ndarray:
    before = frontier_word(0, tr.before)
    after = frontier_word(0, tr.after)
    nlocal = 4**locality
    nendpoint = 1 if locality == 1 else 4 ** (locality - 1)
    delta = np.zeros(nlocal + 2 * nendpoint, dtype=np.int64)
    delta[:nlocal] = word_counts(after, locality) - word_counts(before, locality)
    start_before, end_before = endpoints(before, locality)
    start_after, end_after = endpoints(after, locality)
    delta[nlocal + start_after] += 1
    delta[nlocal + start_before] -= 1
    delta[nlocal + nendpoint + end_after] += 1
    delta[nlocal + nendpoint + end_before] -= 1
    return delta


def synthesize(transitions: list[Transition], locality: int) -> np.ndarray | None:
    """Find a bounded-endpoint, nonnegative local ranking in registered bounds."""
    eligible = [
        tr for tr in transitions
        if len(frontier_word(0, tr.before)) >= locality
    ]
    deltas = {tuple(full_feature_delta(tr, locality).tolist()) for tr in eligible}
    matrix = np.asarray(sorted(deltas), dtype=float)
    nlocal = 4**locality
    nendpoint = 1 if locality == 1 else 4 ** (locality - 1)
    nvars = nlocal + 2 * nendpoint
    constraints = [LinearConstraint(matrix, -np.inf, -np.ones(len(matrix)))]
    # The all-zero word is appended at the deep end and cannot carry weight.
    zero_row = np.zeros((1, nvars))
    zero_row[0, 0] = 1
    constraints.append(LinearConstraint(zero_row, np.zeros(1), np.zeros(1)))
    lower = np.concatenate(
        [np.zeros(nlocal), np.full(2 * nendpoint, -8.0)]
    )
    upper = np.full(nvars, 8.0)
    result = milp(
        c=np.concatenate([np.ones(nlocal), np.zeros(2 * nendpoint)]),
        integrality=np.ones(nvars),
        bounds=Bounds(lower, upper),
        constraints=constraints,
        options={"time_limit": 900},
    )
    if not result.success:
        return None
    weights = np.rint(result.x).astype(int)
    assert np.all(matrix @ weights <= -1)
    return weights


def synthesize_signed(transitions: list[Transition], locality: int) -> np.ndarray | None:
    """Allow every registered coefficient to range over [-8,8].

    This is a stronger feasibility test than a ranking search because it does
    not yet require the resulting energy to be bounded below.
    """
    eligible = [
        tr for tr in transitions
        if len(frontier_word(0, tr.before)) >= locality
    ]
    deltas = {tuple(full_feature_delta(tr, locality).tolist()) for tr in eligible}
    matrix = np.asarray(sorted(deltas), dtype=float)
    nvars = matrix.shape[1]
    result = milp(
        c=np.zeros(nvars),
        integrality=np.ones(nvars),
        bounds=Bounds(np.full(nvars, -8.0), np.full(nvars, 8.0)),
        constraints=[LinearConstraint(matrix, -np.inf, -np.ones(len(matrix)))],
        options={"time_limit": 900},
    )
    if not result.success:
        return None
    weights = np.rint(result.x).astype(int)
    assert np.all(matrix @ weights <= -1)
    return weights


def signed_farkas_support(
    transitions: list[Transition], locality: int
) -> tuple[list[Transition], np.ndarray] | None:
    """Find a nonnegative exact-zero combination of full feature deltas.

    If found, no signed additive potential -- even with unbounded coefficient
    magnitudes -- can strictly decrease on every listed transition.  The LP is
    only a support finder; the returned combination is accepted only if it
    rounds to small integer multiplicities and verifies exactly.
    """
    eligible = [
        tr for tr in transitions
        if len(frontier_word(0, tr.before)) >= locality
    ]
    representatives: dict[tuple[int, ...], Transition] = {}
    for tr in eligible:
        key = tuple(full_feature_delta(tr, locality).tolist())
        representatives.setdefault(key, tr)
    keys = list(representatives)
    matrix = np.asarray(keys, dtype=float)
    m = len(keys)
    eq = np.vstack([matrix.T, np.ones(m)])
    rhs = np.concatenate([np.zeros(matrix.shape[1]), np.ones(1)])
    result = linprog(
        np.zeros(m),
        A_eq=eq,
        b_eq=rhs,
        bounds=(0, None),
        method="highs",
    )
    if not result.success:
        return None
    support = np.flatnonzero(result.x > 1e-9)
    # HiGHS returns a basic rational solution.  Search a modest common scale
    # and accept only an exact integer null combination.
    for scale in range(1, 4097):
        mult = np.rint(result.x[support] * scale).astype(np.int64)
        if np.any(mult <= 0):
            continue
        exact = np.asarray([keys[i] for i in support], dtype=np.int64)
        if np.all(mult @ exact == 0):
            return [representatives[keys[i]] for i in support], mult
    return None


def nonnegative_farkas_support(
    transitions: list[Transition], locality: int
) -> tuple[list[Transition], np.ndarray, np.ndarray] | None:
    """Exact obstruction to nonnegative local weights plus free endpoints.

    Returns a nonnegative transition multiset whose endpoint incidences cancel
    and whose aggregate local-pattern delta is componentwise nonnegative.
    Multiplying strict-decrease inequalities by this multiset gives the exact
    contradiction 0 <= aggregate energy <= -sum(multiplicities).
    """
    nlocal = 4**locality
    eligible = [
        tr for tr in transitions
        if len(frontier_word(0, tr.before)) >= locality
    ]
    representatives: dict[tuple[int, ...], Transition] = {}
    for tr in eligible:
        key = tuple(full_feature_delta(tr, locality).tolist())
        representatives.setdefault(key, tr)
    keys = list(representatives)
    matrix = np.asarray(keys, dtype=float)
    local = matrix[:, :nlocal]
    endpoint = matrix[:, nlocal:]
    m = len(keys)
    result = linprog(
        np.zeros(m),
        A_ub=-local.T,
        b_ub=np.zeros(nlocal),
        A_eq=np.vstack([endpoint.T, np.ones(m)]),
        b_eq=np.concatenate([np.zeros(endpoint.shape[1]), np.ones(1)]),
        bounds=(0, None),
        method="highs",
    )
    if not result.success:
        return None
    support = np.flatnonzero(result.x > 1e-9)
    exact_full = np.asarray([keys[i] for i in support], dtype=np.int64)
    local_support = exact_full[:, :nlocal]
    endpoint_support = exact_full[:, nlocal:]
    integer_result = milp(
        c=np.ones(len(support)),
        integrality=np.ones(len(support)),
        bounds=Bounds(np.zeros(len(support)), np.full(len(support), 65536.0)),
        constraints=[
            LinearConstraint(local_support.T, np.zeros(nlocal), np.inf),
            LinearConstraint(
                endpoint_support.T,
                np.zeros(endpoint_support.shape[1]),
                np.zeros(endpoint_support.shape[1]),
            ),
            LinearConstraint(
                np.ones((1, len(support))), np.ones(1), np.full(1, np.inf)
            ),
        ],
        options={"time_limit": 900},
    )
    if integer_result.success:
        mult = np.rint(integer_result.x).astype(np.int64)
        keep = np.flatnonzero(mult)
        mult = mult[keep]
        exact_full = exact_full[keep]
        aggregate = mult @ exact_full
        assert np.all(aggregate[:nlocal] >= 0)
        assert np.all(aggregate[nlocal:] == 0)
        return (
            [representatives[keys[support[i]]] for i in keep],
            mult,
            aggregate[:nlocal],
        )
    for scale in range(1, 65537):
        mult = np.rint(result.x[support] * scale).astype(np.int64)
        if np.any(mult <= 0):
            continue
        aggregate = mult @ exact_full
        if np.all(aggregate[:nlocal] >= 0) and np.all(aggregate[nlocal:] == 0):
            return (
                [representatives[keys[i]] for i in support],
                mult,
                aggregate[:nlocal],
            )
    for denominator in (10_000, 1_000_000, 100_000_000):
        fractions = [
            Fraction(float(result.x[i])).limit_denominator(denominator)
            for i in support
        ]
        common = 1
        for value in fractions:
            common = lcm(common, value.denominator)
        mult = np.asarray(
            [value.numerator * (common // value.denominator) for value in fractions],
            dtype=object,
        )
        if any(value <= 0 for value in mult):
            continue
        exact_object = np.asarray(
            [[int(value) for value in row] for row in exact_full], dtype=object
        )
        aggregate = mult @ exact_object
        if all(value >= 0 for value in aggregate[:nlocal]) and all(
            value == 0 for value in aggregate[nlocal:]
        ):
            divisor = 0
            from math import gcd
            for value in mult:
                divisor = gcd(divisor, int(value))
            mult = np.asarray([int(value) // divisor for value in mult], dtype=object)
            aggregate = mult @ exact_object
            return (
                [representatives[keys[i]] for i in support],
                mult,
                np.asarray(aggregate[:nlocal], dtype=object),
            )
    return None


def segment_counterexample(
    max_seed: int, max_follow: int, locality: int, phase: int = 0
) -> tuple[int, int, int, int, np.ndarray] | None:
    """Find an endpoint-return segment whose every local count is nondecreasing.

    Such a segment rules out every well-founded additive potential with
    nonnegative local weights and an arbitrary bounded term on these endpoints:
    endpoint terms telescope to zero, while the local contribution is >= 0.
    """
    for length in range(1, max_seed + 1):
        for seed in range(1 << length):
            states = [seed_state(seed, length, phase)]
            for _ in range(max_follow):
                nxt = forced_macro(phase, states[-1])
                if nxt is None:
                    break
                states.append(nxt)
            words = [frontier_word(phase, state) for state in states]
            counts = [word_counts(word, locality) for word in words]
            ends = [
                endpoints(word, locality) if len(word) >= locality - 1 else None
                for word in words
            ]
            for span in range(1, len(states)):
                for start in range(len(states) - span):
                    stop = start + span
                    delta = counts[stop] - counts[start]
                    if (
                        ends[start] is not None
                        and ends[start] == ends[stop]
                        and np.all(delta >= 0)
                    ):
                        return length, seed, start, stop, delta
    return None


def validate_reverse_transducer(max_length: int = 8) -> None:
    """Exhaustively verify the reverse cumulative-XOR macro description."""
    checked = 0
    for T in range(2, 2 * max_length + 1, 2):
        # Exhaust arbitrary A,B only while the Boolean space stays below 2^20.
        if 2 * T - 1 > 20:
            break
        for mask in range(1 << (2 * T - 1)):
            A = mask & ((1 << T) - 1)
            B = mask >> T
            state = (T, A, B)
            nxt = forced_macro(0, state)
            if nxt is None:
                continue
            Tp, D, C = nxt
            assert Tp == T + 2
            # Survival means both newly forced deepest outputs are zero.
            assert ((C >> T) & 1) == 0
            assert ((D >> (T + 1)) & 1) == 0
            # Reverse recurrences, including the pin boundary D_1=1.
            cnext = 0
            dnext2 = 0
            recovered_c = 0
            recovered_d = 0
            for j in range(T, 0, -1):
                aj = (A >> (j - 1)) & 1
                bjm1 = 1 if j == 1 else ((B >> (j - 2)) & 1)
                cj = cnext ^ (aj | bjm1)
                dj1 = dnext2 ^ (cnext | aj)
                recovered_c |= cj << (j - 1)
                recovered_d |= dj1 << j
                cnext, dnext2 = cj, dj1
            d1 = dnext2 ^ (cnext | 0)  # a_0=c_T=0 for even T, phase 01
            recovered_d |= d1
            assert recovered_c == C
            assert recovered_d == D
            assert d1 == 1
            if A.bit_length() >= B.bit_length():
                assert D.bit_length() == A.bit_length() + 1
                assert D.bit_length() >= C.bit_length()
            checked += 1
    print(f"reverse macro transducer: PASS ({checked} surviving arbitrary states)")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-seed", type=int, default=12)
    parser.add_argument("--max-follow", type=int, default=64)
    args = parser.parse_args()

    validate_reverse_transducer()
    transitions = reachable_transitions(args.max_seed, args.max_follow)
    print(f"reachable surviving macro transitions: {len(transitions)}")
    for locality in range(1, 5):
        counterexample = dominating_counterexample(transitions, locality)
        if counterexample is not None:
            before = frontier_word(0, counterexample.before)
            after = frontier_word(0, counterexample.after)
            delta = word_counts(after, locality) - word_counts(before, locality)
            changed = [
                (format_pattern(i, locality), int(value))
                for i, value in enumerate(delta)
                if value
            ]
            print(
                f"locality {locality}: componentwise nondecrease counterexample "
                f"seed_length={counterexample.seed_length} "
                f"seed={counterexample.seed:0{counterexample.seed_length}b} "
                f"follow={counterexample.survival_step}; deltas={changed}"
            )
        segment = segment_counterexample(
            args.max_seed, args.max_follow, locality
        )
        if segment is not None:
            length, seed, start, stop, delta = segment
            changed = [
                (format_pattern(i, locality), int(value))
                for i, value in enumerate(delta)
                if value
            ]
            print(
                f"locality {locality}: endpoint-return nondecrease segment "
                f"seed_length={length} seed={seed:0{length}b} "
                f"steps=[{start},{stop}); deltas={changed}"
            )
        weights = synthesize(transitions, locality)
        if weights is None:
            print(
                f"locality {locality}: MILP UNSAT/no ranking with local "
                "weights 0..8 and endpoint terms -8..8"
            )
            obstruction = nonnegative_farkas_support(transitions, locality)
            if obstruction is None:
                print(
                    f"locality {locality}: no exact nonnegative Farkas "
                    "multiset recovered"
                )
            else:
                support, mult, aggregate = obstruction
                desc = [
                    (
                        int(n), tr.seed_length,
                        format(tr.seed, f"0{tr.seed_length}b"),
                        tr.survival_step,
                    )
                    for tr, n in zip(support, mult, strict=True)
                ]
                gains = [
                    (format_pattern(i, locality), int(value))
                    for i, value in enumerate(aggregate)
                    if value
                ]
                print(
                    f"locality {locality}: exact nonnegative Farkas multiset "
                    f"({len(support)} types, multiplicity {int(mult.sum())}) "
                    f"gains={gains}; transitions={desc}"
                )
        else:
            nlocal = 4**locality
            nonzero = [
                (format_pattern(i, locality), int(w))
                for i, w in enumerate(weights[:nlocal])
                if w
            ]
            print(
                f"locality {locality}: candidate local weights {nonzero}; "
                f"endpoint range=({weights[nlocal:].min()},"
                f"{weights[nlocal:].max()})"
            )
        signed = synthesize_signed(transitions, locality)
        if signed is None:
            print(
                f"locality {locality}: signed MILP UNSAT even before "
                "well-foundedness"
            )
            farkas = signed_farkas_support(transitions, locality)
            if farkas is None:
                print(f"locality {locality}: no small exact Farkas support recovered")
            else:
                support, mult = farkas
                desc = [
                    (
                        int(n), tr.seed_length,
                        format(tr.seed, f"0{tr.seed_length}b"),
                        tr.survival_step,
                    )
                    for tr, n in zip(support, mult, strict=True)
                ]
                print(
                    f"locality {locality}: exact zero-sum transition multiset "
                    f"({len(support)} types, multiplicity {int(mult.sum())}): {desc}"
                )
        else:
            print(
                f"locality {locality}: signed decreasing functional exists "
                "on sample (not yet a ranking)"
            )


if __name__ == "__main__":
    main()
