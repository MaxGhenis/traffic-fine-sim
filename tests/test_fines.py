"""Tests for fine structures - written first per TDD."""

import pytest
import numpy as np

from traffic_fines.core.fines import FineStructure, FlatFine, IncomeBasedFine


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
