"""Reproducible validation and analysis artifact writers."""

from __future__ import annotations

import csv
import hashlib
import importlib.metadata
import json
import platform
import sys
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable, Mapping, Sequence

import mpmath as mp

from source.analysis import (
    build_end_bounded_intervals,
    build_jump_metrics,
    interval_to_dict,
    jump_to_dict,
    summarize_analysis,
)
from source.models import MaximalGapRecord
from source.plots import plot_all
from source.prime_gap_list import (
    DEFAULT_EXHAUSTIVE_LIMIT,
    EXHAUSTIVE_LIMIT_AS_OF,
    EXHAUSTIVE_LIMIT_SOURCE_URL,
    load_and_select_records,
    validate_upstream_schema,
)
from source.provenance import require_experiment_approval, sha256_file
from source.definitions import WORKING_DPS


RECORD_FIELDS = [
    "record_index",
    "start_prime",
    "gap",
    "end_prime",
    "source_id",
    "source_row_id",
    "source_commit",
    "verified_exhaustive_limit",
]


def _package_version(distribution: str) -> str:
    try:
        return importlib.metadata.version(distribution)
    except importlib.metadata.PackageNotFoundError:
        return "NOT_INSTALLED"


def _code_snapshot() -> dict[str, object]:
    root = Path(__file__).resolve().parents[1]
    paths = list((root / "source").glob("*.py"))
    for relative_path in ("run_experiment.ps1", "requirements.txt", "environment.yml"):
        candidate = root / relative_path
        if candidate.exists():
            paths.append(candidate)
    paths.sort(key=lambda path: path.relative_to(root).as_posix())

    digest = hashlib.sha256()
    relative_paths: list[str] = []
    for path in paths:
        relative = path.relative_to(root).as_posix()
        relative_paths.append(relative)
        digest.update(relative.encode("utf-8"))
        digest.update(b"\0")
        digest.update(path.read_bytes())
        digest.update(b"\0")
    return {
        "code_sha256": digest.hexdigest(),
        "code_files": relative_paths,
    }


def _execution_metadata() -> dict[str, object]:
    return {
        "python_executable": sys.executable,
        "python_version": platform.python_version(),
        "platform": platform.platform(),
        "mpmath_version": _package_version("mpmath"),
        "matplotlib_version": _package_version("matplotlib"),
        "gmpy2_version": _package_version("gmpy2"),
        "mpmath_dps": mp.mp.dps,
        "minimum_working_dps": WORKING_DPS,
    } | _code_snapshot()


def _write_json_exclusive(path: Path, value: Mapping[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    serialized = json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    with path.open("x", encoding="utf-8", newline="\n") as handle:
        handle.write(serialized)


def _write_csv_exclusive(
    path: Path,
    rows: Iterable[Mapping[str, object]],
    fieldnames: Sequence[str],
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def _record_to_csv(record: MaximalGapRecord) -> dict[str, object]:
    row = asdict(record)
    for key in (
        "record_index",
        "start_prime",
        "gap",
        "end_prime",
        "verified_exhaustive_limit",
    ):
        row[key] = str(row[key])
    return row


def validate_raw_dataset(
    raw_path: Path,
    metadata_path: Path,
    output_directory: Path,
    *,
    approval_token: str | None,
    exhaustive_limit: int = DEFAULT_EXHAUSTIVE_LIMIT,
) -> tuple[Path, Path, list[MaximalGapRecord], dict[str, object]]:
    """Validate raw input and write immutable normalized records/report files."""

    require_experiment_approval(approval_token)
    metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
    commit = str(metadata.get("commit", ""))
    expected_hash = str(metadata.get("sha256", ""))
    actual_hash = sha256_file(raw_path)
    if actual_hash != expected_hash:
        raise RuntimeError("raw dataset SHA-256 does not match acquisition metadata")

    file_metadata = metadata.get("files")
    if not isinstance(file_metadata, dict):
        raise RuntimeError("acquisition metadata does not contain per-file provenance")
    raw_metadata = file_metadata.get("allgaps.sql")
    if not isinstance(raw_metadata, dict) or raw_metadata.get("sha256") != expected_hash:
        raise RuntimeError("allgaps.sql per-file provenance disagrees with metadata")
    schema_metadata = file_metadata.get("schema.sql")
    if not isinstance(schema_metadata, dict):
        raise RuntimeError("acquisition metadata does not contain schema.sql provenance")
    schema_path = metadata_path.parent / "schema.sql"
    if not schema_path.is_file():
        raise RuntimeError("schema.sql is missing beside the raw dataset")
    schema_hash = sha256_file(schema_path)
    if schema_hash != schema_metadata.get("sha256"):
        raise RuntimeError("schema.sql SHA-256 does not match acquisition metadata")
    validate_upstream_schema(schema_path)

    records, report = load_and_select_records(
        raw_path,
        source_commit=commit,
        exhaustive_limit=exhaustive_limit,
        check_consecutive_primes=True,
    )
    report.update(
        {
            "raw_path": str(raw_path),
            "raw_sha256": actual_hash,
            "schema_path": str(schema_path),
            "schema_sha256": schema_hash,
            "validated_at_utc": datetime.now(timezone.utc)
            .isoformat()
            .replace("+00:00", "Z"),
            "execution": _execution_metadata(),
        }
    )
    if report["status"] != "PASS":
        raise RuntimeError("dataset validation failed; no validated artifact was written")

    records_path = output_directory / "maximal_gap_records.csv"
    report_path = output_directory / "validation_report.json"
    _write_csv_exclusive(
        records_path,
        (_record_to_csv(record) for record in records),
        RECORD_FIELDS,
    )
    report["validated_records_sha256"] = sha256_file(records_path)
    _write_json_exclusive(report_path, report)
    return records_path, report_path, records, report


def load_validated_records(path: Path) -> list[MaximalGapRecord]:
    records: list[MaximalGapRecord] = []
    with path.open("r", encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            records.append(
                MaximalGapRecord(
                    record_index=int(row["record_index"]),
                    start_prime=int(row["start_prime"]),
                    gap=int(row["gap"]),
                    end_prime=int(row["end_prime"]),
                    source_id=row["source_id"],
                    source_row_id=row["source_row_id"],
                    source_commit=row["source_commit"],
                    verified_exhaustive_limit=int(row["verified_exhaustive_limit"]),
                )
            )
    return records


def analyze_validated_records(
    records_path: Path,
    output_directory: Path,
    *,
    approval_token: str | None,
    analysis_limit: int,
) -> dict[str, object]:
    """Compute end-bounded intervals, jumps, and a non-interpretive summary."""

    require_experiment_approval(approval_token)
    records = load_validated_records(records_path)
    if not records:
        raise ValueError("validated records file is empty")
    intervals = build_end_bounded_intervals(records, analysis_limit=analysis_limit)
    jumps = build_jump_metrics(records, analysis_limit=analysis_limit)
    summary = summarize_analysis(
        intervals,
        jumps,
        source_commit=records[0].source_commit,
        analysis_limit=analysis_limit,
        verified_exhaustive_limit=records[0].verified_exhaustive_limit,
    )
    summary.update(
        {
            "records_path": str(records_path),
            "records_sha256": sha256_file(records_path),
            "exhaustive_limit_source_url": EXHAUSTIVE_LIMIT_SOURCE_URL,
            "exhaustive_limit_source_as_of": EXHAUSTIVE_LIMIT_AS_OF,
            "computed_at_utc": datetime.now(timezone.utc)
            .isoformat()
            .replace("+00:00", "Z"),
            "execution": _execution_metadata(),
        }
    )

    interval_rows = [interval_to_dict(item) for item in intervals]
    jump_rows = [jump_to_dict(item) for item in jumps]
    _write_csv_exclusive(
        output_directory / "tables" / "end_bounded_intervals.csv",
        interval_rows,
        list(interval_rows[0]),
    )
    if jump_rows:
        _write_csv_exclusive(
            output_directory / "tables" / "end_bounded_jumps.csv",
            jump_rows,
            list(jump_rows[0]),
        )
    figure_paths = plot_all(
        intervals,
        jumps,
        output_directory / "figures",
        provenance_label=(
            f"source commit {records[0].source_commit}; "
            f"end-bounded; analyzed through x={analysis_limit}; "
            f"exhaustive limit={records[0].verified_exhaustive_limit}"
        ),
    )
    summary["figure_files"] = [str(path) for path in figure_paths]
    _write_json_exclusive(output_directory / "summary.json", summary)
    return summary


__all__ = [
    "RECORD_FIELDS",
    "analyze_validated_records",
    "load_validated_records",
    "validate_raw_dataset",
]
