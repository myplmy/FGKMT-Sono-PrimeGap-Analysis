"""Gated PARI/GP production adapter for one P009 boundary block.

Candidate discovery by ``precprime``/``nextprime`` is not trusted as proof.
The two candidate primes receive independently verified PARI certificates, and
every integer between the last-prime candidate and the half-open block boundary
is closed by an exact nontrivial factor.
"""

from __future__ import annotations

import csv
import json
import time
from pathlib import Path

from source.boundary_witness import (
    BoundaryWitness,
    BoundaryWitnessError,
    CompositeEvidence,
    PrimeEvidence,
    SCHEMA_VERSION,
    verify_boundary_witness,
    witness_to_dict,
)
from source.finite_gap_replay import (
    P007_MOD2310_CERTIFICATE_SHA256,
    require_mod2310_replay_completion,
)
from source.pari_certificate import (
    CERT_BEGIN,
    CERT_END,
    PARI_METHOD,
    PariCertificateError,
    PariProgramRunner,
    extract_marked_payload,
    generate_certificate_bundle,
    probe_gp_version,
    require_adapter_completion,
    run_gp_program,
    verify_pari_prime_evidence,
)
from source.provenance import require_experiment_approval, sha256_file


P008_LOCAL_BOUNDS_SHA256 = (
    "df9312081968e4103d883fb616c70b25e3a2c4f6ed1fa1e2e52df01fd169e164"
)
P009_ACTUAL_EXPERIMENT = "P009_SINGLE_BLOCK_BOUNDARY_ACTUAL"
TARGET_BLOCK_ID = "x1e20_L1000"
TARGET_A = 10**20
TARGET_B = TARGET_A + 1_000
TARGET_THRESHOLD = 1_856


def _write_json_exclusive(path: Path, payload: object) -> None:
    with path.open("x", encoding="utf-8", newline="\n") as handle:
        json.dump(payload, handle, ensure_ascii=False, indent=2, sort_keys=True)
        handle.write("\n")


def validate_prerequisites(
    adapter_manifest_path: Path,
    replay_manifest_path: Path,
    local_bounds_path: Path,
) -> dict[str, object]:
    adapter = require_adapter_completion(adapter_manifest_path)
    replay = require_mod2310_replay_completion(replay_manifest_path)
    if replay.get("input_certificate_sha256") != P007_MOD2310_CERTIFICATE_SHA256:
        raise BoundaryWitnessError("P010A replay certificate hash mismatch")
    local_hash = sha256_file(local_bounds_path)
    if local_hash != P008_LOCAL_BOUNDS_SHA256:
        raise BoundaryWitnessError("P008 local-block table hash mismatch")

    with local_bounds_path.open("r", encoding="utf-8", newline="") as handle:
        matches = [
            row
            for row in csv.DictReader(handle)
            if row.get("block_id") == TARGET_BLOCK_ID
        ]
    if len(matches) != 1:
        raise BoundaryWitnessError("P008 target block row is not unique")
    row = matches[0]
    if (
        int(row["a"]) != TARGET_A
        or int(row["b"]) != TARGET_B
        or int(row["internal_integer_upper_bound"]) != 0
        or row["right_boundary_status"] != "UNRESOLVED"
    ):
        raise BoundaryWitnessError("P008 target block contract changed")
    return {
        "status": "PASS",
        "adapter_gp_version": adapter.get("gp_version"),
        "p010a_replay_status": replay.get("status"),
        "p008_local_bounds_sha256": local_hash,
        "block_id": TARGET_BLOCK_ID,
        "a": str(TARGET_A),
        "b": str(TARGET_B),
        "internal_start_bounded_upper_bound": 0,
        "actual_boundary_experiment_executed": False,
    }


def parse_boundary_candidate_payload(text: str) -> tuple[int, int, tuple[CompositeEvidence, ...]]:
    try:
        payload = json.loads(text)
    except json.JSONDecodeError as exc:
        raise BoundaryWitnessError(f"PARI boundary payload is malformed: {exc}") from exc
    if not isinstance(payload, list) or len(payload) != 3:
        raise BoundaryWitnessError("PARI boundary payload must be [p,q,factors]")
    p, q, raw_factors = payload
    if (
        isinstance(p, bool)
        or not isinstance(p, int)
        or isinstance(q, bool)
        or not isinstance(q, int)
        or not isinstance(raw_factors, list)
    ):
        raise BoundaryWitnessError("PARI boundary payload has invalid scalar types")
    factors: list[CompositeEvidence] = []
    for item in raw_factors:
        if (
            not isinstance(item, list)
            or len(item) != 2
            or any(isinstance(value, bool) or not isinstance(value, int) for value in item)
        ):
            raise BoundaryWitnessError("PARI factor row must contain two integers")
        factors.append(CompositeEvidence(value=item[0], factor=item[1]))
    return p, q, tuple(factors)


def discover_boundary_candidates(
    block_b: int,
    *,
    runner: PariProgramRunner = run_gp_program,
    timeout_seconds: int = 900,
) -> tuple[int, int, tuple[CompositeEvidence, ...], object]:
    if block_b < 3:
        raise ValueError("block_b must be at least 3")
    program = (
        f"b={block_b};p=precprime(b-1);q=nextprime(b);"
        "v=vector(b-p-1,k,n=p+k;[n,factor(n)[1,1]]);\n"
        f'print("{CERT_BEGIN}");print([p,q,v]);print("{CERT_END}");quit\n'
    )
    invocation = runner(program, timeout_seconds)
    if invocation.returncode != 0:
        raise PariCertificateError(
            f"PARI boundary candidate generation returned {invocation.returncode}: "
            f"{invocation.stderr.strip()}"
        )
    payload = extract_marked_payload(invocation.stdout, CERT_BEGIN, CERT_END)
    p, q, factors = parse_boundary_candidate_payload(payload)
    expected = tuple(range(p + 1, block_b))
    if tuple(item.value for item in factors) != expected:
        raise BoundaryWitnessError("PARI factor rows do not exactly cover (p,b)")
    return p, q, factors, invocation


def run_single_block_actual(
    local_bounds_path: Path,
    adapter_manifest_path: Path,
    replay_manifest_path: Path,
    output_directory: Path,
    *,
    approval_token: str | None,
    timeout_seconds: int = 900,
    runner: PariProgramRunner = run_gp_program,
    gp_version: str | None = None,
) -> dict[str, object]:
    require_experiment_approval(approval_token)
    if output_directory.exists():
        raise FileExistsError(f"refusing to overwrite P009 actual result: {output_directory}")
    prerequisite = validate_prerequisites(
        adapter_manifest_path, replay_manifest_path, local_bounds_path
    )
    effective_version = gp_version
    if effective_version is None and runner is run_gp_program:
        effective_version = probe_gp_version()
    if effective_version is None:
        raise BoundaryWitnessError("gp_version is required for a custom runner")

    started = time.perf_counter()
    p, q, composite_evidence, discovery = discover_boundary_candidates(
        TARGET_B, runner=runner, timeout_seconds=timeout_seconds
    )
    output_directory.mkdir(parents=True)
    certificate_root = output_directory / "certificates"
    p_manifest = generate_certificate_bundle(
        p,
        certificate_root / "last_prime",
        runner=runner,
        timeout_seconds=timeout_seconds,
        gp_version=effective_version,
    )
    q_manifest = generate_certificate_bundle(
        q,
        certificate_root / "right_prime",
        runner=runner,
        timeout_seconds=timeout_seconds,
        gp_version=effective_version,
    )
    witness = BoundaryWitness(
        schema_version=SCHEMA_VERSION,
        block_a=TARGET_A,
        block_b=TARGET_B,
        threshold=TARGET_THRESHOLD,
        internal_start_bounded_upper_bound=0,
        last_prime=PrimeEvidence(
            p,
            PARI_METHOD,
            "certificates/last_prime/certificate.json",
            str(p_manifest["artifacts_sha256"]["certificate.json"]),
        ),
        right_prime=PrimeEvidence(
            q,
            PARI_METHOD,
            "certificates/right_prime/certificate.json",
            str(q_manifest["artifacts_sha256"]["certificate.json"]),
        ),
        composite_evidence=composite_evidence,
    )
    verification = verify_boundary_witness(
        witness,
        artifact_root=output_directory,
        certificate_verifier=verify_pari_prime_evidence,
    )
    if verification["status"] != "PASS" or not verification["certified_zero"]:
        raise BoundaryWitnessError("P009 actual boundary witness did not verify")

    _write_json_exclusive(output_directory / "boundary_witness.json", witness_to_dict(witness))
    _write_json_exclusive(output_directory / "verification_report.json", verification)
    with (output_directory / "composite_evidence.csv").open(
        "x", encoding="utf-8", newline=""
    ) as handle:
        writer = csv.DictWriter(handle, fieldnames=("value", "factor"))
        writer.writeheader()
        writer.writerows(
            {"value": item.value, "factor": item.factor}
            for item in composite_evidence
        )
    with (output_directory / "input_local_block_bounds.csv").open("xb") as handle:
        handle.write(local_bounds_path.read_bytes())
    resource_metrics = {
        "status": "PASS",
        "elapsed_seconds": time.perf_counter() - started,
        "candidate_discovery_elapsed_seconds": discovery.elapsed_seconds,
        "candidate_discovery_maximum_resident_set_kib": discovery.maximum_resident_set_kib,
        "artifact_bytes_before_manifest": sum(
            path.stat().st_size for path in output_directory.rglob("*") if path.is_file()
        ),
        "ram_limit_bytes": 32 * 1024**3,
        "disk_limit_bytes": 100 * 10**9,
        "gpu_used": False,
    }
    _write_json_exclusive(output_directory / "resource_metrics.json", resource_metrics)
    artifact_names = (
        "boundary_witness.json",
        "verification_report.json",
        "composite_evidence.csv",
        "input_local_block_bounds.csv",
        "resource_metrics.json",
        "certificates/last_prime/manifest.json",
        "certificates/right_prime/manifest.json",
    )
    manifest = {
        "status": "PASS",
        "experiment": P009_ACTUAL_EXPERIMENT,
        "gp_version": effective_version,
        "block_id": TARGET_BLOCK_ID,
        "threshold": TARGET_THRESHOLD,
        "certified_zero": True,
        "prerequisite": prerequisite,
        "artifacts_sha256": {
            name: sha256_file(output_directory / name) for name in artifact_names
        },
        "direct_search_acceleration_proved": False,
        "gpu_used": False,
    }
    _write_json_exclusive(output_directory / "manifest.json", manifest)
    return {
        **verification,
        "experiment": P009_ACTUAL_EXPERIMENT,
        "gp_version": effective_version,
        "resource_metrics": resource_metrics,
        "direct_search_acceleration_proved": False,
    }


__all__ = [
    "P008_LOCAL_BOUNDS_SHA256",
    "P009_ACTUAL_EXPERIMENT",
    "TARGET_A",
    "TARGET_B",
    "TARGET_THRESHOLD",
    "discover_boundary_candidates",
    "parse_boundary_candidate_payload",
    "run_single_block_actual",
    "validate_prerequisites",
]
