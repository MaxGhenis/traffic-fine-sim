"""Tests for WelfareOptimizer - written first per TDD."""

import pytest
import numpy as np

from traffic_fines.core.agent import Agent
from traffic_fines.core.optimizer import WelfareOptimizer
from traffic_fines.core.fines import FlatFine, IncomeBasedFine


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
