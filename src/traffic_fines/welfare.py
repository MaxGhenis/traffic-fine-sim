"""Welfare analysis functions for traffic fine simulation."""

import numpy as np

from traffic_fines.model import (
    EquilibriumResult,
    FlatFine,
    IncomeBasedFine,
    solve_equilibrium,
    utility,
)


def utilitarian_welfare(utilities: np.ndarray) -> float:
    """Sum of individual utilities."""
    return float(np.sum(utilities))


def rawlsian_welfare(utilities: np.ndarray) -> float:
    """Minimum individual utility (maximin criterion)."""
    return float(np.min(utilities))


def atkinson_welfare(
    values: np.ndarray, epsilon: float = 0.5, shift: float | None = None
) -> float:
    """Atkinson social welfare function applied to consumption levels.

    W = N * ((1/N) * sum(y_i^(1-e)))^(1/(1-e))  for e != 1
    W = N * (prod(y_i))^(1/N)                     for e == 1 (geometric mean)

    When epsilon=0, reduces to utilitarian (sum).
    As epsilon -> inf, approaches rawlsian (N * min).

    To handle non-positive values (which can arise when passing utility
    levels rather than consumption), all values are shifted so that the
    minimum is 1: y_shifted = y - shift + 1. When comparing two
    distributions, pass a common shift (e.g., the minimum across both)
    to ensure the Atkinson comparison is consistent, since the Atkinson
    SWF is not invariant to affine transformations when epsilon != 0.

    Args:
        values: Array of consumption levels (or utility levels, which
            will be shifted to ensure positivity).
        epsilon: Inequality aversion parameter.
        shift: Common floor for shifting. If None, uses min(values).
            When comparing two distributions, compute
            shift = min(min(A), min(B)) and pass it to both calls.

    Returns:
        Atkinson social welfare value.
    """
    n = len(values)

    # Shift values to ensure positivity if needed
    if shift is not None:
        floor = shift
    else:
        floor = np.min(values)

    if floor <= 0:
        y = values - floor + 1.0
    else:
        y = values

    if epsilon == 0.0:
        return float(np.sum(y))

    if abs(epsilon - 1.0) < 1e-12:
        # Geometric mean * N
        return float(n * np.exp(np.mean(np.log(y))))

    one_minus_e = 1.0 - epsilon
    mean_power = np.mean(y ** one_minus_e)
    return float(n * mean_power ** (1.0 / one_minus_e))


def welfare_decomposition(
    eq_flat: EquilibriumResult,
    eq_ib: EquilibriumResult,
    wages: np.ndarray,
    tax_rates: float | np.ndarray,
    alpha: float,
    beta: float,
    max_hours: float,
    vsl: float,
    p_base: float,
    exponent: float,
) -> dict:
    """Decompose welfare difference (IB minus flat) via counterfactuals.

    Uses a proper counterfactual approach rather than ad hoc proxies:

    1. **Deterrence channel**: Welfare gain from IB speeding levels,
       holding labor supply and transfers at flat-fine levels.
       deterrence = W(h_flat, s_ib, T_flat) - W(h_flat, s_flat, T_flat)

    2. **Revenue channel**: Welfare gain from the difference in
       equilibrium transfers (UBI), holding behavior at the
       counterfactual (h_flat, s_ib) point.
       revenue = W(h_flat, s_ib, T_ib) - W(h_flat, s_ib, T_flat)

    3. **Labor distortion**: Residual capturing the welfare effect of
       IB-induced labor supply changes.
       labor = total - deterrence - revenue

    Components sum exactly to the total welfare difference.

    Args:
        eq_flat: Equilibrium result under flat fines.
        eq_ib: Equilibrium result under income-based fines.
        wages: Agent wages (same array used to compute equilibria).
        tax_rates: Tax rate(s), scalar or per-agent array.
        alpha: Speeding utility weight.
        beta: Labor disutility coefficient.
        max_hours: Maximum annual work hours.
        vsl: Value of statistical life.
        p_base: Baseline death probability.
        exponent: Speed-fatality exponent.

    Returns:
        Dict with deterrence_gain, revenue_effect, labor_distortion,
        and total_difference. Components sum to total_difference.
    """
    n = len(wages)
    tax_arr = np.asarray(tax_rates, dtype=float)
    if tax_arr.ndim == 0:
        tax_arr = np.full(n, float(tax_arr))

    total_difference = eq_ib.total_welfare - eq_flat.total_welfare

    # Infer flat fine amount from equilibrium data:
    # FlatFine charges flat_amount * speeding, so flat_amount = fine / speeding
    nonzero_mask = eq_flat.speeding > 1e-10
    if np.any(nonzero_mask):
        flat_amount = float(np.median(
            eq_flat.fines_paid[nonzero_mask] / eq_flat.speeding[nonzero_mask]
        ))
    else:
        flat_amount = 0.0
    flat_fine_system = FlatFine(amount=flat_amount)

    def _counterfactual_welfare(hours, speeding, ubi_val):
        """Compute sum of utilities at given (h, s, T) combination."""
        utils = np.array([
            utility(
                consumption=max(
                    wages[i] * hours[i] * (1.0 - tax_arr[i])
                    - flat_fine_system.calculate(
                        wages[i] * hours[i], speeding[i]
                    )
                    + ubi_val,
                    1e-6,
                ),
                speeding=speeding[i],
                hours=hours[i],
                alpha=alpha,
                beta=beta,
                max_hours=max_hours,
                vsl=vsl,
                p_base=p_base,
                exponent=exponent,
            )
            for i in range(n)
        ])
        return float(np.sum(utils))

    # Baseline: W(h_flat, s_flat, T_flat) = eq_flat.total_welfare
    w_baseline = eq_flat.total_welfare

    # Counterfactual 1: W(h_flat, s_ib, T_flat)
    # Flat-fine labor supply and UBI, but IB speeding levels.
    # Isolates the welfare change from better deterrence alone.
    w_cf1 = _counterfactual_welfare(eq_flat.hours, eq_ib.speeding, eq_flat.ubi)

    # Counterfactual 2: W(h_flat, s_ib, T_ib)
    # Flat-fine labor supply, IB speeding, IB UBI.
    # Adding the revenue channel on top of deterrence.
    w_cf2 = _counterfactual_welfare(eq_flat.hours, eq_ib.speeding, eq_ib.ubi)

    # Deterrence channel: welfare change from IB speeding levels
    deterrence_gain = w_cf1 - w_baseline

    # Revenue channel: welfare change from the UBI difference
    revenue_effect = w_cf2 - w_cf1

    # Labor distortion: residual (labor supply changes + fine structure interaction)
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
    tax_rates: float,
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
            tax_rates=tax_rates, vsl=vsl, p_base=p_base, exponent=exponent,
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
    tax_rates: float,
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
        fine_grid = [25, 50, 100, 200, 500, 1000]

    return _grid_search_welfare(
        wages, fine_grid, lambda amt: FlatFine(amount=amt),
        alpha=alpha, beta=beta, max_hours=max_hours,
        tax_rates=tax_rates, vsl=vsl, p_base=p_base, exponent=exponent,
    )


def find_optimal_ib_rate(
    wages: np.ndarray,
    alpha: float,
    beta: float,
    max_hours: float,
    tax_rates: float,
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
        tax_rates=tax_rates, vsl=vsl, p_base=p_base, exponent=exponent,
    )
