from __future__ import annotations

import importlib.util
import unittest

from zero_tail_smt_certificate import build_certificate


@unittest.skipIf(importlib.util.find_spec("z3") is None, "z3-solver is not installed")
class ZeroTailSmtCertificateTests(unittest.TestCase):
    def test_every_negated_local_schema_is_unsatisfiable(self) -> None:
        certificate = build_certificate()
        self.assertEqual(certificate["status"], "PASS")
        self.assertEqual(len(certificate["obligations"]), 18)
        self.assertTrue(
            all(item["solver_result"] == "unsat" for item in certificate["obligations"])
        )


if __name__ == "__main__":
    unittest.main()
