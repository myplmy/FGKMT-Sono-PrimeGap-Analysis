"""Fail-closed tests for the Theory-84 sparse conductor audit."""

from __future__ import annotations

from copy import deepcopy
import unittest

import mpmath as mp

from source import dep_r09_sparse_divisor_conductor_audit as m


class ConductorDecompositionTests(unittest.TestCase):
    def test_divisors_and_mobius(self):
        self.assertEqual(m.divisors(1), (1,))
        self.assertEqual(m.divisors(30), (1, 2, 3, 5, 6, 10, 15, 30))
        self.assertEqual(m.mobius(1), 1)
        self.assertEqual(m.mobius(30), -1)
        self.assertEqual(m.mobius(12), 0)

    def test_primitive_counts_partition_all_characters(self):
        expected_phi = {
            3: 2,
            30: 8,
            210: 48,
            2310: 480,
            30030: 5760,
            510510: 92160,
        }
        for modulus, phi_value in expected_phi.items():
            partition = m.conductor_partition(modulus)
            self.assertEqual(sum(partition.values()), phi_value)
            self.assertEqual(partition[1], 1)
            self.assertEqual(sum(partition.values()) - 1, phi_value - 1)
            self.assertTrue(m.conductor_partition_is_exact(modulus))

    def test_squarefree_product_formula_and_positive_levels(self):
        expected_levels = {
            3: 2,
            30: 4,
            210: 8,
            2310: 16,
            30030: 32,
            510510: 64,
        }
        for modulus, level_count in expected_levels.items():
            for conductor in m.divisors(modulus):
                self.assertEqual(
                    m.primitive_character_count(conductor),
                    m.squarefree_primitive_count_product(conductor),
                )
            self.assertEqual(
                m.positive_conductor_level_count(modulus), level_count
            )

    def test_invalid_inputs_fail_closed(self):
        with self.assertRaises(ValueError):
            m.divisors(0)
        with self.assertRaises(TypeError):
            m.mobius(True)  # type: ignore[arg-type]
        with self.assertRaises(ValueError):
            m.squarefree_primitive_count_product(12)


class SparseCertificateBarrierTests(unittest.TestCase):
    def test_length_term_alone_exceeds_best_gate(self):
        with mp.workdps(100):
            for modulus in m.SAMPLE_PRIMORIALS:
                for d in (21, 186):
                    self.assertGreater(
                        m.generic_sparse_barrier_margin(modulus, d), 0
                    )

    def test_one_frequency_extremizer_requires_n(self):
        for length in (1, 2, 7, 100):
            result = m.one_frequency_extremizer(length)
            self.assertEqual(result["lhs_squared_magnitude"], length**2)
            self.assertEqual(result["coefficient_energy"], length)
            self.assertEqual(result["minimum_universal_coefficient"], length)

    def test_signed_cancellation_does_not_control_l1(self):
        witness = m.signed_cancellation_witness()
        self.assertEqual(witness["signed_sum_squared"], 0)
        self.assertEqual(witness["l1_sum_squared"], 4)


class LedgerTests(unittest.TestCase):
    def test_diagnostic_is_fail_closed(self):
        before = mp.mp.dps
        diagnostic = m.build_diagnostic()
        self.assertEqual(mp.mp.dps, before)
        self.assertTrue(diagnostic.sample_conductor_partitions_all_exact)
        self.assertTrue(diagnostic.sample_nonprincipal_totals_all_phi_minus_one)
        self.assertTrue(diagnostic.squarefree_product_formula_all_exact)
        self.assertTrue(diagnostic.generic_sparse_length_term_margins_all_positive)
        self.assertTrue(diagnostic.one_frequency_extremizer_requires_length_term)
        self.assertTrue(diagnostic.signed_cancellation_does_not_bound_l1_witness)
        self.assertFalse(
            diagnostic.montgomery_vaughan_2001_pdf_is_requested_vaughan_variance_paper
        )
        self.assertTrue(diagnostic.friedlander_goldston_1996_pdf_identity_verified)
        self.assertFalse(diagnostic.generic_sparse_large_sieve_can_certify_theory82_gate)
        self.assertFalse(diagnostic.prime_specific_bound_identified)
        self.assertFalse(diagnostic.direct_same_law_correlation_theorem_identified)
        self.assertFalse(diagnostic.actual_character_energy_lower_bound_claimed)
        self.assertFalse(diagnostic.pap_11_closed)
        self.assertFalse(diagnostic.dep_r09_closed)
        self.assertFalse(diagnostic.numerical_x_cert_ready)
        self.assertFalse(diagnostic.bounded_x_cert_range_obtained)
        self.assertFalse(diagnostic.threshold_calculator_ready)
        self.assertFalse(diagnostic.actual_prime_computation_run)
        self.assertFalse(diagnostic.source_theorem_local_axiom_used)
        self.assertFalse(diagnostic.proof_escape_used)

    def test_ledger_and_local_source_hashes(self):
        self.assertEqual(m.validate_ledger(m.load_ledger()), [])

    def test_ledger_tampering_is_detected(self):
        changed = deepcopy(m.load_ledger())
        changed["exact_finite_diagnostic"]["numerical_x_cert_ready"] = True
        self.assertTrue(m.validate_ledger(changed, check_hashes=False))

        changed = deepcopy(m.load_ledger())
        pinned = next(
            source
            for source in changed["source_registry"]
            if source.get("key") == "FRIEDLANDER_GOLDSTON1996_LOCAL"
        )
        pinned["sha256"] = "0" * 64
        self.assertTrue(m.validate_ledger(changed))


if __name__ == "__main__":
    unittest.main()
