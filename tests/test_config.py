"""Tests for traffic_fines.config module."""

import pytest

from traffic_fines.config import (
    AgentPriors,
    FineSystemConfig,
    FlatFineConfig,
    IncomeFineConfig,
    IncomeDistribution,
    ModelPriors,
    Prior,
    clear_cache,
    load_externalities,
    load_fine_systems,
    load_income_distribution,
    load_priors,
    validate,
)


@pytest.fixture(autouse=True)
def _clear():
    """Clear cache before each test."""
    clear_cache()


class TestLoadPriors:
    def test_load_priors_returns_model_priors(self):
        priors = load_priors()
        assert isinstance(priors, ModelPriors)
        assert isinstance(priors.agent, AgentPriors)
        assert isinstance(priors.agent.alpha, Prior)

    def test_priors_have_positive_sd(self):
        priors = load_priors()
        for prior in [
            priors.agent.alpha,
            priors.agent.beta,
            priors.safety.vsl,
            priors.safety.death_prob_base,
            priors.safety.speed_fatality_exponent,
            priors.labor.elasticity,
        ]:
            assert prior.sd >= 0, f"{prior.description} has negative sd"

    def test_priors_alpha_reasonable(self):
        priors = load_priors()
        assert 0 < priors.agent.alpha.mean < 2

    def test_priors_vsl_reasonable(self):
        priors = load_priors()
        assert 5_000_000 < priors.safety.vsl.mean < 20_000_000

    def test_priors_exponent_reasonable(self):
        priors = load_priors()
        assert 2 < priors.safety.speed_fatality_exponent.mean < 8


class TestLoadIncomeDistribution:
    def test_load_income_distribution(self):
        dist = load_income_distribution()
        assert isinstance(dist, IncomeDistribution)
        assert dist.type == "cps_microdata"

    def test_income_distribution_positive_values(self):
        dist = load_income_distribution()
        assert dist.mean_income > 0
        assert dist.income_std > 0
        assert dist.n_agents > 0


class TestLoadFineSystems:
    def test_load_fine_systems(self):
        fine = load_fine_systems()
        assert isinstance(fine, FineSystemConfig)
        assert isinstance(fine.flat, FlatFineConfig)
        assert isinstance(fine.income_based, IncomeFineConfig)

    def test_flat_fine_positive(self):
        fine = load_fine_systems()
        assert fine.flat.amount > 0

    def test_income_fine_rate_between_0_and_1(self):
        fine = load_fine_systems()
        assert 0 < fine.income_based.rate < 1


class TestLoadExternalities:
    def test_load_externalities(self):
        ext = load_externalities()
        assert isinstance(ext, dict)
        assert "congestion" in ext
        assert "environment" in ext


class TestValidate:
    def test_validate_returns_no_errors(self):
        errors = validate()
        assert errors == [], f"Validation errors: {errors}"


class TestCache:
    def test_cache_works(self):
        p1 = load_priors()
        p2 = load_priors()
        assert p1 is p2

    def test_clear_cache(self):
        p1 = load_priors()
        clear_cache()
        p2 = load_priors()
        assert p1 is not p2
