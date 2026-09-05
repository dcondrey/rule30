from __future__ import annotations

import json
import sys
import unittest
from itertools import product
from pathlib import Path


HERE = Path(__file__).resolve().parent
OLD = HERE.parent / "p1-period2-invariant"
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(OLD))

from binary_wedge_high_elimination import force_high_one  # noqa: E402
from cegis import minimal_sufficient_fields, projected_collision, run_cegis  # noqa: E402
from seam_spec import (  # noqa: E402
    IDENTITY,
    Phase,
    decode_map,
    exact_map,
    phi,
    seam_target,
    summarize_phases,
)


class SeamCegisTest(unittest.TestCase):
    def test_local_kernel(self) -> None:
        expected = (
            (0, 1, 3, 2),
            (3, 2, 1, 0),
            (3, 2, 0, 1),
            (3, 2, 1, 0),
        )
        self.assertEqual(
            tuple(tuple(phi(left, right) for right in range(4)) for left in range(4)),
            expected,
        )

    def test_d8_group(self) -> None:
        phases = tuple(Phase(*values) for values in product((0, 1), repeat=3))
        self.assertEqual(len({phase.permutation() for phase in phases}), 8)
        for left, middle, right in product(phases, repeat=3):
            self.assertEqual(
                left.after(middle).after(right), left.after(middle.after(right))
            )
        for phase in phases:
            self.assertEqual(phase.after(phase.inverse()), IDENTITY)
            self.assertEqual(phase.inverse().after(phase), IDENTITY)

    def test_projection_and_synthesis(self) -> None:
        self.assertIsNotNone(projected_collision(("x", "y", "z")))
        fields = minimal_sufficient_fields()
        self.assertEqual(fields, ("a", "x", "y", "z"))
        result = run_cegis(fields)
        self.assertEqual(result.expression.operator_cost(), 5)
        self.assertGreater(len(result.rejections), 0)

    def test_all_local_seams(self) -> None:
        result = run_cegis(minimal_sufficient_fields())
        phases = tuple(Phase(*values) for values in product((0, 1), repeat=3))
        for entering, defect in product(phases, repeat=2):
            environment = dict(
                zip(
                    ("a", "b", "g", "x", "y", "z"),
                    entering.coordinates() + defect.coordinates(),
                )
            )
            self.assertEqual(
                result.expression.evaluate(environment), seam_target(entering, defect)
            )

    def test_full_recurrence_crosscheck(self) -> None:
        result = run_cegis(minimal_sufficient_fields())
        for length in range(1, 7):
            for source in product((1, 2), repeat=length):
                exact = exact_map(source)
                expected_suffix, expected_psi = force_high_one(source, length + 2)
                suffix, delta = decode_map(exact.phases, result.expression)
                self.assertEqual(exact.suffix, expected_suffix)
                self.assertEqual(exact.psi, expected_psi)
                self.assertEqual(suffix, exact.suffix)
                self.assertEqual(delta, exact.delta)
                summaries = tuple(
                    summarize_phases(exact.phases, result.expression, shape)
                    for shape in ("left", "right", "balanced")
                )
                self.assertTrue(all(item.suffix == exact.suffix for item in summaries))
                self.assertTrue(all(item.delta == exact.delta for item in summaries))

    def test_archived_corpus(self) -> None:
        result = run_cegis(minimal_sufficient_fields())
        corpus = json.loads((HERE / "adversarial_corpus.json").read_text())
        for record in corpus:
            exact = exact_map(tuple(map(int, record["source"])))
            self.assertEqual(decode_map(exact.phases, result.expression), (exact.suffix, exact.delta))


if __name__ == "__main__":
    unittest.main()
