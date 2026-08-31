from __future__ import annotations

import itertools
import unittest

from center_function_probe import (
    Robdd,
    build_center_function,
    direct_center,
    variable_ranks,
)


class CenterFunctionProbeTests(unittest.TestCase):
    def test_reduced_boolean_identities(self) -> None:
        diagram = Robdd()
        variable = diagram.variable(0)
        self.assertEqual(diagram.apply("xor", variable, variable), diagram.ZERO)
        self.assertEqual(diagram.apply("or", variable, diagram.ZERO), variable)
        self.assertEqual(diagram.apply("and", variable, diagram.ONE), variable)

    def test_all_variable_orders_are_permutations(self) -> None:
        for order in ("left_to_right", "right_to_left", "center_out", "outside_in", "bit_reversal"):
            ranks = variable_ranks(4, order)
            self.assertEqual(set(ranks), set(range(-4, 5)))
            self.assertEqual(set(ranks.values()), set(range(9)))

    def test_bdd_matches_direct_rule_on_every_small_input(self) -> None:
        for rule in (22, 30, 90, 110):
            for order in ("left_to_right", "center_out", "bit_reversal"):
                result = build_center_function(rule, 2, order)
                positions = list(range(-2, 3))
                for values in itertools.product((0, 1), repeat=len(positions)):
                    inputs = dict(zip(positions, values))
                    assignment = {result.ranks[position]: value for position, value in inputs.items()}
                    self.assertEqual(
                        result.diagram.evaluate(result.root, assignment),
                        direct_center(rule, 2, inputs),
                    )

    def test_rule90_center_function_stays_small(self) -> None:
        result = build_center_function(90, 8, "left_to_right")
        self.assertLess(result.reachable_nodes, 50)
        self.assertLess(result.maximum_width, 10)


if __name__ == "__main__":
    unittest.main()
