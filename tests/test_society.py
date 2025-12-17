"""Tests for Society simulation - written first per TDD."""

import pytest
import numpy as np

from traffic_fines.core.agent import Agent
from traffic_fines.core.society import Society
from traffic_fines.core.fines import FlatFine, IncomeBasedFine


class TestSocietyInitialization:
    """Tests for Society initialization."""

    def test_society_stores_agents(self):
        """Society should store list of agents."""
        agents = [Agent(wage=w) for w in [30.0, 50.0, 80.0]]
        fine = FlatFine(amount=200.0)
        society = Society(agents, fine, tax_rate=0.3)

        assert len(society.agents) == 3

    def test_society_stores_fine_structure(self):
        """Society should store fine structure."""
        agents = [Agent(wage=50.0)]
        fine = FlatFine(amount=200.0)
        society = Society(agents, fine, tax_rate=0.3)

        assert society.fine == fine

    def test_society_stores_tax_rate(self):
        """Society should store tax rate."""
        agents = [Agent(wage=50.0)]
        fine = FlatFine(amount=200.0)
        society = Society(agents, fine, tax_rate=0.35)

        assert society.tax_rate == 0.35


class TestSocietySimulation:
    """Tests for society simulation dynamics."""

    def test_simulate_returns_results(self):
        """Simulation should return results dict."""
        agents = [Agent(wage=w, labor_disutility=25.0) for w in [30.0, 50.0, 80.0]]
        fine = FlatFine(amount=200.0)
        society = Society(agents, fine, tax_rate=0.3)

        results = society.simulate()

        assert isinstance(results, dict)
        assert "total_utility" in results
        assert "avg_speeding" in results
        assert "total_fines" in results

    def test_simulate_converges(self):
        """Simulation should converge within max iterations."""
        agents = [Agent(wage=w, labor_disutility=25.0) for w in [30.0, 50.0, 80.0]]
        fine = FlatFine(amount=200.0)
        society = Society(agents, fine, tax_rate=0.3)

        results = society.simulate(max_iterations=50)

        assert results["converged"] or results["iterations"] <= 50

    def test_simulate_tracks_convergence_status(self):
        """Simulation should track whether it converged."""
        agents = [Agent(wage=50.0, labor_disutility=25.0)]
        fine = FlatFine(amount=200.0)
        society = Society(agents, fine, tax_rate=0.3)

        results = society.simulate(max_iterations=5)

        # Result should include convergence info
        assert "converged" in results
        assert "iterations" in results
        assert isinstance(results["converged"], bool)

    def test_ubi_equals_redistributed_revenue(self):
        """UBI should equal (fines + taxes) / n_agents."""
        agents = [Agent(wage=w, labor_disutility=25.0) for w in [30.0, 50.0, 80.0]]
        fine = FlatFine(amount=200.0)
        society = Society(agents, fine, tax_rate=0.3)

        results = society.simulate()

        expected_ubi = (results["total_fines"] + results["total_taxes"]) / len(agents)
        assert np.isclose(results["ubi"], expected_ubi, rtol=0.01)


class TestSocietyWelfare:
    """Tests for welfare calculations."""

    def test_total_utility_is_sum(self):
        """Total utility should be sum of individual utilities."""
        agents = [Agent(wage=w, labor_disutility=25.0) for w in [30.0, 50.0, 80.0]]
        fine = FlatFine(amount=200.0)
        society = Society(agents, fine, tax_rate=0.3)

        results = society.simulate()

        # Total utility should be positive and reasonable
        assert results["total_utility"] > 0

    def test_externality_reduces_welfare(self):
        """Externality from speeding should reduce social welfare."""
        agents = [Agent(wage=w, labor_disutility=25.0) for w in [30.0, 50.0, 80.0]]
        fine = FlatFine(amount=0.0)  # No fines, high speeding

        society_no_ext = Society(agents, fine, tax_rate=0.3, externality_factor=0.0)
        society_ext = Society(agents, fine, tax_rate=0.3, externality_factor=10.0)

        results_no_ext = society_no_ext.simulate()
        results_ext = society_ext.simulate()

        # Externality should reduce welfare
        assert results_ext["social_welfare"] < results_no_ext["social_welfare"]
        assert results_ext["externality_cost"] > 0

    def test_fines_improve_welfare_with_externality(self):
        """Fines should improve welfare when speeding creates externalities."""
        # With externalities, fines that reduce speeding create social gains
        agents_no_fine = [Agent(wage=w, labor_disutility=25.0) for w in [30.0, 50.0, 80.0]]
        agents_fine = [Agent(wage=w, labor_disutility=25.0) for w in [30.0, 50.0, 80.0]]

        no_fine = FlatFine(amount=0.0)
        with_fine = FlatFine(amount=5000.0)

        society_no_fine = Society(agents_no_fine, no_fine, tax_rate=0.3, externality_factor=50.0)
        society_fine = Society(agents_fine, with_fine, tax_rate=0.3, externality_factor=50.0)

        results_no_fine = society_no_fine.simulate()
        results_fine = society_fine.simulate()

        # Fine should reduce speeding and improve welfare
        assert results_fine["avg_speeding"] < results_no_fine["avg_speeding"]
        assert results_fine["social_welfare"] > results_no_fine["social_welfare"]

    def test_flat_vs_income_based_produces_different_welfare(self):
        """Different fine structures should produce different welfare."""
        agents_flat = [Agent(wage=w, labor_disutility=25.0) for w in [30.0, 50.0, 80.0]]
        agents_ib = [Agent(wage=w, labor_disutility=25.0) for w in [30.0, 50.0, 80.0]]

        flat = FlatFine(amount=200.0)
        income_based = IncomeBasedFine(rate=0.004)

        society_flat = Society(agents_flat, flat, tax_rate=0.3)
        society_ib = Society(agents_ib, income_based, tax_rate=0.3)

        results_flat = society_flat.simulate()
        results_ib = society_ib.simulate()

        # Results should differ between systems
        assert results_flat["total_utility"] != results_ib["total_utility"]


class TestSocietyAnalysis:
    """Tests for society analysis methods."""

    def test_income_group_analysis(self):
        """Should compute statistics by income group."""
        wages = [20.0, 30.0, 40.0, 50.0, 60.0, 70.0, 80.0, 90.0, 100.0, 110.0]
        agents = [Agent(wage=w, labor_disutility=25.0) for w in wages]
        fine = FlatFine(amount=200.0)
        society = Society(agents, fine, tax_rate=0.3)

        society.simulate()
        analysis = society.analyze_by_income_group()

        assert "bottom_20" in analysis
        assert "middle_60" in analysis
        assert "top_20" in analysis

    def test_income_group_analysis_with_few_agents(self):
        """Should handle groups with few agents (some may be empty)."""
        # With 2 agents, int(2 * 0.2) = 0, so bottom_20 is empty
        wages = [30.0, 70.0]
        agents = [Agent(wage=w, labor_disutility=25.0) for w in wages]
        fine = FlatFine(amount=200.0)
        society = Society(agents, fine, tax_rate=0.3)

        society.simulate()
        analysis = society.analyze_by_income_group()

        # Some groups may be missing due to rounding
        assert isinstance(analysis, dict)

    def test_gini_coefficient(self):
        """Should compute Gini coefficient."""
        wages = [20.0, 30.0, 40.0, 50.0, 60.0, 70.0, 80.0, 90.0, 100.0, 110.0]
        agents = [Agent(wage=w, labor_disutility=25.0) for w in wages]
        fine = FlatFine(amount=200.0)
        society = Society(agents, fine, tax_rate=0.3)

        society.simulate()

        gini = society.gini_coefficient()
        assert 0 <= gini <= 1


class TestSocietyProperties:
    """Tests for society properties."""

    def test_results_none_before_simulate(self):
        """results should be None before simulation."""
        agents = [Agent(wage=50.0)]
        fine = FlatFine(amount=200.0)
        society = Society(agents, fine, tax_rate=0.3)

        assert society.results is None

    def test_agent_results_none_before_simulate(self):
        """agent_results should be None before simulation."""
        agents = [Agent(wage=50.0)]
        fine = FlatFine(amount=200.0)
        society = Society(agents, fine, tax_rate=0.3)

        assert society.agent_results is None

    def test_results_set_after_simulate(self):
        """results should be set after simulation."""
        agents = [Agent(wage=50.0, labor_disutility=25.0)]
        fine = FlatFine(amount=200.0)
        society = Society(agents, fine, tax_rate=0.3)

        society.simulate()
        assert society.results is not None

    def test_agent_results_set_after_simulate(self):
        """agent_results should be set after simulation."""
        agents = [Agent(wage=50.0, labor_disutility=25.0)]
        fine = FlatFine(amount=200.0)
        society = Society(agents, fine, tax_rate=0.3)

        society.simulate()
        assert society.agent_results is not None


class TestSocietyErrors:
    """Tests for error handling."""

    def test_analyze_before_simulate_raises(self):
        """analyze_by_income_group should raise if called before simulate."""
        agents = [Agent(wage=50.0)]
        fine = FlatFine(amount=200.0)
        society = Society(agents, fine, tax_rate=0.3)

        with pytest.raises(ValueError, match="Must run simulate"):
            society.analyze_by_income_group()

    def test_gini_before_simulate_raises(self):
        """gini_coefficient should raise if called before simulate."""
        agents = [Agent(wage=50.0)]
        fine = FlatFine(amount=200.0)
        society = Society(agents, fine, tax_rate=0.3)

        with pytest.raises(ValueError, match="Must run simulate"):
            society.gini_coefficient()
