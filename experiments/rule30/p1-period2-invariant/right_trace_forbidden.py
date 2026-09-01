#!/usr/bin/env python3
"""Exact right-column forbidden factors for an alternating Rule 30 center."""

from __future__ import annotations

import argparse


ANF = frozenset[int]
ZERO: ANF = frozenset()
ONE: ANF = frozenset({0})


def add(left: ANF, right: ANF) -> ANF:
    return left ^ right


def multiply(left: ANF, right: ANF) -> ANF:
    result: set[int] = set()
    for first in left:
        for second in right:
            term = first | second
            if term in result:
                result.remove(term)
            else:
                result.add(term)
    return frozenset(result)


def complement(value: ANF) -> ANF:
    return add(ONE, value)


def disjunction(left: ANF, right: ANF) -> ANF:
    return add(add(left, right), multiply(left, right))


def rule30_anf(left: ANF, center: ANF, right: ANF) -> ANF:
    return add(left, disjunction(center, right))


def symbolic_rho(length: int, rule30: bool = True) -> tuple[ANF, ...]:
    """Even-time column-1 bits from the minimal right light cone."""
    width = 2 * length - 1
    row = [frozenset({1 << index}) for index in range(width)]
    answer = []
    for time in range(2 * length - 1):
        if time % 2 == 0:
            answer.append(row[0])
        if time == 2 * length - 2:
            break
        boundary = ONE if time % 2 else ZERO
        following = []
        for index in range(len(row) - 1):
            left = boundary if index == 0 else row[index - 1]
            center = row[index]
            right = row[index + 1]
            if rule30:
                following.append(rule30_anf(left, center, right))
            else:
                following.append(add(left, right))
        row = following
    assert len(answer) == length
    return tuple(answer)


def all_zero_indicator(values: tuple[ANF, ...]) -> ANF:
    result = ONE
    for value in values:
        result = multiply(result, complement(value))
    return result


def numeric_rho(seed: int, length: int, rule30: bool = True) -> str:
    row = seed
    answer = []
    for time in range(2 * length - 1):
        if time % 2 == 0:
            answer.append(str(row & 1))
        boundary = time & 1
        if rule30:
            row = ((row << 1) | boundary) ^ (row | (row >> 1))
        else:
            row = ((row << 1) | boundary) ^ (row >> 1)
    return "".join(answer)


def realized_language(length: int, rule30: bool = True) -> set[str]:
    width = 2 * length - 1
    return {
        numeric_rho(seed, length, rule30)
        for seed in range(1 << width)
    }


def language_table(max_length: int) -> list[dict[str, object]]:
    languages = {0: {""}}
    rows = []
    for length in range(1, max_length + 1):
        language = realized_language(length)
        languages[length] = language
        forbidden = []
        for value in range(1 << length):
            word = f"{value:0{length}b}"
            if word in language:
                continue
            if (
                word[:-1] in languages[length - 1]
                and word[1:] in languages[length - 1]
            ):
                forbidden.append(word)
        rows.append(
            {
                "length": length,
                "realized": len(language),
                "minimal_forbidden": forbidden,
            }
        )
    return rows


def independent_five_zero_check(rule30: bool = True) -> tuple[int, int | None]:
    checked = 0
    witness = None
    for seed in range(1 << 9):
        word = numeric_rho(seed, 5, rule30)
        if word == "00000" and witness is None:
            witness = seed
        checked += 1
    return checked, witness


def rule90_center_control(horizon: int = 128) -> None:
    row = {-1, 1}
    for _ in range(horizon + 1):
        assert 0 not in row
        if not row:
            return
        row = {
            index
            for index in range(min(row) - 1, max(row) + 2)
            if ((index - 1 in row) ^ (index + 1 in row))
        }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-language", type=int, default=10)
    args = parser.parse_args()

    rho4 = symbolic_rho(4)
    rho5 = symbolic_rho(5)
    assert all_zero_indicator(rho4) != ZERO
    assert all_zero_indicator(rho5) == ZERO
    checked, witness = independent_five_zero_check()
    assert checked == 512 and witness is None
    print(
        "Rule 30 five-zero theorem: ANF product is zero and "
        "512/512 independent light cones PASS"
    )

    rule90_product = all_zero_indicator(symbolic_rho(5, rule30=False))
    checked90, witness90 = independent_five_zero_check(rule30=False)
    assert rule90_product != ZERO and checked90 == 512 and witness90 is not None
    print(f"Rule 90 five-zero control: witness seed={witness90:#x} PASS")

    rule90_center_control()
    print("Rule 90 {-1,1} center-zero control through t=128: PASS")

    print("length realized-prefixes new-minimal-forbidden-factors")
    for row in language_table(args.max_language):
        print(
            f"{row['length']:2d} {row['realized']:5d} "
            f"{','.join(row['minimal_forbidden']) or '-'}"
        )


if __name__ == "__main__":
    main()
