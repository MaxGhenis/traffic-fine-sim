"""Tests for fine structures - written first per TDD."""

import pytest
import numpy as np

from traffic_fines.core.fines import (
    FineStructure,
    FlatFine,
    IncomeBasedFine,
    HybridFine,
    BackwardLookingFine,
)


class TestFlatFine:
    """Tests for flat fine structure."""

    def test_calculate_fine_independent_of_income(self):
        """Flat fine should be the same regardless of income."""
        fine = FlatFine(amount=200.0)

        assert fine.calculate(income=30_000, speeding=0.5) == 200.0 * 0.5
        assert fine.calculate(income=100_000, speeding=0.5) == 200.0 * 0.5

    def test_calculate_fine_scales_with_speeding(self):
        """Fine should scale linearly with speeding intensity."""
        fine = FlatFine(amount=200.0)

        assert fine.calculate(income=50_000, speeding=0.0) == 0.0
        assert fine.calculate(income=50_000, speeding=0.5) == 100.0
        assert fine.calculate(income=50_000, speeding=1.0) == 200.0

    def test_marginal_rate_is_zero(self):
        """Flat fine has zero marginal rate on income."""
        fine = FlatFine(amount=200.0)

        assert fine.marginal_rate(income=30_000, speeding=0.5) == 0.0
        assert fine.marginal_rate(income=100_000, speeding=0.5) == 0.0

    def test_effective_tax_rate_equals_base_tax(self):
        """Effective tax rate should equal base tax rate for flat fines."""
        fine = FlatFine(amount=200.0)
        base_tax = 0.30

        assert fine.effective_tax_rate(base_tax, income=50_000, speeding=0.5) == 0.30


class TestIncomeBasedFine:
    """Tests for income-based fine structure."""

    def test_calculate_fine_scales_with_income(self):
        """Income-based fine should scale with income."""
        fine = IncomeBasedFine(rate=0.002)

        low_income_fine = fine.calculate(income=30_000, speeding=0.5)
        high_income_fine = fine.calculate(income=100_000, speeding=0.5)

        assert high_income_fine > low_income_fine
        assert np.isclose(low_income_fine, 30_000 * 0.002 * 0.5)
        assert np.isclose(high_income_fine, 100_000 * 0.002 * 0.5)

    def test_calculate_fine_scales_with_speeding(self):
        """Fine should scale with speeding intensity."""
        fine = IncomeBasedFine(rate=0.002)

        assert fine.calculate(income=50_000, speeding=0.0) == 0.0
        assert fine.calculate(income=50_000, speeding=1.0) == 50_000 * 0.002

    def test_marginal_rate_equals_rate_times_speeding(self):
        """Marginal rate on income is rate * speeding."""
        fine = IncomeBasedFine(rate=0.002)

        assert fine.marginal_rate(income=50_000, speeding=0.5) == 0.002 * 0.5
        assert fine.marginal_rate(income=100_000, speeding=0.5) == 0.002 * 0.5

    def test_effective_tax_rate_increases_with_speeding(self):
        """Effective tax rate should increase as speeding increases."""
        fine = IncomeBasedFine(rate=0.002)
        base_tax = 0.30

        etr_no_speed = fine.effective_tax_rate(base_tax, income=50_000, speeding=0.0)
        etr_half_speed = fine.effective_tax_rate(base_tax, income=50_000, speeding=0.5)
        etr_full_speed = fine.effective_tax_rate(base_tax, income=50_000, speeding=1.0)

        assert etr_no_speed == 0.30
        assert etr_half_speed == 0.30 + 0.002 * 0.5
        assert etr_full_speed == 0.30 + 0.002


class TestFineStructureInterface:
    """Tests for the abstract FineStructure interface."""

    def test_flat_fine_is_fine_structure(self):
        """FlatFine should implement FineStructure."""
        fine = FlatFine(amount=200.0)
        assert isinstance(fine, FineStructure)

    def test_income_based_fine_is_fine_structure(self):
        """IncomeBasedFine should implement FineStructure."""
        fine = IncomeBasedFine(rate=0.002)
        assert isinstance(fine, FineStructure)


class TestHybridFine:
    """Tests for hybrid fine structure (flat + income component)."""

    def test_calculate_combines_flat_and_income(self):
        """Hybrid fine should combine flat and income-based components."""
        fine = HybridFine(flat_amount=200.0, income_rate=0.002)

        # At €50,000 income, speeding=0.5:
        # Fine = (200 + 0.002 * 50,000) * 0.5 = (200 + 100) * 0.5 = 150
        result = fine.calculate(income=50_000, speeding=0.5)
        assert np.isclose(result, 150.0)

    def test_pure_flat_when_rate_zero(self):
        """With zero income rate, should behave like flat fine."""
        hybrid = HybridFine(flat_amount=200.0, income_rate=0.0)
        flat = FlatFine(amount=200.0)

        for income in [30_000, 50_000, 100_000]:
            for speeding in [0.0, 0.5, 1.0]:
                assert hybrid.calculate(income, speeding) == flat.calculate(income, speeding)

    def test_pure_income_based_when_flat_zero(self):
        """With zero flat amount, should behave like income-based fine."""
        hybrid = HybridFine(flat_amount=0.0, income_rate=0.002)
        income_based = IncomeBasedFine(rate=0.002)

        for income in [30_000, 50_000, 100_000]:
            for speeding in [0.0, 0.5, 1.0]:
                assert np.isclose(
                    hybrid.calculate(income, speeding),
                    income_based.calculate(income, speeding),
                )

    def test_marginal_rate_equals_income_rate_times_speeding(self):
        """Marginal rate should only reflect income component."""
        fine = HybridFine(flat_amount=200.0, income_rate=0.002)

        # Marginal rate is the derivative with respect to income
        # d/d(income) [(flat + rate*income)*speeding] = rate * speeding
        assert fine.marginal_rate(income=50_000, speeding=0.5) == 0.002 * 0.5
        assert fine.marginal_rate(income=100_000, speeding=0.5) == 0.002 * 0.5

    def test_negative_rate_allowed_for_regressive(self):
        """Negative income rate should be allowed (for testing regressive policies)."""
        fine = HybridFine(flat_amount=500.0, income_rate=-0.002)

        # High income should pay less
        low_income_fine = fine.calculate(income=30_000, speeding=1.0)
        high_income_fine = fine.calculate(income=100_000, speeding=1.0)

        assert low_income_fine > high_income_fine  # Regressive

    def test_floor_at_zero(self):
        """Fine should never go negative."""
        fine = HybridFine(flat_amount=100.0, income_rate=-0.01)

        # At very high income with negative rate, could go negative without floor
        result = fine.calculate(income=100_000, speeding=1.0)
        assert result >= 0


class TestBackwardLookingFine:
    """Tests for backward-looking income-based fine (Finnish system)."""

    def test_uses_lagged_income(self):
        """Fine should be based on lagged income, not current."""
        fine = BackwardLookingFine(rate=0.002, lagged_income=50_000)

        # Current income of €100,000 shouldn't matter
        result = fine.calculate(income=100_000, speeding=1.0)
        expected = 0.002 * 50_000 * 1.0
        assert np.isclose(result, expected)

    def test_marginal_rate_is_zero(self):
        """Marginal rate on current income should be zero."""
        fine = BackwardLookingFine(rate=0.002, lagged_income=50_000)

        # Key property: no labor supply distortion from current work
        assert fine.marginal_rate(income=30_000, speeding=0.5) == 0.0
        assert fine.marginal_rate(income=100_000, speeding=0.5) == 0.0

    def test_effective_tax_rate_equals_base(self):
        """Effective tax rate should equal base tax (no additional distortion)."""
        fine = BackwardLookingFine(rate=0.002, lagged_income=50_000)
        base_tax = 0.40

        etr = fine.effective_tax_rate(base_tax, income=100_000, speeding=1.0)
        assert etr == 0.40

    def test_scales_with_speeding(self):
        """Fine should still scale with speeding intensity."""
        fine = BackwardLookingFine(rate=0.002, lagged_income=50_000)

        assert fine.calculate(income=50_000, speeding=0.0) == 0.0
        assert fine.calculate(income=50_000, speeding=0.5) == 0.002 * 50_000 * 0.5
        assert fine.calculate(income=50_000, speeding=1.0) == 0.002 * 50_000 * 1.0

    def test_is_fine_structure(self):
        """BackwardLookingFine should implement FineStructure."""
        fine = BackwardLookingFine(rate=0.002, lagged_income=50_000)
        assert isinstance(fine, FineStructure)


class TestHybridFineInterface:
    """Tests for HybridFine implementing FineStructure interface."""

    def test_hybrid_fine_is_fine_structure(self):
        """HybridFine should implement FineStructure."""
        fine = HybridFine(flat_amount=200.0, income_rate=0.002)
        assert isinstance(fine, FineStructure)
