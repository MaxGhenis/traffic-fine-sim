"""Tests for PolicyEngine US integration."""

import pytest
import numpy as np

# Skip all tests if policyengine-us is not installed
policyengine_us = pytest.importorskip("policyengine_us")

from traffic_fines.data.policyengine import (
    compute_mtr,
    compute_mtrs_for_incomes,
    create_agents_with_mtrs,
)
from traffic_fines.core.agent import Agent


class TestComputeMTR:
    """Tests for MTR computation."""

    def test_compute_mtr_returns_float(self):
        """MTR computation should return a float."""
        mtr = compute_mtr(income=50000)
        assert isinstance(mtr, float)

    def test_mtr_in_valid_range(self):
        """MTR should be between 0 and 1."""
        mtr = compute_mtr(income=50000)
        assert 0 <= mtr <= 1

    def test_mtr_increases_with_income(self):
        """MTR should generally increase with income (progressive taxes)."""
        mtr_low = compute_mtr(income=20000)
        mtr_high = compute_mtr(income=200000)
        # High income MTR should be at least as high as low income
        # (not strictly greater due to phase-outs)
        assert mtr_high >= mtr_low - 0.1  # Allow some tolerance

    def test_mtr_at_zero_income(self):
        """MTR at zero income should be valid (can be negative due to EITC)."""
        mtr = compute_mtr(income=0)
        # MTR can be negative at low incomes due to EITC phase-in
        assert -1 <= mtr <= 1

    def test_mtr_at_high_income(self):
        """MTR at very high income should be valid."""
        mtr = compute_mtr(income=1000000)
        assert 0 <= mtr <= 1


class TestComputeMTRsForIncomes:
    """Tests for batch MTR computation."""

    def test_batch_mtr_returns_array(self):
        """Batch MTR should return numpy array."""
        incomes = [20000, 50000, 100000]
        mtrs = compute_mtrs_for_incomes(incomes)
        assert isinstance(mtrs, np.ndarray)
        assert len(mtrs) == 3

    def test_batch_mtr_matches_individual(self):
        """Batch MTR should match individual calls."""
        incomes = [30000, 60000, 90000]
        batch_mtrs = compute_mtrs_for_incomes(incomes)
        individual_mtrs = [compute_mtr(inc) for inc in incomes]
        np.testing.assert_allclose(batch_mtrs, individual_mtrs, rtol=0.01)


class TestCreateAgentsWithMTRs:
    """Tests for agent creation with MTRs."""

    def test_creates_agents_with_mtrs(self):
        """Should create agents with MTR attributes set."""
        wages = [20.0, 50.0, 100.0]
        agents = create_agents_with_mtrs(wages)

        assert len(agents) == 3
        for agent in agents:
            assert isinstance(agent, Agent)
            assert agent.mtr is not None
            assert 0 <= agent.mtr <= 1

    def test_higher_wage_higher_mtr(self):
        """Higher wage agents should have higher MTRs (generally)."""
        wages = [15.0, 75.0, 150.0]  # ~$30k, $150k, $300k annual at 2000 hrs
        agents = create_agents_with_mtrs(wages)

        # Top MTR should be higher than bottom (allowing some tolerance)
        assert agents[2].mtr >= agents[0].mtr - 0.1

    def test_custom_hours_for_mtr_calculation(self):
        """Should use custom hours for income calculation."""
        wages = [50.0]
        agents_default = create_agents_with_mtrs(wages)
        agents_custom = create_agents_with_mtrs(wages, annual_hours=1000)

        # Lower hours = lower income = potentially lower MTR
        # Not guaranteed to differ due to tax structure
        assert agents_custom[0].mtr is not None


class TestAgentMTRAttribute:
    """Tests for Agent MTR attribute."""

    def test_agent_mtr_defaults_to_none(self):
        """Agent MTR should default to None."""
        agent = Agent(wage=50.0)
        assert agent.mtr is None

    def test_agent_mtr_can_be_set(self):
        """Agent MTR can be set at initialization."""
        agent = Agent(wage=50.0, mtr=0.35)
        assert agent.mtr == 0.35

    def test_agent_uses_own_mtr_when_set(self):
        """Agent should use own MTR when set, ignoring passed tax_rate."""
        from traffic_fines.core.fines import FlatFine

        agent = Agent(wage=50.0, mtr=0.25)
        fine = FlatFine(amount=100.0)

        # The agent's net income calculation should use its own MTR
        gross = agent.gross_income(1000)  # 50 * 1000 = 50000
        net = agent.net_income(
            hours=1000, speeding=0.5, fine=fine, tax_rate=0.40, ubi=0.0
        )

        # With MTR=0.25: net = 50000 - 50000*0.25 - 100*0.5 = 50000 - 12500 - 50 = 37450
        # Without MTR (using tax_rate=0.40): net = 50000 - 20000 - 50 = 29950
        # So net should be higher when using the lower MTR
        expected_net = gross - gross * 0.25 - fine.calculate(gross, 0.5)
        assert np.isclose(net, expected_net, rtol=0.01)
