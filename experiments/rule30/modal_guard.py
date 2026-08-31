"""Fail-closed admission and accounting for paid Rule 30 experiments.

This module deliberately does not import Modal or submit remote work.  It is a
local gate that must reserve a content-addressed experiment before a separate
runner may execute it.  Exact work units are unique in the lifetime SQLite
ledger, and a failed or ambiguous unit is never eligible for resubmission.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sqlite3
from contextlib import contextmanager
from dataclasses import dataclass
from datetime import date, datetime, timezone
from decimal import Decimal, InvalidOperation, ROUND_UP
from pathlib import Path
from typing import Any, Iterable, Iterator


SCHEMA = "crosstalk.rule30.modal-experiment.v1"
LIFETIME_BUDGET_USD = Decimal("200.00")
STAGE_CAPS_USD = {
    "calibration": Decimal("5.00"),
    "pilot": Decimal("20.00"),
    "expansion": Decimal("50.00"),
    "targeted": Decimal("100.00"),
    "verification": Decimal("200.00"),
}
STAGES = tuple(STAGE_CAPS_USD)
HEX_64 = re.compile(r"^[0-9a-f]{64}$")
FAMILY = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
ACTIVE_STATUSES = ("reserved", "submitted", "ambiguous")
FINAL_STATUSES = ("completed", "failed")


class GuardError(ValueError):
    """Raised when a manifest or ledger operation violates a safety gate."""


@dataclass(frozen=True)
class ValidatedManifest:
    document: dict[str, Any]
    canonical_json: str
    job_id: str
    work_units: tuple[tuple[str, str, str], ...]
    worst_case_cost_usd: Decimal


def _canonical(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def _digest(value: Any) -> str:
    return hashlib.sha256(_canonical(value).encode("utf-8")).hexdigest()


def _require_mapping(value: Any, field: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise GuardError(f"{field} must be an object")
    return value


def _require_list(value: Any, field: str, minimum: int = 1) -> list[Any]:
    if not isinstance(value, list) or len(value) < minimum:
        raise GuardError(f"{field} must contain at least {minimum} item(s)")
    return value


def _require_text(value: Any, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise GuardError(f"{field} must be non-empty text")
    return value.strip()


def _decimal(value: Any, field: str, *, positive: bool = False) -> Decimal:
    if not isinstance(value, str):
        raise GuardError(f"{field} must be a decimal string")
    try:
        parsed = Decimal(value)
    except InvalidOperation as error:
        raise GuardError(f"{field} is not a decimal") from error
    if not parsed.is_finite() or parsed < 0 or (positive and parsed <= 0):
        qualifier = "positive" if positive else "non-negative"
        raise GuardError(f"{field} must be finite and {qualifier}")
    return parsed


def _validate_no_floats(value: Any, field: str = "manifest") -> None:
    if isinstance(value, float):
        raise GuardError(f"{field} contains a binary float; use an integer or decimal string")
    if isinstance(value, dict):
        for key, child in value.items():
            _validate_no_floats(child, f"{field}.{key}")
    elif isinstance(value, list):
        for index, child in enumerate(value):
            _validate_no_floats(child, f"{field}[{index}]")


def load_manifest(path: Path) -> dict[str, Any]:
    try:
        document = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise GuardError(f"cannot read manifest {path}: {error}") from error
    return _require_mapping(document, "manifest")


def validate_manifest(
    document: dict[str, Any],
    *,
    repo_root: Path,
    today: date | None = None,
) -> ValidatedManifest:
    """Validate a preregistration and calculate its immutable identities."""

    _validate_no_floats(document)
    if document.get("schema") != SCHEMA:
        raise GuardError(f"schema must be {SCHEMA}")

    family = _require_text(document.get("analysis_family"), "analysis_family")
    if not FAMILY.fullmatch(family):
        raise GuardError("analysis_family must be stable lowercase kebab-case")
    stage = _require_text(document.get("stage"), "stage")
    if stage not in STAGE_CAPS_USD:
        raise GuardError(f"stage must be one of {', '.join(STAGES)}")
    purpose = _require_text(document.get("purpose"), "purpose")
    if purpose not in ("infrastructure", "discovery", "independent-verification"):
        raise GuardError("purpose is not recognized")
    if stage == "calibration" and purpose != "infrastructure":
        raise GuardError("calibration may use only synthetic infrastructure work")
    if stage == "verification" and purpose != "independent-verification":
        raise GuardError("verification must use purpose independent-verification")

    _require_text(document.get("title"), "title")
    hypothesis = _require_text(document.get("hypothesis"), "hypothesis")
    question = _require_text(document.get("unresolved_question"), "unresolved_question")
    outcomes = _require_list(document.get("predicted_outcomes"), "predicted_outcomes", 2)
    decisions: set[str] = set()
    for index, raw_outcome in enumerate(outcomes):
        outcome = _require_mapping(raw_outcome, f"predicted_outcomes[{index}]")
        _require_text(outcome.get("outcome"), f"predicted_outcomes[{index}].outcome")
        decisions.add(
            _require_text(
                outcome.get("next_decision"),
                f"predicted_outcomes[{index}].next_decision",
            )
        )
    if len(decisions) < 2:
        raise GuardError("predicted outcomes must lead to at least two different decisions")
    for index, criterion in enumerate(
        _require_list(document.get("kill_criteria"), "kill_criteria")
    ):
        _require_text(criterion, f"kill_criteria[{index}]")

    novelty = _require_mapping(document.get("novelty"), "novelty")
    searched_at_text = _require_text(novelty.get("searched_at"), "novelty.searched_at")
    try:
        searched_at = date.fromisoformat(searched_at_text)
    except ValueError as error:
        raise GuardError("novelty.searched_at must be YYYY-MM-DD") from error
    current_date = today or datetime.now(timezone.utc).date()
    age_days = (current_date - searched_at).days
    if age_days < 0 or age_days > 30:
        raise GuardError("prior-art search must be no more than 30 days old")
    queries = _require_list(novelty.get("queries"), "novelty.queries", 2)
    for index, query in enumerate(queries):
        _require_text(query, f"novelty.queries[{index}]")
    sources = _require_list(novelty.get("sources"), "novelty.sources", 2)
    source_urls: set[str] = set()
    for index, raw_source in enumerate(sources):
        source = _require_mapping(raw_source, f"novelty.sources[{index}]")
        _require_text(source.get("title"), f"novelty.sources[{index}].title")
        url = _require_text(source.get("url"), f"novelty.sources[{index}].url")
        if not url.startswith("https://"):
            raise GuardError(f"novelty.sources[{index}].url must use https")
        source_urls.add(url)
        _require_text(source.get("finding"), f"novelty.sources[{index}].finding")
        snapshot = _require_text(
            source.get("snapshot_sha256"),
            f"novelty.sources[{index}].snapshot_sha256",
        )
        if not HEX_64.fullmatch(snapshot):
            raise GuardError(f"novelty.sources[{index}].snapshot_sha256 is invalid")
    if len(source_urls) != len(sources):
        raise GuardError("novelty sources must be distinct")
    _require_text(novelty.get("closest_prior_art"), "novelty.closest_prior_art")
    _require_text(novelty.get("novel_delta"), "novelty.novel_delta")
    if novelty.get("negative_ledger_checked") is not True:
        raise GuardError("novelty.negative_ledger_checked must be true")
    ledger_paths = _require_list(
        novelty.get("local_negative_ledger"),
        "novelty.local_negative_ledger",
    )
    for index, raw_path in enumerate(ledger_paths):
        relative = Path(_require_text(raw_path, f"novelty.local_negative_ledger[{index}]"))
        if relative.is_absolute() or ".." in relative.parts:
            raise GuardError("negative-ledger paths must stay within the repository")
        if not (repo_root / relative).is_file():
            raise GuardError(f"negative-ledger path does not exist: {relative}")

    prerequisites = document.get("prerequisite_job_ids", [])
    if not isinstance(prerequisites, list):
        raise GuardError("prerequisite_job_ids must be a list")
    for index, job_id in enumerate(prerequisites):
        if not isinstance(job_id, str) or not HEX_64.fullmatch(job_id):
            raise GuardError(f"prerequisite_job_ids[{index}] is invalid")
    if stage != "calibration" and not prerequisites:
        raise GuardError("paid scientific stages require an explicitly completed prerequisite")
    independent_from = document.get("independent_from_job_id")
    if stage == "verification":
        if not isinstance(independent_from, str) or not HEX_64.fullmatch(independent_from):
            raise GuardError("verification requires a valid independent_from_job_id")
        if independent_from not in prerequisites:
            raise GuardError("independent_from_job_id must also be a prerequisite")
    elif independent_from is not None:
        raise GuardError("independent_from_job_id is valid only for verification")

    execution = _require_mapping(document.get("execution"), "execution")
    if execution.get("backend") != "modal-sandbox":
        raise GuardError("execution.backend must be modal-sandbox to avoid preemption retries")
    if execution.get("network_access") is not False:
        raise GuardError("paid workers must not have network access")
    if execution.get("gpu") is not False:
        raise GuardError("GPU work is prohibited until a separate measured justification exists")
    if execution.get("retries") != 0:
        raise GuardError("execution.retries must be zero")
    if execution.get("resubmit_ambiguous") is not False:
        raise GuardError("ambiguous failures must never be resubmitted")
    code_sha = _require_text(execution.get("code_sha256"), "execution.code_sha256")
    runtime_sha = _require_text(
        execution.get("runtime_spec_sha256"), "execution.runtime_spec_sha256"
    )
    if not HEX_64.fullmatch(code_sha) or not HEX_64.fullmatch(runtime_sha):
        raise GuardError("code and runtime specification hashes must be lowercase SHA-256")
    algorithm_version = _require_text(
        execution.get("algorithm_version"), "execution.algorithm_version"
    )
    solver_versions = _require_mapping(
        execution.get("solver_versions"), "execution.solver_versions"
    )
    if not solver_versions:
        raise GuardError("execution.solver_versions must not be empty")
    for name, version in solver_versions.items():
        _require_text(name, "execution.solver_versions key")
        _require_text(version, f"execution.solver_versions.{name}")
    random_seed = execution.get("random_seed")
    if not isinstance(random_seed, int) or isinstance(random_seed, bool) or random_seed < 0:
        raise GuardError("execution.random_seed must be a non-negative integer")

    cpu_cores = _decimal(execution.get("cpu_cores"), "execution.cpu_cores", positive=True)
    memory_gib = _decimal(execution.get("memory_gib"), "execution.memory_gib", positive=True)
    timeout = execution.get("timeout_seconds")
    if not isinstance(timeout, int) or isinstance(timeout, bool) or not 1 <= timeout <= 3600:
        raise GuardError("execution.timeout_seconds must be an integer from 1 through 3600")
    safety_multiplier = _decimal(
        execution.get("safety_multiplier"),
        "execution.safety_multiplier",
        positive=True,
    )
    if safety_multiplier < Decimal("1.25"):
        raise GuardError("execution.safety_multiplier must be at least 1.25")

    rate = _require_mapping(execution.get("rate_snapshot"), "execution.rate_snapshot")
    captured_at_text = _require_text(
        rate.get("captured_at"), "execution.rate_snapshot.captured_at"
    )
    try:
        captured_at = datetime.fromisoformat(captured_at_text.replace("Z", "+00:00"))
    except ValueError as error:
        raise GuardError("execution.rate_snapshot.captured_at must be ISO-8601") from error
    rate_age_days = (current_date - captured_at.date()).days
    if rate_age_days < 0 or rate_age_days > 1:
        raise GuardError("Modal rate snapshot must be no more than one day old")
    if rate.get("source") != "modal billing rates --json":
        raise GuardError("rates must come from `modal billing rates --json`")
    cpu_rate = _decimal(
        rate.get("cpu_core_second_usd"),
        "execution.rate_snapshot.cpu_core_second_usd",
        positive=True,
    )
    memory_rate = _decimal(
        rate.get("memory_gib_second_usd"),
        "execution.rate_snapshot.memory_gib_second_usd",
        positive=True,
    )
    fixed_overhead = _decimal(
        rate.get("fixed_overhead_usd"),
        "execution.rate_snapshot.fixed_overhead_usd",
    )

    raw_units = _require_list(execution.get("work_units"), "execution.work_units")
    analysis_core = {
        "schema": SCHEMA,
        "analysis_family": family,
        "purpose": purpose,
        "code_sha256": code_sha,
        "runtime_spec_sha256": runtime_sha,
        "algorithm_version": algorithm_version,
        "solver_versions": solver_versions,
        "random_seed": random_seed,
    }
    units: list[tuple[str, str, str]] = []
    seen_unit_ids: set[str] = set()
    seen_unit_hashes: set[str] = set()
    for index, raw_unit in enumerate(raw_units):
        unit = _require_mapping(raw_unit, f"execution.work_units[{index}]")
        unit_id = _require_text(unit.get("id"), f"execution.work_units[{index}].id")
        if unit_id in seen_unit_ids:
            raise GuardError(f"duplicate work-unit id in manifest: {unit_id}")
        seen_unit_ids.add(unit_id)
        if "payload" not in unit:
            raise GuardError(f"execution.work_units[{index}].payload is required")
        payload_json = _canonical(unit["payload"])
        unit_hash = _digest({"analysis": analysis_core, "payload": unit["payload"]})
        if unit_hash in seen_unit_hashes:
            raise GuardError("two work units describe the same analysis payload")
        seen_unit_hashes.add(unit_hash)
        units.append((unit_hash, unit_id, payload_json))

    per_second = cpu_cores * cpu_rate + memory_gib * memory_rate
    raw_cost = per_second * Decimal(timeout) * Decimal(len(units)) + fixed_overhead
    reserve = (raw_cost * safety_multiplier).quantize(Decimal("0.000001"), rounding=ROUND_UP)
    if reserve <= 0:
        raise GuardError("calculated reservation must be positive")

    job_identity = {
        "analysis": analysis_core,
        "hypothesis": hypothesis,
        "unresolved_question": question,
        "work_unit_hashes": sorted(seen_unit_hashes),
    }
    canonical = _canonical(document)
    return ValidatedManifest(
        document=document,
        canonical_json=canonical,
        job_id=_digest(job_identity),
        work_units=tuple(units),
        worst_case_cost_usd=reserve,
    )


@contextmanager
def connect_ledger(path: Path) -> Iterator[sqlite3.Connection]:
    path.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(path)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    connection.executescript(
        """
        CREATE TABLE IF NOT EXISTS jobs (
            job_id TEXT PRIMARY KEY,
            analysis_family TEXT NOT NULL,
            stage TEXT NOT NULL,
            purpose TEXT NOT NULL,
            manifest_json TEXT NOT NULL,
            status TEXT NOT NULL,
            reserved_usd TEXT NOT NULL,
            actual_usd TEXT,
            external_id TEXT,
            result_sha256 TEXT,
            gate_passed INTEGER,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS work_units (
            unit_hash TEXT PRIMARY KEY,
            job_id TEXT NOT NULL REFERENCES jobs(job_id),
            unit_id TEXT NOT NULL,
            payload_json TEXT NOT NULL
        );
        """
    )
    try:
        yield connection
    finally:
        connection.close()


def _committed_total(connection: sqlite3.Connection) -> Decimal:
    total = Decimal("0")
    for row in connection.execute("SELECT status, reserved_usd, actual_usd FROM jobs"):
        if row["status"] in ACTIVE_STATUSES:
            total += Decimal(row["reserved_usd"])
        elif row["status"] in FINAL_STATUSES:
            actual = row["actual_usd"]
            total += Decimal(actual if actual is not None else row["reserved_usd"])
        else:
            raise GuardError(f"ledger contains unknown status {row['status']}")
    return total


def _check_prerequisites(
    connection: sqlite3.Connection,
    manifest: ValidatedManifest,
) -> None:
    stage = manifest.document["stage"]
    if stage == "calibration":
        return
    prerequisite_ids = manifest.document["prerequisite_job_ids"]
    previous_rank = STAGES.index(stage) - 1
    has_immediate_predecessor = False
    for job_id in prerequisite_ids:
        row = connection.execute(
            "SELECT stage, status, gate_passed FROM jobs WHERE job_id = ?",
            (job_id,),
        ).fetchone()
        if row is None:
            raise GuardError(f"prerequisite is absent from ledger: {job_id}")
        if row["status"] != "completed" or row["gate_passed"] != 1:
            raise GuardError(f"prerequisite did not complete and pass its gate: {job_id}")
        if STAGES.index(row["stage"]) == previous_rank:
            has_immediate_predecessor = True
    if not has_immediate_predecessor:
        raise GuardError(f"stage {stage} requires a passed {STAGES[previous_rank]} job")
    if stage == "verification":
        independent_id = manifest.document["independent_from_job_id"]
        prior = connection.execute(
            "SELECT manifest_json FROM jobs WHERE job_id = ?", (independent_id,)
        ).fetchone()
        if prior is None:
            raise GuardError("independent verification target is absent from ledger")
        prior_manifest = json.loads(prior["manifest_json"])
        current_execution = manifest.document["execution"]
        prior_execution = prior_manifest["execution"]
        if current_execution["code_sha256"] == prior_execution["code_sha256"]:
            raise GuardError("verification must use an independent code implementation")
        if current_execution["algorithm_version"] == prior_execution["algorithm_version"]:
            raise GuardError("verification must use an independent algorithm")


def reserve_manifest(
    connection: sqlite3.Connection,
    manifest: ValidatedManifest,
    *,
    lifetime_budget_usd: Decimal = LIFETIME_BUDGET_USD,
) -> None:
    """Atomically reserve a unique manifest against the staged lifetime cap."""

    if lifetime_budget_usd > LIFETIME_BUDGET_USD:
        raise GuardError("configured lifetime budget may not exceed the authorized $200")
    stage = manifest.document["stage"]
    cap = min(STAGE_CAPS_USD[stage], lifetime_budget_usd)
    now = datetime.now(timezone.utc).isoformat()
    try:
        connection.execute("BEGIN IMMEDIATE")
        if connection.execute(
            "SELECT 1 FROM jobs WHERE job_id = ?", (manifest.job_id,)
        ).fetchone():
            raise GuardError(f"experiment was already admitted: {manifest.job_id}")
        for unit_hash, unit_id, _ in manifest.work_units:
            prior = connection.execute(
                "SELECT job_id FROM work_units WHERE unit_hash = ?", (unit_hash,)
            ).fetchone()
            if prior is not None:
                raise GuardError(
                    f"work unit {unit_id} duplicates prior job {prior['job_id']}"
                )
        _check_prerequisites(connection, manifest)
        projected = _committed_total(connection) + manifest.worst_case_cost_usd
        if projected > cap:
            raise GuardError(
                f"reservation would commit ${projected} beyond {stage} cap ${cap}"
            )
        connection.execute(
            """
            INSERT INTO jobs (
                job_id, analysis_family, stage, purpose, manifest_json, status,
                reserved_usd, created_at, updated_at
            ) VALUES (?, ?, ?, ?, ?, 'reserved', ?, ?, ?)
            """,
            (
                manifest.job_id,
                manifest.document["analysis_family"],
                stage,
                manifest.document["purpose"],
                manifest.canonical_json,
                str(manifest.worst_case_cost_usd),
                now,
                now,
            ),
        )
        connection.executemany(
            "INSERT INTO work_units (unit_hash, job_id, unit_id, payload_json) VALUES (?, ?, ?, ?)",
            (
                (unit_hash, manifest.job_id, unit_id, payload_json)
                for unit_hash, unit_id, payload_json in manifest.work_units
            ),
        )
        connection.commit()
    except Exception:
        connection.rollback()
        raise


def mark_submitted(connection: sqlite3.Connection, job_id: str, external_id: str) -> None:
    external_id = _require_text(external_id, "external_id")
    now = datetime.now(timezone.utc).isoformat()
    cursor = connection.execute(
        """
        UPDATE jobs SET status = 'submitted', external_id = ?, updated_at = ?
        WHERE job_id = ? AND status = 'reserved'
        """,
        (external_id, now, job_id),
    )
    if cursor.rowcount != 1:
        connection.rollback()
        raise GuardError("job is absent or is not in reserved state")
    connection.commit()


def record_terminal(
    connection: sqlite3.Connection,
    job_id: str,
    *,
    status: str,
    actual_cost_usd: Decimal | None = None,
    result_sha256: str | None = None,
    gate_passed: bool = False,
) -> None:
    if status not in ("completed", "failed", "ambiguous"):
        raise GuardError("terminal status must be completed, failed, or ambiguous")
    if status == "completed":
        if actual_cost_usd is None or result_sha256 is None:
            raise GuardError("completed jobs require actual cost and a result hash")
        if not HEX_64.fullmatch(result_sha256):
            raise GuardError("result_sha256 is invalid")
    elif gate_passed:
        raise GuardError("only completed jobs may pass a stage gate")
    if actual_cost_usd is not None and actual_cost_usd < 0:
        raise GuardError("actual cost must be non-negative")
    row = connection.execute(
        "SELECT status FROM jobs WHERE job_id = ?", (job_id,)
    ).fetchone()
    if row is None or row["status"] not in ("reserved", "submitted"):
        raise GuardError("job is absent or already terminal")
    now = datetime.now(timezone.utc).isoformat()
    connection.execute(
        """
        UPDATE jobs
        SET status = ?, actual_usd = ?, result_sha256 = ?, gate_passed = ?, updated_at = ?
        WHERE job_id = ?
        """,
        (
            status,
            None if actual_cost_usd is None else str(actual_cost_usd),
            result_sha256,
            1 if gate_passed else 0,
            now,
            job_id,
        ),
    )
    connection.commit()


def ledger_summary(connection: sqlite3.Connection) -> dict[str, Any]:
    jobs = []
    for row in connection.execute(
        "SELECT job_id, analysis_family, stage, status, reserved_usd, actual_usd, gate_passed "
        "FROM jobs ORDER BY created_at, job_id"
    ):
        jobs.append(dict(row))
    committed = _committed_total(connection)
    return {
        "authorized_lifetime_budget_usd": str(LIFETIME_BUDGET_USD),
        "committed_usd": str(committed),
        "remaining_uncommitted_usd": str(LIFETIME_BUDGET_USD - committed),
        "jobs": jobs,
    }


def _print_json(value: Any) -> None:
    print(json.dumps(value, indent=2, sort_keys=True))


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    for command in ("validate", "reserve"):
        child = subparsers.add_parser(command)
        child.add_argument("manifest", type=Path)
        child.add_argument("--repo-root", type=Path, default=Path.cwd())
        if command == "reserve":
            child.add_argument("--ledger", type=Path, required=True)
    status = subparsers.add_parser("status")
    status.add_argument("--ledger", type=Path, required=True)
    submitted = subparsers.add_parser("mark-submitted")
    submitted.add_argument("job_id")
    submitted.add_argument("external_id")
    submitted.add_argument("--ledger", type=Path, required=True)
    terminal = subparsers.add_parser("record-terminal")
    terminal.add_argument("job_id")
    terminal.add_argument("status", choices=("completed", "failed", "ambiguous"))
    terminal.add_argument("--actual-cost-usd")
    terminal.add_argument("--result-sha256")
    terminal.add_argument("--gate-passed", action="store_true")
    terminal.add_argument("--ledger", type=Path, required=True)
    return parser


def main(argv: Iterable[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    try:
        if args.command in ("validate", "reserve"):
            validated = validate_manifest(
                load_manifest(args.manifest), repo_root=args.repo_root.resolve()
            )
            if args.command == "reserve":
                with connect_ledger(args.ledger) as connection:
                    reserve_manifest(connection, validated)
            _print_json(
                {
                    "job_id": validated.job_id,
                    "stage": validated.document["stage"],
                    "work_units": len(validated.work_units),
                    "worst_case_reservation_usd": str(validated.worst_case_cost_usd),
                    "status": "reserved" if args.command == "reserve" else "valid",
                }
            )
        elif args.command == "status":
            with connect_ledger(args.ledger) as connection:
                _print_json(ledger_summary(connection))
        elif args.command == "mark-submitted":
            with connect_ledger(args.ledger) as connection:
                mark_submitted(connection, args.job_id, args.external_id)
        elif args.command == "record-terminal":
            actual = (
                None
                if args.actual_cost_usd is None
                else _decimal(args.actual_cost_usd, "actual_cost_usd")
            )
            with connect_ledger(args.ledger) as connection:
                record_terminal(
                    connection,
                    args.job_id,
                    status=args.status,
                    actual_cost_usd=actual,
                    result_sha256=args.result_sha256,
                    gate_passed=args.gate_passed,
                )
        else:  # pragma: no cover - argparse makes this unreachable
            raise GuardError("unknown command")
    except GuardError as error:
        print(f"ERROR: {error}")
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
