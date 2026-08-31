from __future__ import annotations

import unittest

from boundary_signature_probe import parse_powers


class BoundarySignatureProbeTests(unittest.TestCase):
    def test_parse_powers_sorts_and_deduplicates(self) -> None:
        self.assertEqual(parse_powers([16, 4, 16, 8], "values"), [4, 8, 16])

    def test_parse_powers_rejects_non_power(self) -> None:
        with self.assertRaises(ValueError):
            parse_powers([4, 12], "values")


if __name__ == "__main__":
    unittest.main()
