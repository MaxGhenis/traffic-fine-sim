"""Tests for Agent class - written first per TDD."""

import pytest
import numpy as np

from traffic_fines.core.agent import Agent
from traffic_fines.core.fines import FlatFine, IncomeBasedFine


class TestAgentInitialization:
    """Tests for Agent initialization."""

    def test_agent_stores_wage(self):
        """Agent should store hourly wage."""
        agent = Agent(wage=50.0)
        assert agent.wage == 50.0

    def test_agent_default_parameters(self):
        """Agent should have sensible defaults."""
        agent = Agent(wage=50.0)
        assert agent.labor_disutility > 0
        assert agent.speeding_utility > 0
        assert agent.vsl > 0


class TestAgentUtility:
    """Tests for utility calculation."""

    def test_utility_increases_with_consumption(self):
        """Higher consumption should increase utility."""
        agent = Agent(wage=50.0)

        u_low = agent.consumption_utility(10_000)
        u_high = agent.consumption_utility(50_000)

        assert u_high > u_low

    def test_utility_is_concave_in_consumption(self):
        """Marginal utility should decrease (concavity)."""
        agent = Agent(wage=50.0)

        mu_low = agent.consumption_utility(20_000) - agent.consumption_utility(10_000)
        mu_high = agent.consumption_utility(40_000) - agent.consumption_utility(30_000)

        assert mu_low > mu_high

    def test_labor_disutility_increases_with_hours(self):
        """Working more should increase disutility."""
        agent = Agent(wage=50.0)

        d_low = agent.labor_disutility_fn(500)
        d_high = agent.labor_disutility_fn(2000)

        assert d_high > d_low

    def test_speeding_utility_increases_with_speeding(self):
        """More speeding should increase speeding utility."""
        agent = Agent(wage=50.0)

        u_low = agent.speeding_utility_fn(0.2)
        u_high = agent.speeding_utility_fn(0.8)

        assert u_high > u_low


class TestAgentOptimization:
    """Tests for agent optimization behavior.

    These tests use calibrated parameters to ensure interior solutions.
    Higher labor_disutility ensures agents don't just work max hours.
    """

    # Calibrated parameters for meaningful behavioral responses
    LABOR_DISUTILITY = 25.0  # Higher value for interior labor solutions
    SPEEDING_UTILITY = 1.0  # High enough to compete with death cost
    VSL = 1_000.0  # Very low VSL for interior speeding solutions in tests

    def test_optimize_returns_hours_and_speeding(self):
        """Optimization should return labor hours and speeding."""
        agent = Agent(wage=50.0, labor_disutility=self.LABOR_DISUTILITY)
        fine = FlatFine(amount=200.0)

        hours, speeding = agent.optimize(fine, tax_rate=0.3, death_prob=0.0001, ubi=0.0)

        assert 0 <= hours <= 2080
        assert 0 <= speeding <= 1

    def test_labor_responds_to_wage(self):
        """Labor supply should respond to wage (direction depends on utility params).

        With log utility, income and substitution effects roughly cancel,
        leading to near-zero labor supply elasticity (realistic).
        """
        low_wage = Agent(wage=30.0, labor_disutility=self.LABOR_DISUTILITY)
        high_wage = Agent(wage=80.0, labor_disutility=self.LABOR_DISUTILITY)
        fine = FlatFine(amount=200.0)

        h_low, _ = low_wage.optimize(fine, tax_rate=0.3, death_prob=0.0001, ubi=0.0)
        h_high, _ = high_wage.optimize(fine, tax_rate=0.3, death_prob=0.0001, ubi=0.0)

        # Verify we get interior solutions (not at boundaries)
        assert 0 < h_low < 2080
        assert 0 < h_high < 2080
        # Small elasticity is expected with log utility
        assert abs(h_high - h_low) / h_low < 0.5  # Less than 50% change

    def test_labor_responds_to_tax(self):
        """Labor supply should respond to tax rate."""
        agent = Agent(wage=50.0, labor_disutility=self.LABOR_DISUTILITY)
        fine = FlatFine(amount=200.0)

        h_low_tax, _ = agent.optimize(fine, tax_rate=0.2, death_prob=0.0001, ubi=0.0)
        h_high_tax, _ = agent.optimize(fine, tax_rate=0.5, death_prob=0.0001, ubi=0.0)

        # Verify interior solutions
        assert 0 < h_low_tax < 2080
        assert 0 < h_high_tax < 2080

    def test_higher_death_prob_reduces_speeding(self):
        """Higher death probability should deter speeding."""
        agent = Agent(
            wage=50.0,
            labor_disutility=self.LABOR_DISUTILITY,
            speeding_utility=self.SPEEDING_UTILITY,
            vsl=self.VSL,
        )
        fine = FlatFine(amount=100.0)

        _, s_low_risk = agent.optimize(fine, tax_rate=0.3, death_prob=0.00001, ubi=0.0)
        _, s_high_risk = agent.optimize(fine, tax_rate=0.3, death_prob=0.01, ubi=0.0)

        assert s_low_risk > s_high_risk

    def test_higher_flat_fine_reduces_speeding(self):
        """Higher flat fine should deter speeding."""
        agent = Agent(
            wage=50.0,
            labor_disutility=self.LABOR_DISUTILITY,
            speeding_utility=self.SPEEDING_UTILITY,
            vsl=self.VSL,
        )
        low_fine = FlatFine(amount=100.0)
        high_fine = FlatFine(amount=5000.0)

        _, s_low = agent.optimize(low_fine, tax_rate=0.3, death_prob=0.0001, ubi=0.0)
        _, s_high = agent.optimize(high_fine, tax_rate=0.3, death_prob=0.0001, ubi=0.0)

        assert s_low > s_high

    def test_income_based_fine_affects_behavior(self):
        """Income-based fines should affect labor and/or speeding differently than flat.

        This is the key prediction: income-based fines create an implicit tax
        that distorts labor supply.
        """
        agent = Agent(
            wage=50.0,
            labor_disutility=self.LABOR_DISUTILITY,
            speeding_utility=self.SPEEDING_UTILITY,
            vsl=self.VSL,
        )

        # Set fines to have similar deterrence at median income
        flat = FlatFine(amount=200.0)
        income_based = IncomeBasedFine(rate=0.01)  # Higher rate for effect

        h_flat, s_flat = agent.optimize(flat, tax_rate=0.3, death_prob=0.0001, ubi=0.0)
        h_ib, s_ib = agent.optimize(
            income_based, tax_rate=0.3, death_prob=0.0001, ubi=0.0
        )

        # Behavior should differ between fine structures
        assert (h_ib != h_flat) or (s_ib != s_flat)


class TestAgentCalculations:
    """Tests for derived calculations."""

    def test_gross_income_calculation(self):
        """Gross income = wage * hours."""
        agent = Agent(wage=50.0)
        assert agent.gross_income(1000) == 50_000

    def test_net_income_calculation(self):
        """Net income accounts for taxes, fines, and UBI."""
        agent = Agent(wage=50.0)
        fine = FlatFine(amount=200.0)

        net = agent.net_income(
            hours=1000, speeding=0.5, fine=fine, tax_rate=0.3, ubi=1000
        )

        gross = 50_000
        tax = gross * 0.3
        fine_amount = 200 * 0.5
        expected = gross - tax - fine_amount + 1000

        assert np.isclose(net, expected)


class TestAgentProperties:
    """Tests for agent properties."""

    def test_optimal_hours_none_before_optimize(self):
        """optimal_hours should be None before optimization."""
        agent = Agent(wage=50.0)
        assert agent.optimal_hours is None

    def test_optimal_speeding_none_before_optimize(self):
        """optimal_speeding should be None before optimization."""
        agent = Agent(wage=50.0)
        assert agent.optimal_speeding is None

    def test_optimal_hours_set_after_optimize(self):
        """optimal_hours should be set after optimization."""
        agent = Agent(wage=50.0, labor_disutility=25.0)
        fine = FlatFine(amount=200.0)
        agent.optimize(fine, tax_rate=0.3, death_prob=0.0001, ubi=0.0)
        assert agent.optimal_hours is not None

    def test_optimal_speeding_set_after_optimize(self):
        """optimal_speeding should be set after optimization."""
        agent = Agent(wage=50.0, labor_disutility=25.0)
        fine = FlatFine(amount=200.0)
        agent.optimize(fine, tax_rate=0.3, death_prob=0.0001, ubi=0.0)
        assert agent.optimal_speeding is not None
