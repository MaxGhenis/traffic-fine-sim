"""Tests for welfare analysis module."""

import numpy as np
import pytest

from traffic_fines.welfare import (
    atkinson_welfare,
    find_optimal_flat_fine,
    find_optimal_ib_rate,
    rawlsian_welfare,
    utilitarian_welfare,
    welfare_decomposition,
)
from traffic_fines.model import FlatFine, IncomeBasedFine, solve_equilibrium


# --- Shared test fixtures ---

WAGES = np.array([15.0, 25.0, 40.0, 60.0, 100.0])
PARAMS = dict(
    alpha=0.3,
    beta=1.0,
    max_hours=2080.0,
    tax_rates=0.3,
    vsl=5_000_000.0,
    p_base=5e-5,
    exponent=4.0,
)


@pytest.fixture
def eq_flat():
    return solve_equilibrium(WAGES, FlatFine(200.0), **PARAMS)


@pytest.fixture
def eq_ib():
    return solve_equilibrium(WAGES, IncomeBasedFine(0.005), **PARAMS)


# --- utilitarian_welfare ---


def test_utilitarian_welfare_returns_sum():
    utils = np.array([1.0, 2.0, 3.0])
    assert utilitarian_welfare(utils) == pytest.approx(6.0)


def test_utilitarian_welfare_single():
    utils = np.array([5.5])
    assert utilitarian_welfare(utils) == pytest.approx(5.5)


# --- rawlsian_welfare ---


def test_rawlsian_welfare_returns_min():
    utils = np.array([3.0, 1.0, 2.0])
    assert rawlsian_welfare(utils) == pytest.approx(1.0)


def test_rawlsian_welfare_equal():
    utils = np.array([4.0, 4.0, 4.0])
    assert rawlsian_welfare(utils) == pytest.approx(4.0)


# --- atkinson_welfare ---


def test_atkinson_epsilon_zero_is_utilitarian():
    utils = np.array([1.0, 2.0, 3.0, 4.0])
    aw = atkinson_welfare(utils, epsilon=0.0)
    uw = utilitarian_welfare(utils)
    assert aw == pytest.approx(uw, rel=1e-6)


def test_atkinson_high_epsilon_approaches_rawlsian():
    utils = np.array([2.0, 5.0, 8.0, 10.0])
    aw = atkinson_welfare(utils, epsilon=50.0)
    n = len(utils)
    rw = rawlsian_welfare(utils)
    # Atkinson with high epsilon approaches N * min(u)
    assert aw == pytest.approx(n * rw, rel=0.1)


def test_atkinson_moderate_epsilon():
    utils = np.array([1.0, 1.0, 1.0])
    # Equal utilities: any epsilon should give same result
    aw = atkinson_welfare(utils, epsilon=0.5)
    assert aw == pytest.approx(3.0, rel=1e-6)


def test_atkinson_epsilon_one():
    """epsilon=1 uses geometric mean formula."""
    utils = np.array([1.0, 4.0])
    aw = atkinson_welfare(utils, epsilon=1.0)
    # N * geometric_mean = N * (1*4)^(1/2) = 2 * 2 = 4
    assert aw == pytest.approx(4.0, rel=1e-6)


# --- welfare_decomposition ---


def test_welfare_decomposition_keys(eq_flat, eq_ib):
    result = welfare_decomposition(eq_flat, eq_ib)
    assert "deterrence_gain" in result
    assert "labor_distortion" in result
    assert "revenue_effect" in result
    assert "total_difference" in result


def test_welfare_decomposition_sums_to_total(eq_flat, eq_ib):
    result = welfare_decomposition(eq_flat, eq_ib)
    components_sum = (
        result["deterrence_gain"]
        + result["labor_distortion"]
        + result["revenue_effect"]
    )
    assert components_sum == pytest.approx(result["total_difference"], rel=1e-6)


def test_welfare_decomposition_total_matches_welfare_diff(eq_flat, eq_ib):
    result = welfare_decomposition(eq_flat, eq_ib)
    actual_diff = eq_ib.total_welfare - eq_flat.total_welfare
    assert result["total_difference"] == pytest.approx(actual_diff, rel=1e-6)


# --- find_optimal_flat_fine ---


def test_find_optimal_flat_fine_returns_positive():
    fine_grid = [50.0, 100.0, 200.0, 500.0]
    amount, welfare = find_optimal_flat_fine(WAGES, **PARAMS, fine_grid=fine_grid)
    assert amount > 0


def test_find_optimal_flat_fine_returns_best_from_grid():
    fine_grid = [50.0, 100.0, 200.0, 500.0]
    amount, welfare = find_optimal_flat_fine(WAGES, **PARAMS, fine_grid=fine_grid)
    # Verify it's actually from the grid
    assert amount in fine_grid


def test_find_optimal_flat_fine_welfare_is_float():
    fine_grid = [50.0, 100.0, 200.0]
    amount, welfare = find_optimal_flat_fine(WAGES, **PARAMS, fine_grid=fine_grid)
    assert isinstance(welfare, float)


# --- find_optimal_ib_rate ---


def test_find_optimal_ib_rate_returns_positive():
    rate_grid = [0.001, 0.002, 0.005]
    rate, welfare = find_optimal_ib_rate(WAGES, **PARAMS, rate_grid=rate_grid)
    assert rate > 0


def test_find_optimal_ib_rate_returns_best_from_grid():
    rate_grid = [0.001, 0.002, 0.005]
    rate, welfare = find_optimal_ib_rate(WAGES, **PARAMS, rate_grid=rate_grid)
    assert rate in rate_grid


def test_find_optimal_ib_rate_welfare_is_float():
    rate_grid = [0.001, 0.002, 0.005]
    rate, welfare = find_optimal_ib_rate(WAGES, **PARAMS, rate_grid=rate_grid)
    assert isinstance(welfare, float)
