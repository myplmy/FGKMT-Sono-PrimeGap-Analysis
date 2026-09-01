from __future__ import annotations

import csv
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import numpy as np

from source.plateau_recurrence import RecordReference, load_record_references
from source.provenance import APPROVAL_TOKEN, ApprovalRequiredError, sha256_file
from source.recurrence_prefix_information import (
    CONTRACT_SHA256,
    PrefixInformationError,
    PrefixMode,
    build_blinded_information_components,
    build_prefix_gate_report,
    load_frozen_contract,
    load_primecount_handoff,
    prefix_mode,
    run_prefix_probe,
    select_complete_prefix_plateaus,
    verify_saved_prefix,
)
from source.recurrence_stratified_null import BIN_SCHEMES, _bin_indices


ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "test_plan" / "P018_prefix_information_probe_contract_v1.json"
RECORDS = (
    ROOT
    / "datas"
    / "validated"
    / "prime-gap-list-project"
    / "1a112a1387052d9ad360686313f501c01fe46b68"
    / "maximal_gap_records.csv"
)


def _reference(index: int, start: int, gap: int) -> RecordReference:
    return RecordReference(
        record_index=index,
        start_prime=start,
        gap=gap,
        end_prime=start + gap,
        source_commit="p018-toy",
        verified_exhaustive_limit=10_000,
    )


def _synthetic_statistics(
    plateaus: list[dict[str, int]], *, gap_count: int
) -> dict[str, object]:
    populations: dict[str, dict[object, int]] = {}
    gaps: dict[str, dict[object, int]] = {}
    exposures: dict[str, dict[object, int]] = {}
    equal: dict[str, dict[object, int]] = {}
    for scheme in BIN_SCHEMES:
        scheme_pop: dict[object, int] = {}
        scheme_gap: dict[object, int] = {}
        scheme_exp: dict[object, int] = {}
        scheme_equal: dict[object, int] = {}
        for plateau_id, plateau in enumerate(plateaus):
            bin_index = int(
                _bin_indices(
                    np.asarray([plateau["start_prime"]], dtype=np.int64), scheme
                )[0]
            )
            scheme_pop[bin_index] = scheme_pop.get(bin_index, 0) + 20_000
            scheme_gap[(bin_index, plateau["gap"])] = 20
            scheme_exp[(plateau_id, bin_index)] = 2_000
            scheme_equal[(plateau_id, bin_index)] = 2
        populations[scheme.name] = scheme_pop
        gaps[scheme.name] = scheme_gap
        exposures[scheme.name] = scheme_exp
        equal[scheme.name] = scheme_equal
    return {
        "prime_count": gap_count + 1,
        "gap_count": gap_count,
        "populations": populations,
        "gap_counts": gaps,
        "exposure_counts": exposures,
        "exposure_equal_counts": equal,
    }


class RecurrencePrefixInformationTests(unittest.TestCase):
    def _primecount_handoff(
        self,
        root: Path,
        *,
        mode: str,
        lower: int,
        upper: int,
        exact_count: int,
        corrupt_difference: bool = False,
    ) -> Path:
        handoff = root / "handoff"
        handoff.mkdir(parents=True)
        counts = handoff / "prime_counts.csv"
        contract = load_frozen_contract(CONTRACT)
        evidence_values: dict[str, int] = {}
        with counts.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(
                handle,
                fieldnames=[
                    "mode",
                    "lower_inclusive",
                    "upper_exclusive",
                    "lower_minus_1",
                    "upper_minus_1",
                    "pi_lower_minus_1",
                    "pi_upper_minus_1",
                    "exact_gap_start_count",
                    "count_provenance",
                ],
            )
            writer.writeheader()
            for candidate_mode in ("P0", "A"):
                candidate = prefix_mode(contract, candidate_mode)
                candidate_lower = (
                    lower if candidate_mode == mode else candidate.lower_inclusive
                )
                candidate_upper = (
                    upper if candidate_mode == mode else candidate.upper_exclusive
                )
                candidate_count = exact_count if candidate_mode == mode else 123
                pi_lower = 100
                pi_upper = pi_lower + candidate_count
                if candidate_mode == mode and corrupt_difference:
                    pi_upper += 1
                writer.writerow(
                    {
                        "mode": candidate_mode,
                        "lower_inclusive": candidate_lower,
                        "upper_exclusive": candidate_upper,
                        "lower_minus_1": candidate_lower - 1,
                        "upper_minus_1": candidate_upper - 1,
                        "pi_lower_minus_1": pi_lower,
                        "pi_upper_minus_1": pi_upper,
                        "exact_gap_start_count": candidate_count,
                        "count_provenance": "primecount_gourdon_deleglise_rivat_match",
                    }
                )
                for algorithm in ("gourdon", "deleglise_rivat"):
                    evidence_values[
                        f"{candidate_mode.lower()}_lower_minus_1_{algorithm}.txt"
                    ] = pi_lower
                    evidence_values[
                        f"{candidate_mode.lower()}_upper_minus_1_{algorithm}.txt"
                    ] = pi_upper
        evidence_manifest = handoff / "primecount_evidence.sha256"
        evidence_lines: list[str] = []
        for name, value in sorted(evidence_values.items()):
            path = handoff / name
            path.write_text(f"toy primecount output\n{value}\n", encoding="utf-8")
            evidence_lines.append(f"{sha256_file(path)}  {name}")
        evidence_manifest.write_text(
            "\n".join(evidence_lines) + "\n", encoding="utf-8"
        )
        metadata = handoff / "metadata.txt"
        metadata.write_text(
            "\n".join(
                [
                    "status=P018_PREFIX_PRIMECOUNTS_READY",
                    "algorithms=gourdon,deleglise-rivat",
                    "algorithms_match=true",
                    f"contract_sha256={CONTRACT_SHA256}",
                    "count_provenance=primecount_gourdon_deleglise_rivat_match",
                    "threads=8",
                    "physical_cores=4",
                    "cpu_list=0,1,2,3,8,9,10,11",
                    "virtual_memory_limit_kib=30000000",
                    "gpu_used=false",
                    "actual_recurrence_analysis=false",
                    f"counts_sha256={sha256_file(counts)}",
                    f"evidence_manifest_sha256={sha256_file(evidence_manifest)}",
                ]
            )
            + "\n",
            encoding="utf-8",
        )
        preparation_log = handoff / "prepare.log"
        preparation_log.write_text("[PASS] toy exact counts\n", encoding="utf-8")
        ready = root / "READY.txt"
        ready.write_text(
            "\n".join(
                [
                    f"counts_relative={counts.relative_to(ROOT).as_posix()}",
                    f"metadata_relative={metadata.relative_to(ROOT).as_posix()}",
                    f"preparation_log_relative={preparation_log.relative_to(ROOT).as_posix()}",
                    f"evidence_manifest_relative={evidence_manifest.relative_to(ROOT).as_posix()}",
                ]
            )
            + "\n",
            encoding="utf-8",
        )
        return ready

    def test_frozen_endpoints_select_exact_complete_records(self) -> None:
        contract = load_frozen_contract(CONTRACT)
        references = load_record_references(RECORDS)
        p0 = prefix_mode(contract, "P0")
        stage_a = prefix_mode(contract, "A")
        self.assertEqual(
            [row["record_index"] for row in select_complete_prefix_plateaus(references, p0)],
            [51],
        )
        self.assertEqual(
            [
                row["record_index"]
                for row in select_complete_prefix_plateaus(references, stage_a)
            ],
            [51, 52],
        )
        too_short = PrefixMode(
            "P0",
            p0.lower_inclusive,
            1_408_695_493_609,
            (),
            16,
            17,
            7200,
            False,
        )
        self.assertEqual(select_complete_prefix_plateaus(references, too_short), [])

    def test_blinded_gate_is_invariant_to_observed_equal_count_mutation(self) -> None:
        contract = load_frozen_contract(CONTRACT)
        config = PrefixMode("A", 100, 200, (1, 2), 3, 5, 100, True)
        plateaus = [
            {
                "record_index": 1,
                "start_prime": 101,
                "end_prime": 103,
                "gap": 2,
                "right_exclusive": 109,
            },
            {
                "record_index": 2,
                "start_prime": 109,
                "end_prime": 127,
                "gap": 18,
                "right_exclusive": 191,
            },
        ]
        statistics = _synthetic_statistics(plateaus, gap_count=21)
        first = build_blinded_information_components(plateaus, statistics)
        for scheme in statistics["exposure_equal_counts"].values():
            for key in list(scheme):
                scheme[key] = 999
        second = build_blinded_information_components(plateaus, statistics)
        self.assertEqual(first, second)
        report = build_prefix_gate_report(
            contract,
            config,
            plateaus,
            first,
            exact_gap_start_count=21,
        )
        rendered = json.dumps({"components": first, "report": report})
        for prohibited in (
            "exposure_equal_counts",
            "observed_recurrences",
            '"C"',
            "p_value",
            "q_value",
            "z_score",
        ):
            self.assertNotIn(prohibited, rendered)
        self.assertFalse(report["automatic_full_range_promotion"])
        self.assertFalse(report["hypothesis_test_performed"])

    def test_A_gate_pass_and_hold_use_only_informative_positive_variance_rows(self) -> None:
        contract = load_frozen_contract(CONTRACT)
        config = PrefixMode("A", 100, 200, (1, 2), 3, 5, 100, True)
        plateaus = [
            {"record_index": 1, "start_prime": 101, "gap": 2},
            {"record_index": 2, "start_prime": 109, "gap": 18},
        ]
        components: list[dict[str, object]] = []
        for scheme in BIN_SCHEMES:
            for plateau in plateaus:
                components.append(
                    {
                        "scheme": scheme.name,
                        "record_index": plateau["record_index"],
                        "plateau_exposure_after_removal": 2_000,
                        "expected_component": 10.0,
                        "variance_component": 1.0,
                        "information_flag": "OK",
                    }
                )
        passed = build_prefix_gate_report(
            contract,
            config,
            plateaus,
            components,
            exact_gap_start_count=10_000,
        )
        self.assertTrue(passed["prefix_A_gate_pass"])
        self.assertEqual(passed["recommendation"], "REVIEW_BALANCED_B_DESIGN")
        self.assertIn("poisson_proxy_probability_at_least_one", passed)
        self.assertNotIn("null_probability_at_least_one", passed)

        for row in components:
            if (
                row["scheme"] == BIN_SCHEMES[0].name
                and row["record_index"] == 2
            ):
                row["variance_component"] = 0.0
        held = build_prefix_gate_report(
            contract,
            config,
            plateaus,
            components,
            exact_gap_start_count=10_000,
        )
        self.assertEqual(held["primary_expected_recurrences_total"], 20.0)
        self.assertEqual(held["primary_informative_expected_recurrences"], 10.0)
        self.assertFalse(held["prefix_A_gate_pass"])
        self.assertEqual(held["recommendation"], "HOLD_PREFIX_INFORMATION")

    def test_primecount_difference_mismatch_is_rejected(self) -> None:
        contract = load_frozen_contract(CONTRACT)
        config = prefix_mode(contract, "P0")
        with tempfile.TemporaryDirectory(dir=ROOT / "tmp") as directory:
            root = Path(directory)
            ready = self._primecount_handoff(
                root,
                mode="P0",
                lower=config.lower_inclusive,
                upper=config.upper_exclusive,
                exact_count=999,
                corrupt_difference=True,
            )
            with self.assertRaisesRegex(
                PrefixInformationError, "inconsistent|endpoint/count"
            ):
                load_primecount_handoff(ready, project_root=ROOT, config=config)

    def test_approval_denial_precedes_all_input_and_output_access(self) -> None:
        with tempfile.TemporaryDirectory(dir=ROOT / "tmp") as directory:
            root = Path(directory)
            output = root / "result"
            with self.assertRaises(ApprovalRequiredError):
                run_prefix_probe(
                    root / "missing-records.csv",
                    root / "missing-contract.json",
                    root / "missing-ready.txt",
                    ROOT,
                    output,
                    mode="P0",
                    approval_token=None,
                )
            self.assertFalse(output.exists())

    def test_toy_artifact_run_and_saved_blinded_recomputation(self) -> None:
        contract = load_frozen_contract(CONTRACT)
        config = prefix_mode(contract, "P0")
        plateaus = select_complete_prefix_plateaus(
            load_record_references(RECORDS), config
        )
        exact_count = 999
        statistics = _synthetic_statistics(plateaus, gap_count=exact_count)
        dual = {
            "status": "PASS",
            "serial_oracle_used": False,
            "full_parallel_passes": 2,
            "exact_statistics_equal": True,
            "expected_gap_start_count": exact_count,
            "independent_endpoint_prime_count_required": True,
            "common_sieve_and_accumulator_kernel_risk_acknowledged": True,
            "work_items_omitted": False,
            "precision_reduced": False,
            "statistics": statistics,
            "verification": {
                "primary_segment_count": 16,
                "verifier_segment_count": 17,
                "segment_counts_coprime": True,
                "interior_boundary_overlap_count": 0,
                "primary_adjacent_boundary_checks": 15,
                "verifier_adjacent_boundary_checks": 16,
                "primary_worker_count_observed": 8,
                "verifier_worker_count_observed": 8,
                "worker_native_thread_ceiling": 1,
            },
        }
        with tempfile.TemporaryDirectory(dir=ROOT / "tmp") as directory:
            root = Path(directory)
            ready = self._primecount_handoff(
                root,
                mode="P0",
                lower=config.lower_inclusive,
                upper=config.upper_exclusive,
                exact_count=exact_count,
            )
            output = root / "result"
            with patch(
                "source.recurrence_prefix_information.dual_partition_accumulate_bin_counts",
                return_value=dual,
            ):
                summary = run_prefix_probe(
                    RECORDS,
                    CONTRACT,
                    ready,
                    ROOT,
                    output,
                    mode="P0",
                    approval_token=APPROVAL_TOKEN,
                    runtime_resource_policy={"toy": True},
                )
            self.assertEqual(summary["status"], "PASS")
            self.assertEqual(summary["gate_recommendation"], "CALIBRATION_ONLY_NO_GATE")
            self.assertFalse(summary["observed_recurrence_saved"])
            verification = verify_saved_prefix(output)
            self.assertEqual(verification["status"], "PASS", verification["issues"])
            self.assertFalse(verification["full_prime_range_recomputed"])
            manifest = json.loads((output / "manifest.json").read_text(encoding="utf-8"))
            self.assertNotIn("full_statistics_sha256", manifest)
            self.assertTrue((output / "blinded_margin_statistics.json").is_file())

    def test_saved_verifier_detects_blinded_margin_tampering(self) -> None:
        contract = load_frozen_contract(CONTRACT)
        config = prefix_mode(contract, "P0")
        plateaus = select_complete_prefix_plateaus(
            load_record_references(RECORDS), config
        )
        exact_count = 999
        statistics = _synthetic_statistics(plateaus, gap_count=exact_count)
        dual = {
            "status": "PASS",
            "serial_oracle_used": False,
            "full_parallel_passes": 2,
            "exact_statistics_equal": True,
            "expected_gap_start_count": exact_count,
            "independent_endpoint_prime_count_required": True,
            "common_sieve_and_accumulator_kernel_risk_acknowledged": True,
            "work_items_omitted": False,
            "precision_reduced": False,
            "statistics": statistics,
            "verification": {},
        }
        with tempfile.TemporaryDirectory(dir=ROOT / "tmp") as directory:
            root = Path(directory)
            ready = self._primecount_handoff(
                root,
                mode="P0",
                lower=config.lower_inclusive,
                upper=config.upper_exclusive,
                exact_count=exact_count,
            )
            output = root / "result"
            with patch(
                "source.recurrence_prefix_information.dual_partition_accumulate_bin_counts",
                return_value=dual,
            ):
                run_prefix_probe(
                    RECORDS,
                    CONTRACT,
                    ready,
                    ROOT,
                    output,
                    mode="P0",
                    approval_token=APPROVAL_TOKEN,
                    runtime_resource_policy={"toy": True},
                )
            margin = output / "blinded_margin_statistics.json"
            payload = json.loads(margin.read_text(encoding="utf-8"))
            payload["gap_count"] += 1
            margin.write_text(json.dumps(payload), encoding="utf-8")
            verification = verify_saved_prefix(output)
            self.assertEqual(verification["status"], "FAIL")
            self.assertTrue(
                any("blinded_margin_statistics" in issue or "prime/gap" in issue for issue in verification["issues"]),
                verification["issues"],
            )


if __name__ == "__main__":
    unittest.main()
