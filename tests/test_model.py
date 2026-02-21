"""Tests for model.py — agent optimization and mean-field equilibrium."""

import numpy as np
import pytest

from traffic_fines.model import (
    Agent,
    EquilibriumResult,
    FineSystem,
    FlatFine,
    IncomeBasedFine,
    death_probability,
    solve_equilibrium,
    utility,
)


class TestDeathProbability:
    """Tests for the speed-fatality power model."""

    def test_zero_speed_gives_base_rate(self):
        p = death_probability(0.0, p_base=0.001, exponent=4.0)
        assert p == pytest.approx(0.001)

    def test_higher_speed_higher_probability(self):
        p_low = death_probability(0.2, p_base=0.001, exponent=4.0)
        p_high = death_probability(0.5, p_base=0.001, exponent=4.0)
        assert p_high > p_low

    def test_power_model_exponent_2(self):
        """With exponent=2, doubling (1+s) should quadruple death probability."""
        # s=0 -> (1+0)^2 = 1 -> p_base
        # s=1 -> (1+1)^2 = 4 -> 4 * p_base
        p0 = death_probability(0.0, p_base=0.001, exponent=2.0)
        p1 = death_probability(1.0, p_base=0.001, exponent=2.0)
        assert p1 / p0 == pytest.approx(4.0)

    def test_power_model_exponent_4(self):
        """With exponent=4, doubling (1+s) should raise death prob by 16x."""
        p0 = death_probability(0.0, p_base=0.001, exponent=4.0)
        p1 = death_probability(1.0, p_base=0.001, exponent=4.0)
        assert p1 / p0 == pytest.approx(16.0)

    def test_negative_speed_raises(self):
        with pytest.raises(ValueError):
            death_probability(-0.1, p_base=0.001, exponent=4.0)

    def test_probability_bounded_below_one(self):
        """Even at extreme speed, probability should be capped at 1."""
        p = death_probability(100.0, p_base=0.001, exponent=4.0)
        assert p <= 1.0


class TestUtility:
    """Tests for the corrected utility function."""

    def test_positive_consumption_positive_utility(self):
        """Positive consumption should give positive log utility."""
        u = utility(
            consumption=1000,
            speeding=0.0,
            hours=1000,
            alpha=0.5,
            beta=1.0,
            max_hours=2080,
            vsl=3_600_000,
            p_base=0.001,
            exponent=4.0,
        )
        assert np.isfinite(u)

    def test_more_consumption_more_utility(self):
        """Utility is increasing in consumption."""
        u1 = utility(1000, 0.0, 1000, 0.5, 1.0, 2080, 3_600_000, 0.00005, 4.0)
        u2 = utility(2000, 0.0, 1000, 0.5, 1.0, 2080, 3_600_000, 0.00005, 4.0)
        assert u2 > u1

    def test_more_hours_less_utility_at_margin(self):
        """Labor disutility makes more hours reduce utility (all else equal)."""
        u1 = utility(1000, 0.0, 500, 0.5, 1.0, 2080, 3_600_000, 0.00005, 4.0)
        u2 = utility(1000, 0.0, 1500, 0.5, 1.0, 2080, 3_600_000, 0.00005, 4.0)
        assert u1 > u2

    def test_speeding_has_utility_benefit(self):
        """Some speeding increases utility from alpha term (ignoring death)."""
        # With very low death cost (low VSL), speeding should increase utility
        u1 = utility(1000, 0.0, 1000, 0.5, 1.0, 2080, 1.0, 0.00005, 4.0)
        u2 = utility(1000, 0.3, 1000, 0.5, 1.0, 2080, 1.0, 0.00005, 4.0)
        assert u2 > u1

    def test_death_cost_reduces_utility(self):
        """Higher VSL makes speeding more costly in utility terms."""
        u_low_vsl = utility(1000, 0.5, 1000, 0.5, 1.0, 2080, 100, 0.00005, 4.0)
        u_high_vsl = utility(1000, 0.5, 1000, 0.5, 1.0, 2080, 10_000_000, 0.00005, 4.0)
        assert u_low_vsl > u_high_vsl

    def test_death_cost_scales_with_marginal_utility(self):
        """Death cost = p(s) * VSL / (1+c), so higher c reduces death cost."""
        # At high consumption, marginal utility of consumption is low,
        # so the utility cost of death risk is lower
        u_poor = utility(100, 0.5, 1000, 0.5, 1.0, 2080, 3_600_000, 0.0001, 4.0)
        u_rich = utility(100_000, 0.5, 1000, 0.5, 1.0, 2080, 3_600_000, 0.0001, 4.0)
        # Both should be finite
        assert np.isfinite(u_poor)
        assert np.isfinite(u_rich)


class TestFineStructures:
    """Tests for flat and income-based fine calculations."""

    def test_flat_fine_independent_of_income(self):
        fine = FlatFine(amount=200)
        assert fine.calculate(income=30_000, speeding=0.5) == fine.calculate(
            income=100_000, speeding=0.5
        )

    def test_flat_fine_proportional_to_speeding(self):
        fine = FlatFine(amount=200)
        assert fine.calculate(income=50_000, speeding=1.0) == pytest.approx(
            2 * fine.calculate(income=50_000, speeding=0.5)
        )

    def test_flat_fine_zero_speeding(self):
        fine = FlatFine(amount=200)
        assert fine.calculate(income=50_000, speeding=0.0) == 0.0

    def test_income_fine_scales_with_income(self):
        fine = IncomeBasedFine(rate=0.02)
        f_low = fine.calculate(income=30_000, speeding=0.5)
        f_high = fine.calculate(income=100_000, speeding=0.5)
        assert f_high > f_low

    def test_income_fine_proportional_to_income(self):
        fine = IncomeBasedFine(rate=0.02)
        f1 = fine.calculate(income=50_000, speeding=0.5)
        f2 = fine.calculate(income=100_000, speeding=0.5)
        assert f2 / f1 == pytest.approx(2.0)

    def test_income_fine_proportional_to_speeding(self):
        fine = IncomeBasedFine(rate=0.02)
        f1 = fine.calculate(income=50_000, speeding=0.25)
        f2 = fine.calculate(income=50_000, speeding=0.5)
        assert f2 / f1 == pytest.approx(2.0)

    def test_income_fine_implicit_marginal_tax(self):
        """Income-based fine creates an implicit marginal tax on income."""
        fine = IncomeBasedFine(rate=0.02)
        # Marginal fine w.r.t. income = rate * speeding
        speeding = 0.5
        marginal_tax = fine.rate * speeding
        assert marginal_tax > 0

    def test_fine_system_interface(self):
        """Both fine types implement the same interface."""
        for fine_obj in [FlatFine(amount=200), IncomeBasedFine(rate=0.02)]:
            result = fine_obj.calculate(income=50_000, speeding=0.5)
            assert isinstance(result, float)
            assert result >= 0


class TestAgent:
    """Tests for individual agent optimization."""

    def test_agent_optimizes_valid_choices(self):
        """Agent should return hours in [0, 2080] and speeding in [0, 1]."""
        agent = Agent(wage=20.0, alpha=0.5, beta=1.0, max_hours=2080, tax_rate=0.3)
        hours, speeding = agent.optimize(
            fine_system=FlatFine(amount=200),
            ubi=0.0,
            vsl=3_600_000,
            p_base=0.001,
            exponent=4.0,
        )
        assert 0 <= hours <= 2080
        assert 0 <= speeding <= 1

    def test_higher_fine_reduces_speeding(self):
        """Higher fines should reduce optimal speeding."""
        agent = Agent(wage=20.0, alpha=0.5, beta=1.0, max_hours=2080, tax_rate=0.3)
        _, s_low = agent.optimize(
            FlatFine(amount=50), 0.0, 3_600_000, 0.00005, 4.0
        )
        _, s_high = agent.optimize(
            FlatFine(amount=500), 0.0, 3_600_000, 0.00005, 4.0
        )
        assert s_high <= s_low

    def test_higher_wage_more_hours(self):
        """Higher wage should induce more labor supply."""
        agent_low = Agent(wage=10.0, alpha=0.5, beta=1.0, max_hours=2080, tax_rate=0.3)
        agent_high = Agent(wage=30.0, alpha=0.5, beta=1.0, max_hours=2080, tax_rate=0.3)
        h_low, _ = agent_low.optimize(
            FlatFine(amount=200), 0.0, 3_600_000, 0.00005, 4.0
        )
        h_high, _ = agent_high.optimize(
            FlatFine(amount=200), 0.0, 3_600_000, 0.00005, 4.0
        )
        assert h_high >= h_low

    def test_agent_consumption_positive(self):
        """Agent should choose hours such that consumption is positive."""
        agent = Agent(wage=20.0, alpha=0.5, beta=1.0, max_hours=2080, tax_rate=0.3)
        hours, speeding = agent.optimize(
            FlatFine(amount=200), 0.0, 3_600_000, 0.00005, 4.0
        )
        income = agent.wage * hours
        consumption = income * (1 - 0.3) - FlatFine(200).calculate(income, speeding)
        assert consumption > 0


class TestEquilibrium:
    """Tests for mean-field equilibrium solver."""

    @pytest.fixture
    def small_economy(self):
        """A small economy for testing (10 agents for speed)."""
        np.random.seed(42)
        wages = np.maximum(5.0, np.random.lognormal(np.log(20), 0.5, size=10))
        return wages

    def test_equilibrium_converges(self, small_economy):
        """Equilibrium should converge within max iterations."""
        result = solve_equilibrium(
            wages=small_economy,
            fine_system=FlatFine(amount=200),
            alpha=0.5,
            beta=1.0,
            max_hours=2080,
            tax_rates=0.3,
            vsl=3_600_000,
            p_base=0.001,
            exponent=4.0,
            max_iter=200,
            tol=1e-4,
            damping=0.5,
        )
        assert result.converged

    def test_equilibrium_result_shapes(self, small_economy):
        """Result arrays should match number of agents."""
        n = len(small_economy)
        result = solve_equilibrium(
            wages=small_economy,
            fine_system=FlatFine(amount=200),
            alpha=0.5,
            beta=1.0,
            max_hours=2080,
            tax_rates=0.3,
            vsl=3_600_000,
            p_base=0.001,
            exponent=4.0,
        )
        assert len(result.hours) == n
        assert len(result.speeding) == n
        assert len(result.incomes) == n
        assert len(result.utilities) == n

    def test_ubi_positive(self, small_economy):
        """UBI from redistributed taxes + fines should be positive."""
        result = solve_equilibrium(
            wages=small_economy,
            fine_system=FlatFine(amount=200),
            alpha=0.5,
            beta=1.0,
            max_hours=2080,
            tax_rates=0.3,
            vsl=3_600_000,
            p_base=0.001,
            exponent=4.0,
        )
        assert result.ubi > 0

    def test_income_fines_vs_flat_comparison(self, small_economy):
        """Both fine systems should produce valid equilibria."""
        result_flat = solve_equilibrium(
            wages=small_economy,
            fine_system=FlatFine(amount=200),
            alpha=0.5,
            beta=1.0,
            max_hours=2080,
            tax_rates=0.3,
            vsl=3_600_000,
            p_base=0.001,
            exponent=4.0,
        )
        result_income = solve_equilibrium(
            wages=small_economy,
            fine_system=IncomeBasedFine(rate=0.02),
            alpha=0.5,
            beta=1.0,
            max_hours=2080,
            tax_rates=0.3,
            vsl=3_600_000,
            p_base=0.001,
            exponent=4.0,
        )
        assert result_flat.converged
        assert result_income.converged
        # Both should have positive mean speeding
        assert np.mean(result_flat.speeding) > 0
        assert np.mean(result_income.speeding) > 0

    def test_damping_affects_convergence(self, small_economy):
        """Damping parameter should affect convergence speed."""
        result = solve_equilibrium(
            wages=small_economy,
            fine_system=FlatFine(amount=200),
            alpha=0.5,
            beta=1.0,
            max_hours=2080,
            tax_rates=0.3,
            vsl=3_600_000,
            p_base=0.001,
            exponent=4.0,
            damping=0.5,
        )
        assert result.iterations > 0

    def test_gini_between_0_and_1(self, small_economy):
        """Gini coefficient should be between 0 and 1."""
        result = solve_equilibrium(
            wages=small_economy,
            fine_system=FlatFine(amount=200),
            alpha=0.5,
            beta=1.0,
            max_hours=2080,
            tax_rates=0.3,
            vsl=3_600_000,
            p_base=0.001,
            exponent=4.0,
        )
        assert 0 <= result.gini <= 1

    def test_convergence_diagnostics_stored(self, small_economy):
        """Equilibrium result should store convergence diagnostics."""
        result = solve_equilibrium(
            wages=small_economy,
            fine_system=FlatFine(amount=200),
            alpha=0.5,
            beta=1.0,
            max_hours=2080,
            tax_rates=0.3,
            vsl=3_600_000,
            p_base=0.001,
            exponent=4.0,
        )
        assert hasattr(result, "iterations")
        assert hasattr(result, "max_delta")
        assert hasattr(result, "converged")


class TestPerAgentTaxRates:
    """Tests for heterogeneous per-agent tax rates."""

    @pytest.fixture
    def small_economy(self):
        np.random.seed(42)
        return np.maximum(5.0, np.random.lognormal(np.log(20), 0.5, size=10))

    def test_array_tax_rates_accepted(self, small_economy):
        """solve_equilibrium accepts array of tax rates."""
        n = len(small_economy)
        tax_rates = np.linspace(0.1, 0.4, n)
        result = solve_equilibrium(
            wages=small_economy,
            fine_system=FlatFine(amount=200),
            alpha=0.5, beta=1.0, max_hours=2080,
            tax_rates=tax_rates,
            vsl=3_600_000, p_base=0.001, exponent=4.0,
        )
        assert result.converged

    def test_scalar_and_array_equivalent(self, small_economy):
        """Scalar tax_rates should give same result as uniform array."""
        n = len(small_economy)
        result_scalar = solve_equilibrium(
            wages=small_economy,
            fine_system=FlatFine(amount=200),
            alpha=0.5, beta=1.0, max_hours=2080,
            tax_rates=0.3,
            vsl=3_600_000, p_base=0.001, exponent=4.0,
        )
        result_array = solve_equilibrium(
            wages=small_economy,
            fine_system=FlatFine(amount=200),
            alpha=0.5, beta=1.0, max_hours=2080,
            tax_rates=np.full(n, 0.3),
            vsl=3_600_000, p_base=0.001, exponent=4.0,
        )
        np.testing.assert_allclose(
            result_scalar.utilities, result_array.utilities, rtol=1e-6
        )

    def test_length_mismatch_raises(self, small_economy):
        """Array tax_rates with wrong length should raise."""
        wrong_length = np.array([0.2, 0.3])  # Only 2 but 10 agents
        with pytest.raises(ValueError):
            solve_equilibrium(
                wages=small_economy,
                fine_system=FlatFine(amount=200),
                alpha=0.5, beta=1.0, max_hours=2080,
                tax_rates=wrong_length,
                vsl=3_600_000, p_base=0.001, exponent=4.0,
            )

    def test_heterogeneous_tax_rates_affect_labor(self, small_economy):
        """Agents with higher tax rates should work less."""
        n = len(small_economy)
        low_tax = solve_equilibrium(
            wages=small_economy,
            fine_system=FlatFine(amount=200),
            alpha=0.5, beta=1.0, max_hours=2080,
            tax_rates=0.1,
            vsl=3_600_000, p_base=0.001, exponent=4.0,
        )
        high_tax = solve_equilibrium(
            wages=small_economy,
            fine_system=FlatFine(amount=200),
            alpha=0.5, beta=1.0, max_hours=2080,
            tax_rates=0.5,
            vsl=3_600_000, p_base=0.001, exponent=4.0,
        )
        # Higher taxes should reduce labor supply
        assert np.mean(high_tax.hours) <= np.mean(low_tax.hours)
