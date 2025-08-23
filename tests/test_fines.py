"""Tests for fine structures."""

import pytest
import numpy as np
from traffic_fines.core.fines import FlatFine, IncomeBasedFine, ProgressiveFine


class TestFlatFine:
    """Test suite for FlatFine class."""

    def test_initialization(self):
        """Test flat fine initialization."""
        fine = FlatFine(fine_amount=150)
        assert fine.fine_amount == 150

    def test_calculate_fine(self):
        """Test flat fine calculation."""
        fine = FlatFine(fine_amount=200)

        # Should be same for all incomes
        assert fine.calculate_fine(0) == 200
        assert fine.calculate_fine(30000) == 200
        assert fine.calculate_fine(100000) == 200

    def test_parameters(self):
        """Test parameter getting and setting."""
        fine = FlatFine(100)

        params = fine.get_parameters()
        assert params == [100]

        fine.set_parameters([250])
        assert fine.fine_amount == 250
        assert fine.calculate_fine(50000) == 250

    def test_marginal_rate(self):
        """Test marginal rate calculation."""
        fine = FlatFine(100)

        # Marginal rate should always be zero
        assert fine.get_marginal_rate(0) == 0
        assert fine.get_marginal_rate(50000) == 0
        assert fine.get_marginal_rate(100000) == 0

    def test_invalid_parameters(self):
        """Test error handling for invalid parameters."""
        fine = FlatFine(100)

        with pytest.raises(ValueError):
            fine.set_parameters([100, 200])  # Too many parameters


class TestIncomeBasedFine:
    """Test suite for IncomeBasedFine class."""

    def test_initialization(self):
        """Test income-based fine initialization."""
        fine = IncomeBasedFine(base_amount=50, income_factor=0.002)
        assert fine.base_amount == 50
        assert fine.income_factor == 0.002

    def test_calculate_fine(self):
        """Test income-based fine calculation."""
        fine = IncomeBasedFine(base_amount=100, income_factor=0.001)

        # Fine should increase with income
        assert fine.calculate_fine(0) == 100
        assert fine.calculate_fine(50000) == 100 + 50
        assert fine.calculate_fine(100000) == 100 + 100

    def test_parameters(self):
        """Test parameter getting and setting."""
        fine = IncomeBasedFine(100, 0.001)

        params = fine.get_parameters()
        assert params == [100, 0.001]

        fine.set_parameters([200, 0.002])
        assert fine.base_amount == 200
        assert fine.income_factor == 0.002
        assert fine.calculate_fine(50000) == 200 + 100

    def test_marginal_rate(self):
        """Test marginal rate calculation."""
        fine = IncomeBasedFine(100, 0.003)

        # Marginal rate should equal income_factor
        assert fine.get_marginal_rate(0) == 0.003
        assert fine.get_marginal_rate(50000) == 0.003
        assert fine.get_marginal_rate(100000) == 0.003

    def test_progressive_effect(self):
        """Test that fine is progressive."""
        fine = IncomeBasedFine(50, 0.002)

        low_income = 20000
        high_income = 100000

        low_fine = fine.calculate_fine(low_income)
        high_fine = fine.calculate_fine(high_income)

        # Fine as percentage of income should increase
        low_rate = low_fine / low_income
        high_rate = high_fine / high_income

        assert high_rate > low_rate


class TestProgressiveFine:
    """Test suite for ProgressiveFine class."""

    def test_initialization(self):
        """Test progressive fine initialization."""
        fine = ProgressiveFine()
        assert len(fine.brackets) == len(fine.rates)

    def test_custom_brackets(self):
        """Test progressive fine with custom brackets."""
        brackets = [0, 25000, 75000]
        rates = [0.001, 0.003, 0.005]
        fine = ProgressiveFine(brackets, rates)

        assert fine.brackets == brackets
        assert fine.rates == rates

    def test_calculate_fine(self):
        """Test progressive fine calculation."""
        brackets = [0, 30000, 60000]
        rates = [0.001, 0.002, 0.004]
        fine = ProgressiveFine(brackets, rates)

        # Test various incomes
        assert fine.calculate_fine(20000) == 20000 * 0.001
        assert fine.calculate_fine(40000) == 30000 * 0.001 + 10000 * 0.002
        assert (
            fine.calculate_fine(70000) == 30000 * 0.001 + 30000 * 0.002 + 10000 * 0.004
        )

    def test_marginal_rate(self):
        """Test marginal rate at different income levels."""
        brackets = [0, 30000, 60000]
        rates = [0.001, 0.002, 0.004]
        fine = ProgressiveFine(brackets, rates)

        assert fine.get_marginal_rate(20000) == 0.001
        assert fine.get_marginal_rate(40000) == 0.002
        assert fine.get_marginal_rate(70000) == 0.004

    def test_progressivity(self):
        """Test that fine structure is truly progressive."""
        fine = ProgressiveFine()

        incomes = [20000, 50000, 100000, 200000]
        fines = [fine.calculate_fine(inc) for inc in incomes]
        rates = [f / i for f, i in zip(fines, incomes)]

        # Average rates should increase with income
        for i in range(len(rates) - 1):
            assert rates[i + 1] > rates[i]
