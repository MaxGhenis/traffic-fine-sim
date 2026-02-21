"""Tests for Monte Carlo uncertainty propagation."""

import numpy as np
import pandas as pd
import pytest
from unittest.mock import patch

from traffic_fines.montecarlo import MonteCarloResult, run_montecarlo


N_SAMPLES = 20
N_AGENTS = 5


@pytest.fixture(autouse=True)
def mock_cps(tmp_path):
    """Mock CPS data for MC tests."""
    rng_data = np.random.default_rng(99)
    n = 500
    incomes = rng_data.lognormal(10.5, 0.8, n)
    mtrs = np.clip(rng_data.normal(0.25, 0.15, n), 0.0, 0.95)
    df = pd.DataFrame({
        "employment_income": incomes,
        "marginal_tax_rate": mtrs,
        "person_weight": rng_data.uniform(50, 500, n),
        "age": rng_data.integers(18, 65, n),
        "hourly_wage": incomes / 2080,
    })
    parquet_path = tmp_path / "cps_agents.parquet"
    df.to_parquet(parquet_path)

    from traffic_fines import cps_data
    cps_data.load_cps_data.cache_clear()
    with patch.object(cps_data, "PARQUET_PATH", parquet_path):
        yield
    cps_data.load_cps_data.cache_clear()


@pytest.fixture
def mc_result():
    """Run Monte Carlo with small parameters for speed."""
    return run_montecarlo(n_samples=N_SAMPLES, seed=42, n_agents=N_AGENTS)


class TestMonteCarloResultShapes:
    """MonteCarloResult arrays have correct shapes."""

    def test_flat_welfare_shape(self, mc_result):
        assert mc_result.flat_welfare.shape == (N_SAMPLES,)

    def test_ib_welfare_shape(self, mc_result):
        assert mc_result.ib_welfare.shape == (N_SAMPLES,)

    def test_flat_speeding_shape(self, mc_result):
        assert mc_result.flat_speeding.shape == (N_SAMPLES,)

    def test_ib_speeding_shape(self, mc_result):
        assert mc_result.ib_speeding.shape == (N_SAMPLES,)

    def test_flat_gini_shape(self, mc_result):
        assert mc_result.flat_gini.shape == (N_SAMPLES,)

    def test_ib_gini_shape(self, mc_result):
        assert mc_result.ib_gini.shape == (N_SAMPLES,)

    def test_welfare_difference_shape(self, mc_result):
        assert mc_result.welfare_difference.shape == (N_SAMPLES,)

    def test_n_samples_stored(self, mc_result):
        assert mc_result.n_samples == N_SAMPLES

    def test_seed_stored(self, mc_result):
        assert mc_result.seed == 42


class TestReproducibility:
    """Same seed produces identical results; different seeds differ."""

    def test_same_seed_identical(self):
        r1 = run_montecarlo(n_samples=N_SAMPLES, seed=123, n_agents=N_AGENTS)
        r2 = run_montecarlo(n_samples=N_SAMPLES, seed=123, n_agents=N_AGENTS)
        np.testing.assert_array_equal(r1.flat_welfare, r2.flat_welfare)
        np.testing.assert_array_equal(r1.ib_welfare, r2.ib_welfare)
        np.testing.assert_array_equal(r1.welfare_difference, r2.welfare_difference)

    def test_different_seeds_differ(self):
        r1 = run_montecarlo(n_samples=N_SAMPLES, seed=1, n_agents=N_AGENTS)
        r2 = run_montecarlo(n_samples=N_SAMPLES, seed=2, n_agents=N_AGENTS)
        assert not np.array_equal(r1.flat_welfare, r2.flat_welfare)


class TestValueValidity:
    """Output values are finite and in valid ranges."""

    def test_welfare_finite(self, mc_result):
        assert np.all(np.isfinite(mc_result.flat_welfare))
        assert np.all(np.isfinite(mc_result.ib_welfare))

    def test_speeding_in_range(self, mc_result):
        assert np.all(mc_result.flat_speeding >= 0)
        assert np.all(mc_result.flat_speeding <= 1)
        assert np.all(mc_result.ib_speeding >= 0)
        assert np.all(mc_result.ib_speeding <= 1)

    def test_welfare_difference_consistent(self, mc_result):
        expected = mc_result.flat_welfare - mc_result.ib_welfare
        np.testing.assert_allclose(mc_result.welfare_difference, expected)


class TestConfidenceIntervals:
    """CI lower < mean < CI upper for welfare difference."""

    def test_ci_ordering(self, mc_result):
        diff = mc_result.welfare_difference
        mean = np.mean(diff)
        ci_lower = np.percentile(diff, 2.5)
        ci_upper = np.percentile(diff, 97.5)
        assert ci_lower < mean < ci_upper


class TestParameterDraws:
    """Parameter draws are stored with correct shapes."""

    def test_param_draws_keys(self, mc_result):
        expected_keys = {"alpha", "beta", "vsl", "p_base", "exponent"}
        assert set(mc_result.param_draws.keys()) == expected_keys

    def test_param_draws_shapes(self, mc_result):
        for name, draws in mc_result.param_draws.items():
            assert draws.shape == (N_SAMPLES,), f"{name} has wrong shape"

    def test_param_draws_finite(self, mc_result):
        for name, draws in mc_result.param_draws.items():
            assert np.all(np.isfinite(draws)), f"{name} has non-finite values"
