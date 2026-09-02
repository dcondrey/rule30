#!/usr/bin/env python3
"""Exact local algebra and cancellation control for projected support."""

from __future__ import annotations

from itertools import product

from constant_tail_holonomy_defect_closure import scenario_rows
from constant_tail_scale import Affine, hard_core_extension_length


def main() -> None:
    affines = tuple(
        Affine(alpha, beta, gamma)
        for alpha, beta, gamma in product(range(2), repeat=3)
    )

    legal_counts = {2: 0, 3: 0}
    for affine in affines:
        for tail in (2, 3):
            forced = affine.permutation().index(tail)
            legal = forced in (1, 2)
            expected = (
                affine.gamma == (affine.alpha | affine.beta)
                if tail == 2
                else affine.gamma == int(not (affine.alpha | affine.beta))
            )
            assert legal == expected
            if legal:
                assert forced == 2 - affine.alpha
                legal_counts[tail] += 1

    # pi_2=(alpha,beta) is an additive quotient of the D8 composition.
    for after in affines:
        for before in affines:
            composed = after.after(before)
            assert (composed.alpha, composed.beta) == (
                after.alpha ^ before.alpha,
                after.beta ^ before.beta,
            )

    # pi_3=(alpha,gamma) is the literal state A(0), not a group quotient.
    for affine in affines:
        assert affine.apply(0) == 2 * affine.alpha + affine.gamma

    # The smallest endpoint-telescope cancellation retained in the reports.
    word = (1, 2, 1)
    tail = 3
    scenarios = tuple(scenario_rows(word, prefix, tail) for prefix in range(4))
    survival = hard_core_extension_length(
        word, tuple(row.forced for row in scenarios[0])
    )
    assert survival == 4
    projected = tuple(
        (scenario[0].affine.alpha, scenario[0].affine.gamma)
        for scenario in scenarios
    )
    assert projected == ((0, 1), (1, 0), (1, 0), (0, 1))
    assert projected[0] == projected[-1]
    assert len(set(projected)) == 2

    print(
        f"hard-core legality table: tail2={legal_counts[2]} "
        f"tail3={legal_counts[3]} affine states PASS"
    )
    print("tail-2 (alpha,beta) additive quotient: 64 products PASS")
    print("tail-3 (alpha,gamma)=A(0): 8 affine states PASS")
    print(
        "endpoint telescope cancellation: W=121 tail=3 row=0 "
        f"values={projected} survival={survival} PASS"
    )


if __name__ == "__main__":
    main()
