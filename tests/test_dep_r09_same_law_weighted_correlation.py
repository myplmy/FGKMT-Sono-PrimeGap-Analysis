"""Exact tests for the DEP-R09 same-law weighted-correlation audit."""

from __future__ import annotations

from copy import deepcopy
from fractions import Fraction
import unittest

from source import dep_r09_same_law_weighted_correlation as m


def fixture_law() -> m.JointLaw:
    return (
        m.OuterOutcome(
            probability=Fraction(1, 2),
            outer_good=True,
            inner_outcomes=(
                m.InnerOutcome(Fraction(1, 4), True, Fraction(1, 16)),
                m.InnerOutcome(Fraction(3, 4), False, Fraction(1)),
            ),
        ),
        m.OuterOutcome(
            probability=Fraction(1, 3),
            outer_good=True,
            inner_outcomes=(
                m.InnerOutcome(Fraction(1, 2), True, Fraction(1, 4)),
                m.InnerOutcome(Fraction(1, 2), True, Fraction(9, 16)),
            ),
        ),
        m.OuterOutcome(
            probability=Fraction(1, 6),
            outer_good=False,
            inner_outcomes=(
                m.InnerOutcome(Fraction(1), True, Fraction(100)),
            ),
        ),
    )


class FiniteJointLawTests(unittest.TestCase):
    def test_tower_and_flat_moments_are_exactly_equal(self):
        law = fixture_law()
        self.assertEqual(m.outer_good_mass(law), Fraction(5, 6))
        self.assertEqual(
            m.outer_good_moment_tower(law),
            m.outer_good_moment_flat(law),
        )
        self.assertEqual(
            m.conditional_outer_good_moment(law),
            m.outer_good_moment_tower(law) / Fraction(5, 6),
        )

    def test_exact_sieve_and_correlation_success_mass(self):
        law = fixture_law()
        self.assertEqual(m.exact_sieve_good_mass(law), Fraction(11, 24))
        self.assertEqual(
            m.exact_joint_success_mass(law, Fraction(1, 2)),
            Fraction(7, 24),
        )

    def test_global_and_conditional_markov_bounds(self):
        self.assertEqual(
            m.global_markov_joint_success_lower(
                Fraction(1, 5),
                Fraction(1, 4),
                Fraction(1, 100),
                Fraction(1, 2),
            ),
            Fraction(14, 25),
        )
        self.assertEqual(
            m.conditional_markov_joint_success_lower(
                Fraction(1, 5),
                Fraction(1, 4),
                Fraction(1, 100),
                Fraction(1, 2),
            ),
            Fraction(71, 125),
        )

    def test_uniform_fiber_strict_boundary(self):
        self.assertTrue(
            m.uniform_fiber_selection_certified(
                Fraction(1, 4), Fraction(1, 8), Fraction(1, 2)
            )
        )
        self.assertFalse(
            m.uniform_fiber_selection_certified(
                Fraction(1, 2), Fraction(1, 8), Fraction(1, 2)
            )
        )

    def test_raw_second_moment_requires_a_pointwise_survivor_floor(self):
        self.assertEqual(
            m.raw_to_normalized_moment_upper(
                Fraction(45), Fraction(3), Fraction(5)
            ),
            Fraction(1, 5),
        )
        with self.assertRaises(ValueError):
            m.raw_to_normalized_moment_upper(
                Fraction(1), Fraction(0), Fraction(5)
            )

    def test_invalid_joint_laws_fail_closed(self):
        bad_outer = (
            m.OuterOutcome(
                Fraction(1, 2),
                True,
                (m.InnerOutcome(Fraction(1), True, Fraction(0)),),
            ),
        )
        with self.assertRaises(ValueError):
            m.validate_joint_law(bad_outer)
        bad_inner = (
            m.OuterOutcome(
                Fraction(1),
                True,
                (m.InnerOutcome(Fraction(1, 2), True, Fraction(0)),),
            ),
        )
        with self.assertRaises(ValueError):
            m.validate_joint_law(bad_inner)
        negative_badness = (
            m.OuterOutcome(
                Fraction(1),
                True,
                (m.InnerOutcome(Fraction(1), True, Fraction(-1)),),
            ),
        )
        with self.assertRaises(ValueError):
            m.validate_joint_law(negative_badness)
        with self.assertRaises(TypeError):
            m.global_markov_joint_success_lower(
                Fraction(0), Fraction(0), 0.1, Fraction(1)
            )


class LedgerTests(unittest.TestCase):
    def test_ledger_and_source_hashes(self):
        self.assertEqual(m.validate_ledger(m.load_ledger()), [])

    def test_fail_closed_status(self):
        diagnostic = m.build_diagnostic()
        self.assertTrue(diagnostic.finite_tower_identity_exact)
        self.assertFalse(diagnostic.same_law_analytic_moment_bound_available)
        self.assertFalse(diagnostic.numerical_x_cert_ready)
        self.assertFalse(diagnostic.source_theorem_local_axiom_used)
        self.assertFalse(diagnostic.proof_escape_used)

    def test_ledger_tampering_is_detected(self):
        changed = deepcopy(m.load_ledger())
        changed["exact_finite_diagnostic"]["numerical_x_cert_ready"] = True
        self.assertTrue(m.validate_ledger(changed, check_hashes=False))
        changed = deepcopy(m.load_ledger())
        changed["source_registry"][0]["sha256"] = "0" * 64
        self.assertTrue(m.validate_ledger(changed))


if __name__ == "__main__":
    unittest.main()
