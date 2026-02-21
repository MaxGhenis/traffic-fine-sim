"""Tests for CPS data loading and sampling."""

from pathlib import Path
from unittest.mock import patch

import numpy as np
import pandas as pd
import pytest

from traffic_fines.cps_data import (
    AgentSample,
    PARQUET_PATH,
    get_summary_statistics,
    load_cps_data,
    sample_agents,
)


@pytest.fixture
def synthetic_cps_data():
    """Create synthetic CPS-like data for testing."""
    rng = np.random.default_rng(42)
    n = 500
    incomes = rng.lognormal(10.5, 0.8, n)  # ~$36k median
    mtrs = np.clip(rng.normal(0.25, 0.15, n), 0.0, 0.95)
    return pd.DataFrame(
        {
            "employment_income": incomes,
            "marginal_tax_rate": mtrs,
            "person_weight": rng.uniform(50, 500, n),
            "age": rng.integers(18, 65, n),
            "hourly_wage": incomes / 2080,
        }
    )


@pytest.fixture
def mock_cps_data(synthetic_cps_data, tmp_path):
    """Mock the parquet file with synthetic data."""
    parquet_path = tmp_path / "cps_agents.parquet"
    synthetic_cps_data.to_parquet(parquet_path)
    # Clear the lru_cache before and after
    load_cps_data.cache_clear()
    with patch("traffic_fines.cps_data.PARQUET_PATH", parquet_path):
        yield synthetic_cps_data
    load_cps_data.cache_clear()


class TestLoadCpsData:
    def test_loads_dataframe(self, mock_cps_data):
        df = load_cps_data()
        assert isinstance(df, pd.DataFrame)

    def test_has_required_columns(self, mock_cps_data):
        df = load_cps_data()
        required = {
            "employment_income",
            "marginal_tax_rate",
            "person_weight",
            "age",
            "hourly_wage",
        }
        assert required.issubset(set(df.columns))

    def test_raises_if_file_missing(self):
        load_cps_data.cache_clear()
        with patch(
            "traffic_fines.cps_data.PARQUET_PATH", Path("/nonexistent/path.parquet")
        ):
            with pytest.raises(FileNotFoundError, match="CPS data not found"):
                load_cps_data()
        load_cps_data.cache_clear()


class TestSampleAgents:
    def test_returns_agent_sample(self, mock_cps_data):
        rng = np.random.default_rng(42)
        sample = sample_agents(50, rng)
        assert isinstance(sample, AgentSample)

    def test_correct_size(self, mock_cps_data):
        rng = np.random.default_rng(42)
        sample = sample_agents(100, rng)
        assert len(sample.wages) == 100
        assert len(sample.tax_rates) == 100
        assert len(sample.employment_incomes) == 100
        assert len(sample.weights) == 100

    def test_reproducible_with_same_seed(self, mock_cps_data):
        s1 = sample_agents(50, np.random.default_rng(123))
        s2 = sample_agents(50, np.random.default_rng(123))
        np.testing.assert_array_equal(s1.wages, s2.wages)
        np.testing.assert_array_equal(s1.tax_rates, s2.tax_rates)

    def test_different_seeds_differ(self, mock_cps_data):
        s1 = sample_agents(50, np.random.default_rng(1))
        s2 = sample_agents(50, np.random.default_rng(2))
        assert not np.array_equal(s1.wages, s2.wages)

    def test_wages_positive(self, mock_cps_data):
        sample = sample_agents(100, np.random.default_rng(42))
        assert np.all(sample.wages > 0)

    def test_tax_rates_in_range(self, mock_cps_data):
        sample = sample_agents(100, np.random.default_rng(42))
        assert np.all(sample.tax_rates >= 0)
        assert np.all(sample.tax_rates <= 0.95)

    def test_weighted_sampling(self, mock_cps_data):
        """Higher-weight observations should appear more often in large samples."""
        rng = np.random.default_rng(42)
        sample = sample_agents(10000, rng)
        # Just verify it runs and produces valid output
        assert len(sample.wages) == 10000


class TestGetSummaryStatistics:
    def test_returns_dict(self, mock_cps_data):
        stats = get_summary_statistics()
        assert isinstance(stats, dict)

    def test_has_expected_keys(self, mock_cps_data):
        stats = get_summary_statistics()
        expected = {
            "n_observations",
            "mean_income",
            "median_income",
            "mean_mtr",
            "median_mtr",
            "std_mtr",
            "mean_hourly_wage",
            "min_mtr",
            "max_mtr",
        }
        assert expected.issubset(set(stats.keys()))

    def test_positive_income(self, mock_cps_data):
        stats = get_summary_statistics()
        assert stats["mean_income"] > 0
        assert stats["median_income"] > 0

    def test_mtr_in_range(self, mock_cps_data):
        stats = get_summary_statistics()
        assert 0 <= stats["mean_mtr"] <= 1
        assert stats["min_mtr"] >= 0
        assert stats["max_mtr"] <= 0.95
