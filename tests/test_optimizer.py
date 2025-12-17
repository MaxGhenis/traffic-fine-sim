"""Tests for WelfareOptimizer - written first per TDD."""

import pytest
import numpy as np

from traffic_fines.core.agent import Agent
from traffic_fines.core.optimizer import WelfareOptimizer
from traffic_fines.core.fines import FlatFine, IncomeBasedFine, HybridFine


class TestWelfareOptimizerInitialization:
    """Tests for optimizer initialization."""

    def test_optimizer_stores_agents(self):
        """Optimizer should store agents."""
        agents = [Agent(wage=w, labor_disutility=25.0) for w in [30.0, 50.0, 80.0]]
        optimizer = WelfareOptimizer(agents)

        assert len(optimizer.agents) == 3


class TestWelfareOptimization:
    """Tests for welfare optimization."""

    def test_optimize_flat_fine_returns_result(self):
        """Optimization should return result with optimal parameters."""
        agents = [Agent(wage=w, labor_disutility=25.0) for w in [30.0, 50.0, 80.0]]
        optimizer = WelfareOptimizer(agents)

        result = optimizer.optimize_flat_fine(tax_rate=0.3)

        assert "optimal_fine" in result
        assert "welfare" in result
        assert result["optimal_fine"] >= 0

    def test_optimize_income_based_fine_returns_result(self):
        """Optimization should return result with optimal parameters."""
        agents = [Agent(wage=w, labor_disutility=25.0) for w in [30.0, 50.0, 80.0]]
        optimizer = WelfareOptimizer(agents)

        result = optimizer.optimize_income_based_fine(tax_rate=0.3)

        assert "optimal_rate" in result
        assert "welfare" in result
        assert result["optimal_rate"] >= 0

    def test_compare_systems_returns_both(self):
        """Comparison should return results for both fine systems."""
        agents = [Agent(wage=w, labor_disutility=25.0) for w in [30.0, 50.0, 80.0]]
        optimizer = WelfareOptimizer(agents)

        comparison = optimizer.compare_systems(tax_rate=0.3)

        assert "flat" in comparison
        assert "income_based" in comparison
        assert "welfare_difference" in comparison

    def test_history_property(self):
        """History property should return optimization history."""
        agents = [Agent(wage=w, labor_disutility=25.0) for w in [30.0, 50.0, 80.0]]
        optimizer = WelfareOptimizer(agents)

        optimizer.optimize_flat_fine(tax_rate=0.3)

        assert len(optimizer.history) > 0
        assert "welfare" in optimizer.history[0]


class TestHybridFineOptimization:
    """Tests for hybrid fine optimization (flat + income rate)."""

    def test_optimize_hybrid_returns_both_params(self):
        """Hybrid optimization should return both flat amount and income rate."""
        agents = [Agent(wage=w, labor_disutility=25.0) for w in [30.0, 50.0, 80.0]]
        optimizer = WelfareOptimizer(agents)

        result = optimizer.optimize_hybrid_fine(tax_rate=0.3)

        assert "optimal_flat" in result
        assert "optimal_rate" in result
        assert "welfare" in result
        assert result["optimal_flat"] >= 0
        assert result["optimal_rate"] >= -1  # Can be negative (regressive)

    def test_optimize_hybrid_constrained_rate_nonnegative(self):
        """Constrained hybrid optimization should keep rate >= 0."""
        agents = [Agent(wage=w, labor_disutility=25.0) for w in [30.0, 50.0, 80.0]]
        optimizer = WelfareOptimizer(agents)

        result = optimizer.optimize_hybrid_fine(
            tax_rate=0.3, constrain_rate_nonnegative=True
        )

        assert result["optimal_rate"] >= 0

    def test_optimize_hybrid_unconstrained_can_be_regressive(self):
        """Unconstrained hybrid optimization can find regressive optimum."""
        agents = [Agent(wage=w, labor_disutility=25.0) for w in [30.0, 50.0, 80.0]]
        optimizer = WelfareOptimizer(agents)

        result = optimizer.optimize_hybrid_fine(
            tax_rate=0.3, constrain_rate_nonnegative=False
        )

        # Result may or may not be regressive, but method should work
        assert "optimal_rate" in result

    def test_hybrid_welfare_at_least_as_good_as_flat(self):
        """Hybrid optimal welfare should be >= pure flat optimal welfare."""
        agents = [Agent(wage=w, labor_disutility=25.0) for w in [30.0, 50.0, 80.0]]
        optimizer = WelfareOptimizer(agents)

        flat_result = optimizer.optimize_flat_fine(tax_rate=0.3)
        hybrid_result = optimizer.optimize_hybrid_fine(tax_rate=0.3)

        # Hybrid should be at least as good (can set rate=0 to match flat)
        assert hybrid_result["welfare"] >= flat_result["welfare"] - 0.01


class TestAlternativeWelfareFunctions:
    """Tests for optimization under different welfare functions."""

    def test_optimize_with_rawlsian(self):
        """Should be able to optimize with Rawlsian (maximin) welfare."""
        agents = [Agent(wage=w, labor_disutility=25.0) for w in [30.0, 50.0, 80.0]]
        optimizer = WelfareOptimizer(agents)

        result = optimizer.optimize_flat_fine(tax_rate=0.3, welfare_function="rawlsian")

        assert "optimal_fine" in result
        assert "welfare" in result

    def test_optimize_with_atkinson(self):
        """Should be able to optimize with Atkinson welfare (gamma=1)."""
        agents = [Agent(wage=w, labor_disutility=25.0) for w in [30.0, 50.0, 80.0]]
        optimizer = WelfareOptimizer(agents)

        result = optimizer.optimize_flat_fine(
            tax_rate=0.3, welfare_function="atkinson", inequality_aversion=1.0
        )

        assert "optimal_fine" in result

    def test_higher_inequality_aversion_favors_income_based(self):
        """Higher inequality aversion should favor more progressive fines."""
        agents = [Agent(wage=w, labor_disutility=25.0) for w in [20.0, 40.0, 100.0]]
        optimizer = WelfareOptimizer(agents)

        low_aversion = optimizer.optimize_hybrid_fine(
            tax_rate=0.3,
            welfare_function="atkinson",
            inequality_aversion=0.5,
            constrain_rate_nonnegative=True,
        )

        high_aversion = optimizer.optimize_hybrid_fine(
            tax_rate=0.3,
            welfare_function="atkinson",
            inequality_aversion=2.0,
            constrain_rate_nonnegative=True,
        )

        # Higher aversion should lead to higher (or equal) income rate
        assert high_aversion["optimal_rate"] >= low_aversion["optimal_rate"] - 0.001


class TestSensitivityAnalysis:
    """Tests for sensitivity analysis methods."""

    def test_sensitivity_over_externality_factor(self):
        """Should analyze sensitivity to externality factor."""
        agents = [Agent(wage=w, labor_disutility=25.0) for w in [30.0, 50.0, 80.0]]
        optimizer = WelfareOptimizer(agents)

        results = optimizer.sensitivity_analysis(
            tax_rate=0.3, parameter="externality_factor", values=[0.1, 0.2, 0.5]
        )

        assert len(results) == 3
        assert all("optimal_flat" in r for r in results)
        assert all("externality_factor" in r for r in results)

    def test_sensitivity_over_tax_rate(self):
        """Should analyze sensitivity to tax rate."""
        agents = [Agent(wage=w, labor_disutility=25.0) for w in [30.0, 50.0, 80.0]]
        optimizer = WelfareOptimizer(agents)

        results = optimizer.sensitivity_analysis(
            tax_rate=0.3,  # baseline, will be overridden
            parameter="tax_rate",
            values=[0.2, 0.3, 0.4],
        )

        assert len(results) == 3
        assert all("tax_rate" in r for r in results)

    def test_sample_size_convergence(self):
        """Should test convergence across sample sizes."""
        # Create a large pool of wages to sample from
        np.random.seed(42)
        wage_pool = np.random.lognormal(np.log(25.0), 0.5, 500)

        results = WelfareOptimizer.sample_size_convergence(
            wage_pool=wage_pool,
            sample_sizes=[10, 25, 50],
            tax_rate=0.3,
            labor_disutility=25.0,
        )

        assert len(results) == 3
        assert all("n_agents" in r for r in results)
        assert all("optimal_flat" in r for r in results)
