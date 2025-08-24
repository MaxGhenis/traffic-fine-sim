"""Tests for Society simulation."""

import pytest
import numpy as np
from traffic_fines.core.agent import Agent
from traffic_fines.core.society import Society
from traffic_fines.core.fines import FlatFine, IncomeBasedFine


class TestSociety:
    """Test suite for Society class."""

    @pytest.fixture
    def simple_society(self):
        """Create a simple society for testing."""
        incomes = [30000, 60000, 90000]
        agents = [Agent(income) for income in incomes]
        fine_structure = FlatFine(100)
        return Society(agents, fine_structure)

    def test_initialization(self, simple_society):
        """Test society initialization."""
        assert len(simple_society.agents) == 3
        assert simple_society.tax_rate == 0.3
        assert simple_society.ubi == 0.0
        assert simple_society.iteration == 0

    def test_single_iteration(self, simple_society):
        """Test a single iteration of society simulation."""
        results = simple_society.simulate(max_iterations=1)

        assert results["iterations"] == 1
        assert "total_utility" in results
        assert "avg_speeding" in results
        assert "avg_labor_hours" in results
        assert results["ubi"] >= 0

    def test_convergence(self):
        """Test that society can converge."""
        incomes = [40000, 50000, 60000]
        agents = [Agent(income, labor_disutility_factor=0.3) for income in incomes]
        fine_structure = FlatFine(50)
        society = Society(agents, fine_structure, convergence_threshold=1.0)

        results = society.simulate(max_iterations=20)

        # Should converge before max iterations with loose threshold
        assert results["converged"]
        assert results["iterations"] < 20

    def test_income_groups(self, simple_society):
        """Test income group analysis."""
        results = simple_society.simulate(max_iterations=5)

        assert "income_groups" in results
        groups = results["income_groups"]

        # Should have appropriate groups
        assert "bottom_20" in groups or "middle_60" in groups or "top_20" in groups

        # Each group should have expected statistics
        for group_name, group_data in groups.items():
            if group_data:  # If group has members
                assert "avg_labor" in group_data
                assert "avg_speeding" in group_data
                assert "avg_utility" in group_data
                assert "avg_effective_mtr" in group_data

    def test_welfare_metrics(self, simple_society):
        """Test welfare metric calculations."""
        simple_society.simulate(max_iterations=5)
        metrics = simple_society.calculate_welfare_metrics()

        assert "total_utility" in metrics
        assert "avg_utility" in metrics
        assert "utility_gini" in metrics
        assert "deadweight_loss" in metrics
        assert "efficiency_ratio" in metrics

        # Gini should be between 0 and 1
        assert 0 <= metrics["utility_gini"] <= 1

        # Efficiency ratio should be positive but <= 1
        assert 0 < metrics["efficiency_ratio"] <= 1

    def test_history_tracking(self, simple_society):
        """Test that history is properly tracked."""
        results = simple_society.simulate(max_iterations=5)

        assert "history" in results
        history = results["history"]

        # Should have one entry per iteration
        assert len(history) == results["iterations"]

        # Each history entry should have expected fields
        for entry in history:
            assert "iteration" in entry
            assert "total_utility" in entry
            assert "avg_speeding" in entry
            assert "avg_labor" in entry
            assert "ubi" in entry
            assert "death_prob" in entry

    def test_flat_vs_income_based(self):
        """Test difference between flat and income-based fines."""
        incomes = np.array([20000, 40000, 60000, 80000, 100000])

        # Create society with flat fine
        agents_flat = [Agent(income) for income in incomes]
        flat_fine = FlatFine(100)
        society_flat = Society(agents_flat, flat_fine)
        results_flat = society_flat.simulate(max_iterations=10)

        # Create society with income-based fine
        agents_income = [Agent(income) for income in incomes]
        income_fine = IncomeBasedFine(50, 0.001)
        society_income = Society(agents_income, income_fine)
        results_income = society_income.simulate(max_iterations=10)

        # Results should differ
        assert results_flat["total_utility"] != results_income["total_utility"]

        # Income-based should have different MTRs by group
        flat_groups = results_flat["income_groups"]
        income_groups = results_income["income_groups"]

        # Check that high-income group faces higher effective MTR with income-based fines
        # Note: MTR only differs for those who speed
        if "top_20" in income_groups and "top_20" in flat_groups:
            # If speeding is > 0, income-based should have higher MTR
            if income_groups["top_20"]["avg_speeding"] > 0.01:
                assert (
                    income_groups["top_20"]["avg_effective_mtr"]
                    >= flat_groups["top_20"]["avg_effective_mtr"]
                )

    def test_ubi_redistribution(self):
        """Test that UBI redistribution works correctly."""
        incomes = [30000, 60000, 90000]
        agents = [Agent(income) for income in incomes]
        fine_structure = FlatFine(100)
        society = Society(agents, fine_structure, tax_rate=0.3)

        results = society.simulate(max_iterations=5)

        # UBI should be positive (from taxes and fines)
        assert results["ubi"] > 0

        # Check UBI calculation from history
        last_iteration = results["history"][-1]
        expected_ubi = (
            last_iteration["total_fines"] + last_iteration["total_taxes"]
        ) / len(agents)
        assert abs(results["ubi"] - expected_ubi) < 0.01
