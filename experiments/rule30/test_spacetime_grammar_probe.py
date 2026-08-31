from __future__ import annotations

import unittest

from spacetime_grammar_probe import (
    RULE_90,
    active_cone_complement,
    build_tile_grammar,
    directional_tile_reuse,
    directional_word_vocabulary,
    edge_vocabulary,
    eca_grid,
    greedy_boundary_signature,
    random_triangle_grid,
    symmetry_quotient,
    transform_tile_word,
)


class SpacetimeGrammarProbeTests(unittest.TestCase):
    def test_grammar_exactly_reconstructs_grid(self) -> None:
        bits, side = eca_grid(RULE_90, 16)
        grammar = build_tile_grammar(bits, side)
        observed = [
            grammar.bit_at(row, column)
            for row in range(side)
            for column in range(side)
        ]
        self.assertEqual(observed, bits)

    def test_uniform_grid_has_one_type_per_nonterminal_scale(self) -> None:
        grammar = build_tile_grammar([0] * 64, 8)
        self.assertEqual(grammar.type_counts, (2, 1, 1, 1))
        self.assertEqual(grammar.occurrences[3], {0: 1})

    def test_rendered_tile_matches_original_root(self) -> None:
        bits, side = eca_grid(RULE_90, 8)
        grammar = build_tile_grammar(bits, side)
        rendered = grammar.render_tile(grammar.levels, grammar.root)
        self.assertEqual([bit for row in rendered for bit in row], bits)

    def test_perimeter_ambiguity_detects_different_interiors(self) -> None:
        # Two 4x4 tiles with the same all-zero perimeter and different centers.
        side = 8
        bits = [0] * (side * side)
        bits[1 * side + 1] = 1
        bits[1 * side + 5] = 0
        edges, signatures, tile_types, ambiguous = edge_vocabulary(bits, side, 4)
        self.assertEqual(edges, 1)
        self.assertEqual(signatures, 1)
        self.assertEqual(tile_types, 2)
        self.assertEqual(ambiguous, 1)

    def test_greedy_boundary_reports_unresolvable_interior(self) -> None:
        side = 8
        bits = [0] * (side * side)
        bits[1 * side + 1] = 1
        signature = greedy_boundary_signature(bits, side, 4)
        self.assertEqual(signature.tile_types, 2)
        self.assertEqual(signature.unresolved_groups, 1)
        self.assertEqual(signature.largest_unresolved_group, 2)

    def test_greedy_boundary_distinguishes_boundary_bits(self) -> None:
        bits = [0] * 16
        bits[0] = 1
        signature = greedy_boundary_signature(bits, 4, 2)
        self.assertEqual(signature.tile_types, 2)
        self.assertEqual(len(signature.selected_bits), 1)
        self.assertEqual(signature.unresolved_groups, 0)

    def test_random_control_is_deterministic(self) -> None:
        first, first_side = random_triangle_grid(32)
        second, second_side = random_triangle_grid(32)
        self.assertEqual(first_side, second_side)
        self.assertEqual(first, second)

    def test_active_cone_complement_leaves_padding_neutral(self) -> None:
        bits = [0] * 64
        complemented, side = active_cone_complement(bits, 8, 4)
        self.assertEqual(side, 8)
        self.assertEqual(sum(complemented), sum(2 * time + 1 for time in range(4)))
        self.assertEqual(complemented[0], 0)
        self.assertEqual(complemented[4], 1)
        self.assertEqual(sum(complemented[4 * side :]), 0)

    def test_square_transforms_are_exact(self) -> None:
        word = 0b0110
        self.assertEqual(transform_tile_word(word, 2, "mirror_lr"), 0b1001)
        rotated = transform_tile_word(word, 2, "rotate_90")
        self.assertEqual(transform_tile_word(rotated, 2, "rotate_270"), word)

    def test_symmetry_quotient_merges_mirror_pair(self) -> None:
        bits = [
            1, 0, 0, 1,
            0, 0, 0, 0,
            0, 0, 0, 0,
            0, 0, 0, 0,
        ]
        raw, mirrored, dihedral, fixed = symmetry_quotient(bits, 4, 2)
        self.assertEqual(raw, 3)
        self.assertEqual(mirrored, 2)
        self.assertLessEqual(dihedral, mirrored)
        self.assertGreaterEqual(fixed, 1)

    def test_directional_reuse_separates_axes(self) -> None:
        bits = []
        for row in range(8):
            bits.extend(([1, 0] * 4) if row < 2 else [0] * 8)
        reuse = directional_tile_reuse(bits, 8, 2)
        self.assertEqual(reuse.horizontal_equal, 3)
        self.assertGreater(reuse.horizontal_equal, reuse.vertical_equal)
        self.assertEqual(reuse.horizontal_periodic, 1)

    def test_unaligned_word_vocabulary_separates_axes(self) -> None:
        bits = [
            1, 0, 1, 0,
            1, 0, 1, 0,
            0, 1, 0, 1,
            0, 1, 0, 1,
        ]
        words = directional_word_vocabulary(bits, 4, 2)
        self.assertEqual(words.horizontal_types, 2)
        self.assertEqual(words.horizontal_reflection_types, 1)
        self.assertGreater(words.vertical_types, words.horizontal_reflection_types)

    def test_invalid_grid_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            build_tile_grammar([0, 1, 0], 2)


if __name__ == "__main__":
    unittest.main()
