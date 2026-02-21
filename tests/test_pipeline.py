"""Tests for pipeline.py — end-to-end orchestration and results.json generation."""

import json
import tempfile
from pathlib import Path
from unittest.mock import patch

import numpy as np
import pandas as pd
import pytest

from traffic_fines.cps_data import AgentSample
from traffic_fines.pipeline import AnalysisResults, run_analysis


FAST_FLAT_GRID = [100, 500]
FAST_IB_GRID = [0.02, 0.1]


@pytest.fixture(autouse=True)
def mock_cps(tmp_path):
    """Mock CPS data for pipeline tests."""
    rng = np.random.default_rng(99)
    n = 500
    incomes = rng.lognormal(10.5, 0.8, n)
    mtrs = np.clip(rng.normal(0.25, 0.15, n), 0.0, 0.95)
    df = pd.DataFrame({
        "employment_income": incomes,
        "marginal_tax_rate": mtrs,
        "person_weight": rng.uniform(50, 500, n),
        "age": rng.integers(18, 65, n),
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
def results() -> AnalysisResults:
    """Run a fast analysis for testing (tiny samples, small grids)."""
    return run_analysis(
        n_samples=10, n_agents=5, seed=42,
        flat_grid=FAST_FLAT_GRID, ib_grid=FAST_IB_GRID,
    )


class TestAnalysisStructure:
    def test_returns_analysis_results(self, results):
        assert isinstance(results, AnalysisResults)

    def test_has_seed(self, results):
        assert results.seed == 42

    def test_has_n_samples(self, results):
        assert results.n_samples == 10

    def test_has_flat_results(self, results):
        assert "welfare_mean" in results.flat
        assert "welfare_ci" in results.flat
        assert "speeding_mean" in results.flat
        assert "gini_mean" in results.flat

    def test_has_ib_results(self, results):
        assert "welfare_mean" in results.income_based
        assert "welfare_ci" in results.income_based
        assert "speeding_mean" in results.income_based

    def test_has_comparison(self, results):
        assert "welfare_difference_mean" in results.comparison
        assert "welfare_difference_ci" in results.comparison
        assert "p_flat_better" in results.comparison


class TestResultValues:
    def test_welfare_finite(self, results):
        assert np.isfinite(results.flat["welfare_mean"])
        assert np.isfinite(results.income_based["welfare_mean"])

    def test_speeding_in_range(self, results):
        assert 0 <= results.flat["speeding_mean"] <= 1
        assert 0 <= results.income_based["speeding_mean"] <= 1

    def test_gini_in_range(self, results):
        assert 0 <= results.flat["gini_mean"] <= 1
        assert 0 <= results.income_based["gini_mean"] <= 1

    def test_ci_ordered(self, results):
        ci = results.flat["welfare_ci"]
        assert ci[0] <= results.flat["welfare_mean"] <= ci[1]

    def test_p_flat_better_in_range(self, results):
        assert 0 <= results.comparison["p_flat_better"] <= 1


class TestSerialization:
    def test_to_dict(self, results):
        d = results.to_dict()
        assert isinstance(d, dict)
        assert "seed" in d
        assert "flat" in d
        assert "income_based" in d
        assert "comparison" in d

    def test_json_serializable(self, results):
        d = results.to_dict()
        s = json.dumps(d)
        assert isinstance(s, str)
        loaded = json.loads(s)
        assert loaded["seed"] == 42

    def test_save_and_load(self, results):
        with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as f:
            path = Path(f.name)
        results.save(path)
        loaded = AnalysisResults.load(path)
        assert loaded.seed == results.seed
        assert loaded.flat["welfare_mean"] == pytest.approx(
            results.flat["welfare_mean"]
        )
        path.unlink()


class TestReproducibility:
    def test_same_seed_same_results(self):
        r1 = run_analysis(n_samples=5, n_agents=5, seed=123)
        r2 = run_analysis(n_samples=5, n_agents=5, seed=123)
        assert r1.flat["welfare_mean"] == pytest.approx(r2.flat["welfare_mean"])
        assert r1.income_based["welfare_mean"] == pytest.approx(
            r2.income_based["welfare_mean"]
        )

    def test_different_seed_different_results(self):
        r1 = run_analysis(n_samples=5, n_agents=5, seed=1)
        r2 = run_analysis(n_samples=5, n_agents=5, seed=2)
        # Very unlikely to be exactly equal
        assert r1.flat["welfare_mean"] != pytest.approx(
            r2.flat["welfare_mean"], abs=1e-6
        )


class TestParametersStored:
    def test_parameters_in_results(self, results):
        assert "parameters" in results.to_dict()
        params = results.to_dict()["parameters"]
        assert "alpha_mean" in params
        assert "vsl_mean" in params
        assert "p_base_mean" in params
        assert "mtr_source" in params  # CPS-based MTRs, not scalar tax_rate
        assert "tax_rate_mean" not in params  # Removed: no longer a single prior
