from __future__ import annotations

import copy
import hashlib
import tempfile
import unittest
from datetime import date
from decimal import Decimal
from pathlib import Path

from modal_guard import (
    GuardError,
    backfill_unadmitted,
    connect_ledger,
    ledger_summary,
    mark_submitted,
    record_terminal,
    reserve_manifest,
    validate_manifest,
)


SHA_A = "a" * 64
SHA_B = "b" * 64
SHA_C = "c" * 64


def manifest(*, stage: str = "calibration", purpose: str = "infrastructure") -> dict:
    return {
        "schema": "crosstalk.rule30.modal-experiment.v1",
        "analysis_family": "guard-synthetic-calibration",
        "stage": stage,
        "purpose": purpose,
        "title": "Synthetic admission-path calibration",
        "hypothesis": "The admission path records one synthetic unit exactly once.",
        "unresolved_question": "Does the local guard preserve its accounting invariants?",
        "predicted_outcomes": [
            {"outcome": "The synthetic check passes.", "next_decision": "Admit a pilot."},
            {"outcome": "The synthetic check fails.", "next_decision": "Repair the guard."},
        ],
        "kill_criteria": ["Stop after the first deterministic synthetic result."],
        "prerequisite_job_ids": [],
        "novelty": {
            "searched_at": "2026-08-27",
            "queries": ["synthetic guard check", "content addressed experiment ledger"],
            "sources": [
                {
                    "title": "Source A",
                    "url": "https://example.com/a",
                    "finding": "No scientific computation is contained in this calibration.",
                    "snapshot_sha256": SHA_A,
                },
                {
                    "title": "Source B",
                    "url": "https://example.com/b",
                    "finding": "The calibration uses synthetic inputs only.",
                    "snapshot_sha256": SHA_B,
                },
            ],
            "closest_prior_art": "Not applicable to a synthetic infrastructure check.",
            "novel_delta": "This checks only the local admission path.",
            "negative_ledger_checked": True,
            "local_negative_ledger": ["negative.md"],
        },
        "execution": {
            "backend": "modal-sandbox",
            "network_access": False,
            "gpu": False,
            "retries": 0,
            "resubmit_ambiguous": False,
            "code_sha256": SHA_A,
            "runtime_spec_sha256": SHA_B,
            "algorithm_version": "synthetic-v1",
            "solver_versions": {"python": "3.13"},
            "random_seed": 0,
            "cpu_cores": "1",
            "memory_gib": "1",
            "timeout_seconds": 10,
            "safety_multiplier": "1.25",
            "rate_snapshot": {
                "captured_at": "2026-08-27T12:00:00Z",
                "source": "modal billing rates --json",
                "cpu_core_second_usd": "0.01",
                "memory_gib_second_usd": "0.001",
                "fixed_overhead_usd": "0",
            },
            "work_units": [{"id": "synthetic-1", "payload": {"value": 1}}],
        },
    }


class ModalGuardTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        (self.root / "negative.md").write_text("bounded negatives\n", encoding="utf-8")
        self.today = date(2026, 8, 27)

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def validate(self, document: dict):
        return validate_manifest(document, repo_root=self.root, today=self.today)

    def test_valid_manifest_has_stable_identity_and_cost(self) -> None:
        first = self.validate(manifest())
        second_document = copy.deepcopy(manifest())
        second_document["title"] = "Cosmetically renamed calibration"
        second_document["execution"]["rate_snapshot"]["cpu_core_second_usd"] = "0.02"
        second = self.validate(second_document)
        self.assertEqual(first.job_id, second.job_id)
        self.assertNotEqual(first.worst_case_cost_usd, second.worst_case_cost_usd)
        self.assertEqual(first.worst_case_cost_usd, Decimal("0.137500"))

    def test_value_of_information_requires_distinct_decisions(self) -> None:
        document = manifest()
        document["predicted_outcomes"][1]["next_decision"] = "Admit a pilot."
        with self.assertRaisesRegex(GuardError, "different decisions"):
            self.validate(document)

    def test_stale_prior_art_search_is_rejected(self) -> None:
        document = manifest()
        document["novelty"]["searched_at"] = "2026-06-01"
        with self.assertRaisesRegex(GuardError, "30 days"):
            self.validate(document)

    def test_stale_rate_snapshot_is_rejected(self) -> None:
        document = manifest()
        document["execution"]["rate_snapshot"]["captured_at"] = "2026-08-01T00:00:00Z"
        with self.assertRaisesRegex(GuardError, "rate snapshot"):
            self.validate(document)

    def test_network_gpu_retries_and_resubmission_are_fail_closed(self) -> None:
        cases = (
            ("network_access", True, "network access"),
            # `gpu` is now a device name rather than a flag, so a bare True is
            # rejected for not naming a device. It is still fail-closed.
            ("gpu", True, "execution.gpu must be non-empty text"),
            ("retries", 1, "retries must be zero"),
            ("resubmit_ambiguous", True, "never be resubmitted"),
        )
        for field, value, message in cases:
            with self.subTest(field=field):
                document = manifest()
                document["execution"][field] = value
                with self.assertRaisesRegex(GuardError, message):
                    self.validate(document)

    def _gpu_manifest(self) -> dict:
        """A manifest naming a device, with a complete measured justification."""
        document = manifest()
        execution = document["execution"]
        execution["gpu"] = "H100"
        execution["gpu_measured_justification"] = {
            "device": "H100",
            "measured_throughput": "1.06e14 cell-updates/s at R=16 H=16 W=4",
            "validated_against": "WDR 1,980,000 bits bit-exact; OEIS b051023 100,001 bits",
            "evidence": ["negative.md"],
        }
        execution["rate_snapshot"]["gpu_second_usd"] = "0.0011"
        return document

    def test_gpu_requires_a_measured_justification(self) -> None:
        """Naming a device is not enough; the justification gates admission."""
        document = self._gpu_manifest()
        del document["execution"]["gpu_measured_justification"]
        with self.assertRaisesRegex(GuardError, "gpu_measured_justification"):
            self.validate(document)

    def test_gpu_justification_must_name_the_same_device(self) -> None:
        document = self._gpu_manifest()
        document["execution"]["gpu_measured_justification"]["device"] = "A100"
        with self.assertRaisesRegex(GuardError, "must name the same device"):
            self.validate(document)

    def test_gpu_evidence_must_resolve_in_repo(self) -> None:
        """The justification's evidence is checked to exist, as prior art is."""
        document = self._gpu_manifest()
        document["execution"]["gpu_measured_justification"]["evidence"] = ["absent.md"]
        with self.assertRaisesRegex(GuardError, "GPU evidence path does not exist"):
            self.validate(document)
        document["execution"]["gpu_measured_justification"]["evidence"] = ["../escape.md"]
        with self.assertRaisesRegex(GuardError, "must stay within the repository"):
            self.validate(document)

    def test_gpu_requires_a_device_rate_and_charges_for_it(self) -> None:
        """Without a device rate the reservation would understate the run."""
        document = self._gpu_manifest()
        del document["execution"]["rate_snapshot"]["gpu_second_usd"]
        with self.assertRaisesRegex(GuardError, "gpu_second_usd"):
            self.validate(document)

        # A priced GPU manifest is admitted, and the device is billed for the
        # full timeout on top of CPU and memory rather than ignored.
        cpu_only = self.validate(manifest()).worst_case_cost_usd
        with_gpu = self.validate(self._gpu_manifest()).worst_case_cost_usd
        self.assertGreater(with_gpu, cpu_only)
        # 10 s timeout x 1 unit x $0.0011/s x 1.25 safety = $0.01375 of device.
        self.assertEqual(with_gpu - cpu_only, Decimal("0.013750"))

    def test_backfilled_spend_counts_against_later_reservations(self) -> None:
        """In-arrears spend is real money and must constrain what follows."""
        ledger = self.root / "ledger.sqlite3"
        with connect_ledger(ledger) as connection:
            job_id = backfill_unadmitted(
                connection,
                analysis_family="rule30-deep-simulation",
                stage="calibration",
                note="ran before the guard was consulted",
                actual_cost_usd=Decimal("1.89"),
            )
            summary = ledger_summary(connection)
            self.assertEqual(summary["committed_usd"], "1.89")
            # Booked as spent, and explicitly not as an admitted experiment.
            row = connection.execute(
                "SELECT status, manifest_json FROM jobs WHERE job_id = ?", (job_id,)
            ).fetchone()
            self.assertEqual(row["status"], "completed")
            self.assertIn('"admitted":false', row["manifest_json"].replace(" ", ""))

            # The same breach cannot be booked twice.
            with self.assertRaisesRegex(GuardError, "already backfilled"):
                backfill_unadmitted(
                    connection,
                    analysis_family="rule30-deep-simulation",
                    stage="calibration",
                    note="ran before the guard was consulted",
                    actual_cost_usd=Decimal("1.89"),
                )

    def test_backfill_cannot_exceed_the_lifetime_ceiling(self) -> None:
        with connect_ledger(self.root / "ledger.sqlite3") as connection:
            with self.assertRaisesRegex(GuardError, "beyond"):
                backfill_unadmitted(
                    connection,
                    analysis_family="rule30-deep-simulation",
                    stage="calibration",
                    note="implausible",
                    actual_cost_usd=Decimal("250.00"),
                )

    def test_duplicate_job_and_duplicate_work_unit_are_rejected(self) -> None:
        validated = self.validate(manifest())
        with connect_ledger(self.root / "ledger.sqlite3") as connection:
            reserve_manifest(connection, validated)
            with self.assertRaisesRegex(GuardError, "already admitted"):
                reserve_manifest(connection, validated)

            renamed = manifest()
            renamed["hypothesis"] = "Different prose describing the same execution."
            renamed["unresolved_question"] = "Different prose question."
            duplicate_unit = self.validate(renamed)
            self.assertNotEqual(validated.job_id, duplicate_unit.job_id)
            with self.assertRaisesRegex(GuardError, "duplicates prior job"):
                reserve_manifest(connection, duplicate_unit)

    def test_stage_cap_is_enforced_from_worst_case_reservation(self) -> None:
        document = manifest()
        document["execution"]["timeout_seconds"] = 3600
        validated = self.validate(document)
        self.assertGreater(validated.worst_case_cost_usd, Decimal("5"))
        with connect_ledger(self.root / "ledger.sqlite3") as connection:
            with self.assertRaisesRegex(GuardError, "calibration cap"):
                reserve_manifest(connection, validated)

    def test_pilot_requires_passed_calibration(self) -> None:
        calibration = self.validate(manifest())
        with connect_ledger(self.root / "ledger.sqlite3") as connection:
            reserve_manifest(connection, calibration)

            pilot_document = manifest(stage="pilot", purpose="discovery")
            pilot_document["analysis_family"] = "periodic-center-contradiction"
            pilot_document["prerequisite_job_ids"] = [calibration.job_id]
            pilot_document["execution"]["code_sha256"] = SHA_C
            pilot_document["execution"]["work_units"] = [
                {"id": "period-1", "payload": {"period": 1}}
            ]
            pilot = self.validate(pilot_document)
            with self.assertRaisesRegex(GuardError, "did not complete"):
                reserve_manifest(connection, pilot)

            mark_submitted(connection, calibration.job_id, "synthetic-call")
            record_terminal(
                connection,
                calibration.job_id,
                status="completed",
                actual_cost_usd=Decimal("0.01"),
                result_sha256=hashlib.sha256(b"pass").hexdigest(),
                gate_passed=True,
            )
            reserve_manifest(connection, pilot)
            self.assertEqual(len(ledger_summary(connection)["jobs"]), 2)

    def test_verification_requires_named_independent_target(self) -> None:
        document = manifest(stage="verification", purpose="independent-verification")
        document["prerequisite_job_ids"] = [SHA_A]
        with self.assertRaisesRegex(GuardError, "independent_from_job_id"):
            self.validate(document)

    def test_ambiguous_failure_remains_fully_reserved_and_cannot_repeat(self) -> None:
        validated = self.validate(manifest())
        with connect_ledger(self.root / "ledger.sqlite3") as connection:
            reserve_manifest(connection, validated)
            mark_submitted(connection, validated.job_id, "call-1")
            record_terminal(connection, validated.job_id, status="ambiguous")
            summary = ledger_summary(connection)
            self.assertEqual(
                Decimal(summary["committed_usd"]), validated.worst_case_cost_usd
            )
            with self.assertRaisesRegex(GuardError, "already admitted"):
                reserve_manifest(connection, validated)


if __name__ == "__main__":
    unittest.main()
