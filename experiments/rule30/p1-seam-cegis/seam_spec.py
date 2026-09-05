#!/usr/bin/env python3
"""Independent exact specification of the deterministic ``(Q, Delta)`` map.

The implementation uses only the four-state inverse-cone kernel.  It does not
import the existing binary-wedge verifier, so that comparisons against that
verifier are genuine cross-checks rather than calls through the same code.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping, Protocol


State = int
Word = tuple[int, ...]
Permutation = tuple[int, int, int, int]


def equality_bit(state: State) -> int:
    """Return ``E = 1 + H + L`` over F_2."""

    return 1 ^ (state >> 1) ^ (state & 1)


def boundary(state: State) -> State:
    """The inverse-terminal boundary permutation ``(3,2,1,0)``."""

    if state not in range(4):
        raise ValueError("a four-state symbol must lie in 0..3")
    return state ^ 3


def phi(left: State, right: State) -> State:
    """The exact inverse-cone/Peel kernel in ``(H,E)`` coordinates."""

    if left not in range(4) or right not in range(4):
        raise ValueError("four-state symbols must lie in 0..3")
    high_left = left >> 1
    high_right = right >> 1
    equal_left = equality_bit(left)
    equal_right = equality_bit(right)
    high = high_right ^ 1 ^ equal_left ^ (equal_left & high_left)
    equal = equal_right ^ (high_right & (high_left ^ equal_left))
    low = 1 ^ high ^ equal
    return 2 * high + low


def inverse_cone(endpoint: Word) -> Word:
    """Return the inverse-terminal diagonal ``I(endpoint)``."""

    if not endpoint:
        return ()
    older = tuple(boundary(value) for value in endpoint)
    answer = [older[0]]
    if len(endpoint) == 1:
        return tuple(answer)
    newer = tuple(
        phi(endpoint[index], boundary(endpoint[index + 1]))
        for index in range(len(endpoint) - 1)
    )
    answer.append(newer[0])
    for time in range(2, len(endpoint)):
        current = tuple(
            phi(older[index + 1], newer[index + 1])
            for index in range(len(endpoint) - time)
        )
        answer.append(current[0])
        older, newer = newer, current
    return tuple(answer)


def peel(values: Word) -> Word:
    return tuple(phi(left, right) for left, right in zip(values, values[1:]))


def wedge(endpoint: Word, depth: int) -> Word:
    """Return ``P^depth(I(endpoint))`` exactly."""

    if not 0 <= depth <= len(endpoint):
        raise ValueError("invalid Peel depth")
    result = inverse_cone(endpoint)
    for _ in range(depth):
        result = peel(result)
    return result


@dataclass(frozen=True, slots=True)
class Phase:
    """One affine ``D8`` map ``(h,l)->(h+a,l+b*h+g)``."""

    alpha: int
    beta: int
    gamma: int

    def __post_init__(self) -> None:
        if any(value not in (0, 1) for value in self.coordinates()):
            raise ValueError("phase coordinates must be Boolean")

    def coordinates(self) -> tuple[int, int, int]:
        return self.alpha, self.beta, self.gamma

    def apply(self, state: State) -> State:
        high, low = state >> 1, state & 1
        return 2 * (high ^ self.alpha) + (
            low ^ (self.beta & high) ^ self.gamma
        )

    def permutation(self) -> Permutation:
        return tuple(self.apply(state) for state in range(4))  # type: ignore[return-value]

    def after(self, before: "Phase") -> "Phase":
        """Return ``self o before``."""

        return Phase(
            self.alpha ^ before.alpha,
            self.beta ^ before.beta,
            self.gamma ^ before.gamma ^ (self.beta & before.alpha),
        )

    def inverse(self) -> "Phase":
        return Phase(
            self.alpha,
            self.beta,
            self.gamma ^ (self.alpha & self.beta),
        )


IDENTITY = Phase(0, 0, 0)


def decode_phase(permutation: Permutation) -> Phase:
    alpha = permutation[0] >> 1
    gamma = permutation[0] & 1
    beta = (permutation[2] & 1) ^ gamma
    phase = Phase(alpha, beta, gamma)
    if phase.permutation() != permutation:
        raise ValueError(f"not an affine D8 permutation: {permutation}")
    return phase


def newest_phase(endpoint_prefix: Word, depth: int) -> Phase:
    """Map the next endpoint symbol to the next depth-``depth`` output."""

    permutation = tuple(
        wedge(endpoint_prefix + (state,), depth)[-1] for state in range(4)
    )
    return decode_phase(permutation)  # type: ignore[arg-type]


def forced_symbol(phase: Phase) -> State:
    """The unique binary endpoint symbol forcing output high bit one."""

    return 2 - phase.alpha


def phase_psi(phase: Phase) -> int:
    """The remaining equality bit after high-bit elimination."""

    output = phase.apply(forced_symbol(phase))
    assert output >> 1 == 1
    return equality_bit(output)


def holonomy(left: Phase, right: Phase) -> Phase:
    """Return the ordered defect ``left^-1 o right``."""

    return left.inverse().after(right)


def seam_target(entering: Phase, defect: Phase) -> int:
    """Define an adjacent output defect without using its simplified law."""

    following = entering.after(defect)
    return phase_psi(entering) ^ phase_psi(following)


def seam_environment(entering: Phase, defect: Phase) -> dict[str, int]:
    return dict(
        zip(
            ("a", "b", "g", "x", "y", "z"),
            entering.coordinates() + defect.coordinates(),
        )
    )


class BooleanExpression(Protocol):
    def evaluate(self, environment: Mapping[str, int]) -> int: ...


@dataclass(frozen=True, slots=True)
class ExactMap:
    source: Word
    suffix: Word
    psi: Word
    delta: Word
    phases: tuple[Phase, ...]
    holonomies: tuple[Phase, ...]


@dataclass(frozen=True, slots=True)
class PhaseSummary:
    """A lossless interval summary of an already-derived phase profile."""

    length: int
    entering: Phase
    exiting: Phase
    suffix: Word
    delta: Word


def phase_leaf(phase: Phase) -> PhaseSummary:
    return PhaseSummary(1, phase, phase, (forced_symbol(phase),), ())


def join_phase_summaries(
    left: PhaseSummary,
    right: PhaseSummary,
    expression: BooleanExpression,
) -> PhaseSummary:
    """Concatenate two phase intervals with exactly one seam correction."""

    seam = expression.evaluate(
        seam_environment(left.exiting, holonomy(left.exiting, right.entering))
    )
    return PhaseSummary(
        length=left.length + right.length,
        entering=left.entering,
        exiting=right.exiting,
        suffix=left.suffix + right.suffix,
        delta=left.delta + (seam,) + right.delta,
    )


def summarize_phases(
    phases: tuple[Phase, ...],
    expression: BooleanExpression,
    shape: str = "balanced",
) -> PhaseSummary:
    """Fold a nonempty profile with a selected recursive split shape."""

    if not phases:
        raise ValueError("a phase summary must be nonempty")
    if len(phases) == 1:
        return phase_leaf(phases[0])
    if shape == "left":
        split = len(phases) - 1
    elif shape == "right":
        split = 1
    elif shape == "balanced":
        split = len(phases) // 2
    else:
        raise ValueError("shape must be left, right, or balanced")
    return join_phase_summaries(
        summarize_phases(phases[:split], expression, shape),
        summarize_phases(phases[split:], expression, shape),
        expression,
    )


def exact_map(source: Word) -> ExactMap:
    """Compute the requested deterministic map from the full recurrence."""

    if not source or any(value not in (1, 2) for value in source):
        raise ValueError("the source must be a nonempty word over {1,2}")
    depth = len(source)
    endpoint = source
    suffix: list[int] = []
    phases: list[Phase] = []
    for _ in range(depth + 2):
        phase = newest_phase(endpoint, depth)
        value = forced_symbol(phase)
        phases.append(phase)
        suffix.append(value)
        endpoint += (value,)

    output = wedge(endpoint, depth)
    psi = tuple(equality_bit(state) for state in output)
    delta = tuple(left ^ right for left, right in zip(psi, psi[1:]))
    defects = tuple(
        holonomy(left, right) for left, right in zip(phases, phases[1:])
    )
    assert tuple(phase_psi(phase) for phase in phases) == psi
    return ExactMap(
        source=source,
        suffix=tuple(suffix),
        psi=psi,
        delta=delta,
        phases=tuple(phases),
        holonomies=defects,
    )


def decode_map(
    phases: tuple[Phase, ...], expression: BooleanExpression
) -> tuple[Word, Word]:
    """Decode ``(Q, Delta)`` from a phase profile and a typed seam law."""

    suffix = tuple(forced_symbol(phase) for phase in phases)
    delta = tuple(
        expression.evaluate(seam_environment(phase, defect))
        for phase, defect in zip(phases, map(holonomy, phases, phases[1:]))
    )
    return suffix, delta
