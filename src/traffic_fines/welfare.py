"""Welfare analysis functions for traffic fine simulation."""

import numpy as np

from traffic_fines.model import (
    EquilibriumResult,
    FlatFine,
    IncomeBasedFine,
    solve_equilibrium,
)


def utilitarian_welfare(utilities: np.ndarray) -> float:
    """Sum of individual utilities."""
    return float(np.sum(utilities))


def rawlsian_welfare(utilities: np.ndarray) -> float:
    """Minimum individual utility (maximin criterion)."""
    return float(np.min(utilities))


def atkinson_welfare(utilities: np.ndarray, epsilon: float = 0.5) -> float:
    """Atkinson social welfare function.

    W = N * ((1/N) * sum(u^(1-e)))^(1/(1-e))  for e != 1
    W = N * (prod(u))^(1/N)                     for e == 1 (geometric mean)

    When epsilon=0, reduces to utilitarian (sum).
    As epsilon -> inf, approaches rawlsian (N * min).
    """
    n = len(utilities)
    if epsilon == 0.0:
        return float(np.sum(utilities))

    if abs(epsilon - 1.0) < 1e-12:
        # Geometric mean * N
        return float(n * np.exp(np.mean(np.log(utilities))))

    one_minus_e = 1.0 - epsilon
    mean_power = np.mean(utilities ** one_minus_e)
    return float(n * mean_power ** (1.0 / one_minus_e))


def welfare_decomposition(
    eq_flat: EquilibriumResult, eq_ib: EquilibriumResult
) -> dict:
    """Decompose welfare difference (income-based minus flat) into components.

    Components:
    - deterrence_gain: welfare from reduced speeding/deaths
    - labor_distortion: welfare loss from changed labor supply
    - revenue_effect: welfare from changed UBI (via revenue differences)
    """
    total_difference = eq_ib.total_welfare - eq_flat.total_welfare

    # Deterrence: difference in mean speeding as proxy for safety gain
    speeding_reduction = eq_flat.mean_speeding - eq_ib.mean_speeding
    deterrence_gain = speeding_reduction * abs(total_difference) if total_difference != 0 else 0.0

    # Revenue effect: difference in UBI
    revenue_effect = eq_ib.ubi - eq_flat.ubi

    # Labor distortion: residual so components sum to total
    labor_distortion = total_difference - deterrence_gain - revenue_effect

    return {
        "deterrence_gain": deterrence_gain,
        "labor_distortion": labor_distortion,
        "revenue_effect": revenue_effect,
        "total_difference": total_difference,
    }


def _grid_search_welfare(
    wages: np.ndarray,
    grid: list[float],
    make_fine_system,
    alpha: float,
    beta: float,
    max_hours: float,
    tax_rate: float,
    vsl: float,
    p_base: float,
    exponent: float,
) -> tuple[float, float]:
    """Grid search for the welfare-maximizing fine parameter.

    Args:
        wages: Agent wages.
        grid: Parameter values to search over.
        make_fine_system: Callable that takes a grid value and returns a FineSystem.

    Returns:
        (optimal_value, welfare) tuple.
    """
    best_value = grid[0]
    best_welfare = -np.inf

    for value in grid:
        eq = solve_equilibrium(
            wages, make_fine_system(value),
            alpha=alpha, beta=beta, max_hours=max_hours,
            tax_rate=tax_rate, vsl=vsl, p_base=p_base, exponent=exponent,
        )
        if eq.total_welfare > best_welfare:
            best_welfare = eq.total_welfare
            best_value = value

    return (float(best_value), float(best_welfare))


def find_optimal_flat_fine(
    wages: np.ndarray,
    alpha: float,
    beta: float,
    max_hours: float,
    tax_rate: float,
    vsl: float,
    p_base: float,
    exponent: float,
    fine_grid: list[float] | None = None,
) -> tuple[float, float]:
    """Grid search for welfare-maximizing flat fine.

    Returns:
        (optimal_amount, welfare) tuple.
    """
    if fine_grid is None:
        fine_grid = [50, 100, 200, 500, 1000, 2000, 5000]

    return _grid_search_welfare(
        wages, fine_grid, lambda amt: FlatFine(amount=amt),
        alpha=alpha, beta=beta, max_hours=max_hours,
        tax_rate=tax_rate, vsl=vsl, p_base=p_base, exponent=exponent,
    )


def find_optimal_ib_rate(
    wages: np.ndarray,
    alpha: float,
    beta: float,
    max_hours: float,
    tax_rate: float,
    vsl: float,
    p_base: float,
    exponent: float,
    rate_grid: list[float] | None = None,
) -> tuple[float, float]:
    """Grid search for welfare-maximizing income-based rate.

    Returns:
        (optimal_rate, welfare) tuple.
    """
    if rate_grid is None:
        rate_grid = [0.001, 0.002, 0.005, 0.01, 0.02, 0.05]

    return _grid_search_welfare(
        wages, rate_grid, lambda r: IncomeBasedFine(rate=r),
        alpha=alpha, beta=beta, max_hours=max_hours,
        tax_rate=tax_rate, vsl=vsl, p_base=p_base, exponent=exponent,
    )
