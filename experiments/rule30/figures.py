"""Emit the manuscript's space-time figures as TikZ, from the verified rule code.

Every cell drawn is computed by ``zero_tail_probe``; no figure is drawn by
hand.  Run ``python figures.py --check`` to assert the properties each figure
claims to show before regenerating the ``.tex`` fragments.
"""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Iterable, Sequence

from zero_tail_probe import (
    RULE_30,
    RULE_90,
    center_trace,
    class_m_finite_window,
    eca_step,
)

CELL = 0.058
INK = "ruleink"
BAND = "ruleband"
MARK = "rulegold"


def orbit(row: Iterable[int], steps: int, rule: int = RULE_30) -> list[set[int]]:
    current = set(row)
    rows = [set(current)]
    for _ in range(steps):
        current = eca_step(current, rule)
        rows.append(set(current))
    return rows


def _cells(rows: Sequence[set[int]], xs: range, color: str) -> list[str]:
    out = []
    for t, row in enumerate(rows):
        for x in row:
            if x in xs:
                out.append(
                    f"  \\fill[{color}] ({x * CELL:.4f},{-t * CELL:.4f}) "
                    f"rectangle ++({CELL:.4f},{-CELL:.4f});"
                )
    return out


def _band_span(xs: range, steps: int) -> tuple[float, float]:
    _, y0, _, y1 = _card_corners(xs, steps)
    return y0, y1


def _band_under(x: int, xs: range, steps: int) -> str:
    top, bottom = _band_span(xs, steps)
    return (
        f"  \\fill[{BAND}] ({x * CELL:.4f},{top:.4f}) "
        f"rectangle ({(x + 1) * CELL:.4f},{bottom:.4f});"
    )


def _band_over(x: int, xs: range, steps: int) -> list[str]:
    top, bottom = _band_span(xs, steps)
    return [
        f"  \\draw[{MARK}!65, line width=0.3pt] "
        f"({edge * CELL:.4f},{top:.4f}) -- ({edge * CELL:.4f},{bottom:.4f});"
        for edge in (x, x + 1)
    ]


PAD = 1.6


def _card_corners(xs: range, steps: int) -> tuple[float, float, float, float]:
    pad = PAD * CELL
    return (
        xs.start * CELL - pad,
        0.0 + pad,
        xs.stop * CELL + pad,
        -(steps + 1) * CELL - pad,
    )


def _card(xs: range, steps: int, stroke: bool) -> str:
    x0, y0, x1, y1 = _card_corners(xs, steps)
    style = "rulecardline" if stroke else "rulecardfill"
    return (
        f"  \\{'draw' if stroke else 'fill'}[{style}] "
        f"({x0:.4f},{y0:.4f}) rectangle ({x1:.4f},{y1:.4f});"
    )


def _caret(x: int, xs: range, steps: int) -> str:
    _, _, _, y1 = _card_corners(xs, steps)
    cx = (x + 0.5) * CELL
    half = CELL * 0.95
    tip = y1 + CELL * 0.75
    return (
        f"  \\fill[{MARK}] ({cx - half:.4f},{y1:.4f}) -- "
        f"({cx + half:.4f},{y1:.4f}) -- ({cx:.4f},{tip:.4f}) -- cycle;"
    )


def _marker(x: int, t: int) -> list[str]:
    cx = (x + 0.5) * CELL
    cy = -(t + 0.5) * CELL
    radius = CELL * 1.9
    return [
        f"  \\draw[white, line width=1.5pt] ({cx:.4f},{cy:.4f}) "
        f"circle ({radius:.4f});",
        f"  \\draw[{MARK}, line width=0.7pt] ({cx:.4f},{cy:.4f}) "
        f"circle ({radius:.4f});",
    ]


def occupied(rows: Sequence[set[int]], margin: int = 1) -> range:
    live = set().union(*rows) if rows else set()
    if not live:
        return range(-margin, margin + 1)
    return range(min(live) - margin, max(live) + margin + 1)


def panel(
    rows: Sequence[set[int]],
    xs: range,
    steps: int,
    *,
    band: int | None = None,
    marker: tuple[int, int] | None = None,
    color: str = INK,
) -> str:
    body: list[str] = [_card(xs, steps, stroke=False)]
    if band is not None:
        body.append(_band_under(band, xs, steps))
    body.extend(_cells(rows[: steps + 1], xs, color))
    if band is not None:
        body.extend(_band_over(band, xs, steps))
    body.append(_card(xs, steps, stroke=True))
    if band is not None:
        body.append(_caret(band, xs, steps))
    if marker is not None:
        body.extend(_marker(*marker))
    return "\n".join(body)


def fiber_figure(first_one: int = 3, steps: int = 16, half: int = 13) -> str:
    """Theorem 2 made visible: a nonzero member of C_m and its zero center."""
    left_extent = steps + half + 4
    right_bits = [0] * (first_one + 1)
    right_bits[first_one] = 1
    row = class_m_finite_window(first_one, left_extent, right_bits)
    rows = orbit(row, steps)
    xs = range(-half, half + 1)
    return panel(rows, xs, steps, band=0)


def rule90_figure(steps: int = 16, half: int = 13) -> tuple[str, str]:
    """The Rule 90 counterexample beside Rule 30 on the same initial row."""
    seed = {-1, 1}
    xs = range(-half, half + 1)
    ninety = panel(orbit(seed, steps, RULE_90), xs, steps, band=0)
    thirty_rows = orbit(seed, steps, RULE_30)
    trace = center_trace(seed, steps, RULE_30)
    first = next(t for t, bit in enumerate(trace) if bit)
    thirty = panel(thirty_rows, xs, steps, band=0, marker=(0, first))
    return ninety, thirty


def horizon_panels(widths: Sequence[int] = (1, 2, 3, 4, 5, 6)) -> list[tuple[int, str]]:
    """Theorem 4: an extremizer per radius, with the escape cell circled."""
    panels = []
    for w in widths:
        right_bits = [0] * (w + 1)
        right_bits[w] = 1
        first_one = w
        left_extent = w
        row = {
            position
            for position in class_m_finite_window(first_one, left_extent, right_bits)
        }
        steps = 2 * ((w + 1) // 2) + 1
        trace = center_trace(row, steps)
        escape = next(t for t, bit in enumerate(trace) if bit)
        rows = orbit(row, steps)
        xs = occupied(rows[: steps + 1])
        panels.append((w, panel(rows, xs, steps, band=0, marker=(0, escape))))
    return panels


def check() -> None:
    steps = 26
    for m in (1, 2, 3, 5):
        left_extent = steps + 20
        right_bits = [0] * (m + 1)
        right_bits[m] = 1
        row = class_m_finite_window(m, left_extent, right_bits)
        trace = center_trace(row, steps)
        assert set(trace) == {0}, (m, trace)
    assert set(center_trace({-1, 1}, 60, RULE_90)) == {0}
    assert 1 in center_trace({-1, 1}, 60, RULE_30)
    for w, _ in horizon_panels():
        right_bits = [0] * (w + 1)
        right_bits[w] = 1
        row = class_m_finite_window(w, w, right_bits)
        trace = center_trace(row, 2 * ((w + 1) // 2) + 2)
        escape = next(t for t, bit in enumerate(trace) if bit)
        assert escape == 2 * ((w + 1) // 2) + 1, (w, escape, trace)
    print("figures: all claimed properties hold")


def emit(out_dir: Path) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "fig-fiber.tex").write_text(fiber_figure() + "\n")
    ninety, thirty = rule90_figure()
    (out_dir / "fig-rule90.tex").write_text(ninety + "\n")
    (out_dir / "fig-rule30.tex").write_text(thirty + "\n")
    for w, body in horizon_panels():
        (out_dir / f"fig-horizon-{w}.tex").write_text(body + "\n")
    print(f"figures: wrote TikZ fragments to {out_dir}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    parser.add_argument(
        "--out", type=Path, default=Path(__file__).resolve().parents[2]
        / "docs" / "rule30" / "paper" / "figures"
    )
    args = parser.parse_args()
    check()
    if not args.check:
        emit(args.out)


if __name__ == "__main__":
    main()
