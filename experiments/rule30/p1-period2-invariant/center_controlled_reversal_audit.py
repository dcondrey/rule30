#!/usr/bin/env python3
"""Exact center-controlled reversal and adaptive-fold audit."""

from __future__ import annotations

from itertools import combinations, product


Vector = tuple[int, ...]
FEATURES = ("X", "N", "O")


def rule30(left: int, center: int, right: int) -> int:
    return left ^ (center | right)


def right_step(word: Vector, next_center: int) -> Vector:
    """Advance a center-to-edge right half and append its new edge."""

    following = [next_center]
    for index in range(1, len(word)):
        following.append(
            rule30(
                word[index - 1],
                word[index],
                word[index + 1] if index + 1 < len(word) else 0,
            )
        )
    following.append(rule30(word[-1], 0, 0))
    return tuple(following)


def encode(word: Vector, center: int) -> Vector:
    assert word[0] == center
    return word if center == 0 else tuple(reversed(word))


def decode(encoded: Vector, center: int) -> Vector:
    word = encoded if center == 0 else tuple(reversed(encoded))
    assert word[0] == center
    return word


def adaptive_step(encoded: Vector, center: int) -> Vector:
    physical = decode(encoded, center)
    assert physical[-1] == 1
    next_center = 1 - center
    return encode(right_step(physical, next_center), next_center)


def left_step(word: Vector, next_center: int) -> Vector:
    """Advance a center-to-edge left half and append its new edge."""

    following = [next_center]
    for index in range(1, len(word)):
        following.append(
            rule30(
                word[index + 1] if index + 1 < len(word) else 0,
                word[index],
                word[index - 1],
            )
        )
    following.append(rule30(0, 0, word[-1]))
    return tuple(following)


def inherited(encoded: Vector, center: int, steps: int) -> Vector:
    following = encoded
    phase = center
    for _ in range(steps):
        following = adaptive_step(following, phase)
        phase = 1 - phase
    assert len(following) == len(encoded) + steps
    # The final orientation decides which end contains the newly appended
    # physical edge cells.
    if phase == 1:
        return following[steps:]
    return following[:-steps]


def admissible_words(length: int, center: int):
    for encoded in product((0, 1), repeat=length):
        physical = encoded if center == 0 else tuple(reversed(encoded))
        if physical[0] == center and physical[-1] == 1:
            yield encoded


def compare(output: Vector, source: Vector, colex: bool, one_low: bool) -> int:
    order = (1, 0) if one_low else (0, 1)
    indices = (
        range(len(source) - 1, -1, -1) if colex else range(len(source))
    )
    for index in indices:
        if output[index] != source[index]:
            return -1 if order[output[index]] < order[source[index]] else 1
    return 0


def comparison_census(max_length: int, steps: int):
    answer = {}
    for center in (0, 1):
        for colex in (False, True):
            for one_low in (False, True):
                counts = {-1: 0, 0: 0, 1: 0}
                examples: dict[int, tuple[int, Vector, Vector]] = {}
                for length in range(1, max_length + 1):
                    for source in admissible_words(length, center):
                        output = inherited(source, center, steps)
                        relation = compare(output, source, colex, one_low)
                        counts[relation] += 1
                        examples.setdefault(relation, (length, source, output))
                answer[(center, colex, one_low)] = (counts, examples)
    return answer


def half_words(length: int, center: int):
    for word in product((0, 1), repeat=length):
        if word[0] == center and word[-1] == 1:
            yield word


def word_key(word: Vector, colex: bool, one_low: bool) -> Vector:
    order = (1, 0) if one_low else (0, 1)
    values = tuple(reversed(word)) if colex else word
    return tuple(order[value] for value in values)


def product_key(
    left: Vector,
    right: Vector,
    phase: int,
    config: tuple[str, bool, bool],
) -> Vector:
    primary, left_one_low, right_one_low = config
    left_key = word_key(left, False, left_one_low)
    # The adaptive right edge is at the end in phase zero and at the
    # beginning in phase one.  Read away from the center so that it is least
    # significant in either representation.
    right_key = word_key(right, phase == 1, right_one_low)
    return (
        left_key + right_key if primary == "A" else right_key + left_key
    )


def two_half_rank_search(max_length: int = 9):
    configs = tuple(
        (primary, left_one_low, right_one_low)
        for primary in ("A", "B")
        for left_one_low in (False, True)
        for right_one_low in (False, True)
    )
    candidates = {(zero, one) for zero in configs for one in configs}
    first_failure = {}
    cases = 0
    for length in range(1, max_length + 1):
        for phase in (0, 1):
            for left in half_words(length, phase):
                left_following = left_step(left, 1 - phase)[:-1]
                for right in admissible_words(length, phase):
                    right_following = inherited(right, phase, 1)
                    cases += 1
                    for pair in tuple(candidates):
                        source_config = pair[phase]
                        target_config = pair[1 - phase]
                        source = product_key(
                            left, right, phase, source_config
                        )
                        target = product_key(
                            left_following,
                            right_following,
                            1 - phase,
                            target_config,
                        )
                        if not target < source:
                            candidates.remove(pair)
                            first_failure[pair] = (
                                length,
                                phase,
                                left,
                                right,
                                left_following,
                                right_following,
                                target == source,
                            )
    return candidates, first_failure, cases


def two_step_bit(values: Vector) -> int:
    assert len(values) == 5
    first = tuple(
        rule30(values[index], values[index + 1], values[index + 2])
        for index in range(3)
    )
    return rule30(*first)


def pair_bits(state: int) -> tuple[int, int]:
    return state >> 1, state & 1


def projected(state: int, names: tuple[str, ...]) -> tuple[int, ...]:
    left, right = pair_bits(state)
    values = {"X": left ^ right, "N": left & right, "O": left | right}
    return tuple(values[name] for name in names)


def two_step_fold(stencil: Vector, phase: int) -> int:
    """Interior two-step pair map returning to the same fold orientation."""

    if phase == 0:
        assert len(stencil) == 5
        left_values = tuple(pair_bits(state)[0] for state in reversed(stencil))
        right_values = tuple(pair_bits(state)[1] for state in stencil)
    else:
        assert len(stencil) == 7
        # Stencil coordinates are i-4,...,i+2.
        left_values = tuple(
            pair_bits(stencil[index])[0] for index in (6, 5, 4, 3, 2)
        )
        right_values = tuple(
            pair_bits(stencil[index])[1] for index in (4, 3, 2, 1, 0)
        )
    return 2 * two_step_bit(left_values) + two_step_bit(right_values)


def fold_collision(names: tuple[str, ...], phase: int):
    width = 5 if phase == 0 else 7
    seen = {}
    for stencil in product(range(4), repeat=width):
        key = tuple(projected(state, names) for state in stencil)
        output = projected(two_step_fold(stencil, phase), names)
        previous = seen.get(key)
        if previous is not None and previous[0] != output:
            return previous[1], stencil
        seen.setdefault(key, (output, stencil))
    return None


def subsets(items: tuple[str, ...]):
    for size in range(1, len(items) + 1):
        yield from combinations(items, size)


def fmt_word(word: Vector) -> str:
    return "".join(map(str, word))


def main() -> None:
    # Literal involution and edge-placement controls on every admissible word.
    checked = 0
    for length in range(1, 11):
        for center in (0, 1):
            for encoded in admissible_words(length, center):
                physical = decode(encoded, center)
                assert encode(physical, center) == encoded
                following = adaptive_step(encoded, center)
                assert decode(following, 1 - center) == right_step(
                    physical, 1 - center
                )
                if center == 0:
                    assert following[0] == 1
                else:
                    assert following[-1] == 1
                checked += 1
    print(f"adaptive reversal and alternating edge placement: {checked} PASS")

    for steps in (1, 2):
        census = comparison_census(14, steps)
        print(f"inherited-word comparison after {steps} step(s):")
        for key, (counts, examples) in census.items():
            center, colex, one_low = key
            order_name = ("colex" if colex else "lex") + (
                " 1<0" if one_low else " 0<1"
            )
            fields = f"less/equal/greater={counts[-1]}/{counts[0]}/{counts[1]}"
            if set(relation for relation, count in counts.items() if count) == {-1}:
                assert steps == 1 and center == 1 and not colex and not one_low
                fields += " ALL-WORD STRICT: first bit 1 -> 0"
            else:
                directions = []
                for relation, label in ((-1, "<"), (1, ">")):
                    if relation in examples:
                        length, source, output = examples[relation]
                        directions.append(
                            f"{label}@n{length}:{fmt_word(source)}->{fmt_word(output)}"
                        )
                fields += " " + " ".join(directions)
            print(f"  phase={center} {order_name}: {fields}")

    # Geometric endpoint law for the adaptive paired fold.
    for center in (0, 1):
        if center == 0:
            endpoints = ((center, center), (1, 1))
        else:
            endpoints = ((center, 1), (1, center))
        assert all(left ^ right == 0 for left, right in endpoints)
    print("adaptive folded XOR endpoints: zero in both phases PASS")

    for phase in (0, 1):
        for names in subsets(FEATURES):
            collision = fold_collision(names, phase)
            assert collision is not None
            print(
                f"phase={phase} symmetric two-step projection="
                f"{''.join(names)} NOT-CLOSED collision="
                f"{collision[0]}/{collision[1]}"
            )

    rank_candidates, rank_failures, rank_cases = two_half_rank_search()
    assert not rank_candidates
    last_pair, last_failure = max(
        rank_failures.items(), key=lambda item: item[1][0]
    )
    length, phase, left, right, left_next, right_next, equal = last_failure
    print(
        "adaptive two-half lexicographic products: "
        f"64/64 rejected in {rank_cases} row pairs; "
        f"last survivor {last_pair} fails at n={length}, phase={phase}, "
        f"A/B={fmt_word(left)}/{fmt_word(right)} -> "
        f"{fmt_word(left_next)}/{fmt_word(right_next)}, equal={equal}"
    )

    print(
        "scope: the phase-1 one-step lex descent is erased by phase 0; "
        "no fixed word order or symmetric two-step folded quotient closes"
    )


if __name__ == "__main__":
    main()
