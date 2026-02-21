"""Agent optimization and mean-field equilibrium.

Implements:
1. Corrected utility: U = log(1+c) + α·log(1+s) - β·(h/H)²/2 - p(s)·VSL/(1+c)
2. Power-law death probability: p(s) = p_base·(1+s)^n (Nilsson 2004)
3. Fine structures: flat and income-based
4. Mean-field equilibrium with damped iteration
"""

from dataclasses import dataclass
from typing import Protocol

import numpy as np
from scipy.optimize import minimize


def death_probability(
    speeding: float, p_base: float, exponent: float
) -> float:
    """Nilsson (2004) power model for speed-fatality relationship.

    p(s) = p_base · (1 + s)^n, capped at 1.0.

    Args:
        speeding: Speeding intensity in [0, 1] (fraction above limit).
        p_base: Baseline annual traffic death probability.
        exponent: Power model exponent (n ≈ 4 for fatalities).

    Returns:
        Annual death probability.
    """
    if speeding < 0:
        raise ValueError(f"Speeding must be non-negative, got {speeding}")
    return min(1.0, p_base * (1.0 + speeding) ** exponent)


def utility(
    consumption: float,
    speeding: float,
    hours: float,
    alpha: float,
    beta: float,
    max_hours: float,
    vsl: float,
    p_base: float,
    exponent: float,
) -> float:
    """Corrected utility function.

    U = log(1+c) + α·log(1+s) - β·(h/H)²/2 - p(s)·VSL/(1+c)

    The death cost term p(s)·VSL·u'(c) = p(s)·VSL/(1+c) properly converts
    the monetary VSL into utility units by multiplying by marginal utility
    of consumption.

    Args:
        consumption: After-tax, after-fine consumption (EUR).
        speeding: Speeding intensity [0, 1].
        hours: Annual work hours.
        alpha: Weight on speeding utility.
        beta: Labor disutility coefficient.
        max_hours: Maximum annual hours (normalizer).
        vsl: Value of statistical life (EUR).
        p_base: Baseline death probability.
        exponent: Power model exponent.

    Returns:
        Utility level.
    """
    c = max(consumption, 1e-6)  # Floor to avoid log(0)
    s = max(speeding, 0.0)
    h_ratio = hours / max_hours

    log_consumption = np.log(1.0 + c)
    speeding_benefit = alpha * np.log(1.0 + s)
    labor_cost = beta * (h_ratio ** 2) / 2.0
    p_death = death_probability(s, p_base, exponent)
    death_cost = p_death * vsl / (1.0 + c)

    return log_consumption + speeding_benefit - labor_cost - death_cost


class FineSystem(Protocol):
    """Protocol for fine calculation."""

    def calculate(self, income: float, speeding: float) -> float: ...


@dataclass
class FlatFine:
    """Fixed fine regardless of income."""

    amount: float

    def calculate(self, income: float, speeding: float) -> float:
        return self.amount * speeding


@dataclass
class IncomeBasedFine:
    """Income-proportional fine (day-fine system)."""

    rate: float

    def calculate(self, income: float, speeding: float) -> float:
        return self.rate * income * speeding


@dataclass
class Agent:
    """An economic agent who optimizes labor supply and speeding."""

    wage: float
    alpha: float
    beta: float
    max_hours: float

    def optimize(
        self,
        fine_system: FineSystem,
        tax_rate: float,
        ubi: float,
        vsl: float,
        p_base: float,
        exponent: float,
    ) -> tuple[float, float]:
        """Find optimal (hours, speeding) given fine system and UBI.

        Returns:
            Tuple of (hours, speeding).
        """

        def neg_utility(x):
            h, s = x
            income = self.wage * h
            fine = fine_system.calculate(income, s)
            consumption = income * (1.0 - tax_rate) - fine + ubi
            if consumption <= 0:
                return 1e10  # Infeasible
            return -utility(
                consumption, s, h, self.alpha, self.beta,
                self.max_hours, vsl, p_base, exponent,
            )

        # Two starting points: interior + high-labor
        best_result = None
        best_val = np.inf

        for h0, s0 in [(self.max_hours / 2, 0.1), (self.max_hours * 0.75, 0.05)]:
            try:
                result = minimize(
                    neg_utility,
                    x0=[h0, s0],
                    method="L-BFGS-B",
                    bounds=[(1.0, self.max_hours), (0.0, 1.0)],
                )
                if result.fun < best_val:
                    best_val = result.fun
                    best_result = result
            except Exception:
                continue

        if best_result is None:
            return (self.max_hours / 2, 0.0)  # Fallback

        h_opt, s_opt = best_result.x
        return (float(np.clip(h_opt, 0, self.max_hours)),
                float(np.clip(s_opt, 0, 1)))


@dataclass
class EquilibriumResult:
    """Result of mean-field equilibrium computation."""

    hours: np.ndarray
    speeding: np.ndarray
    incomes: np.ndarray
    consumptions: np.ndarray
    utilities: np.ndarray
    fines_paid: np.ndarray
    ubi: float
    gini: float
    iterations: int
    max_delta: float
    converged: bool
    total_welfare: float
    mean_speeding: float
    total_fine_revenue: float
    total_tax_revenue: float


def _gini_coefficient(values: np.ndarray) -> float:
    """Compute Gini coefficient of an array of values."""
    v = np.sort(values)
    n = len(v)
    if n == 0 or np.sum(v) == 0:
        return 0.0
    index = np.arange(1, n + 1)
    return float((2.0 * np.sum(index * v) - (n + 1) * np.sum(v)) / (n * np.sum(v)))


def solve_equilibrium(
    wages: np.ndarray,
    fine_system: FineSystem,
    alpha: float,
    beta: float,
    max_hours: float,
    tax_rate: float,
    vsl: float,
    p_base: float,
    exponent: float,
    max_iter: int = 200,
    tol: float = 1e-4,
    damping: float = 0.5,
) -> EquilibriumResult:
    """Solve mean-field equilibrium with damped iteration.

    Fixed point: agents optimize given UBI → UBI = (taxes + fines) / N →
    aggregate speeding consistent.

    Args:
        wages: Array of agent wages.
        fine_system: Fine system to use.
        alpha: Speeding utility weight.
        beta: Labor disutility coefficient.
        max_hours: Maximum annual work hours.
        tax_rate: Proportional income tax rate.
        vsl: Value of statistical life.
        p_base: Baseline death probability.
        exponent: Speed-fatality exponent.
        max_iter: Maximum iterations.
        tol: Convergence tolerance on UBI.
        damping: Damping parameter λ ∈ (0, 1].

    Returns:
        EquilibriumResult with per-agent choices and aggregate statistics.
    """
    n = len(wages)
    agents = [Agent(wage=w, alpha=alpha, beta=beta, max_hours=max_hours) for w in wages]

    # Initialize UBI
    ubi = 0.0
    converged = False
    max_delta = np.inf

    for iteration in range(1, max_iter + 1):
        # Each agent optimizes given current UBI
        hours = np.zeros(n)
        speeding = np.zeros(n)

        for i, agent in enumerate(agents):
            h, s = agent.optimize(fine_system, tax_rate, ubi, vsl, p_base, exponent)
            hours[i] = h
            speeding[i] = s

        # Compute incomes and fines
        incomes = wages * hours
        fines = np.array([
            fine_system.calculate(inc, spd) for inc, spd in zip(incomes, speeding)
        ])
        tax_revenue = np.sum(incomes * tax_rate)
        fine_revenue = np.sum(fines)

        # New UBI = total revenue / N
        new_ubi = (tax_revenue + fine_revenue) / n

        # Damped update
        max_delta = abs(new_ubi - ubi)
        rel_delta = max_delta / max(abs(ubi), 1.0)
        ubi = damping * new_ubi + (1.0 - damping) * ubi

        if rel_delta < tol:
            converged = True
            break

    # Final computation
    consumptions = incomes * (1.0 - tax_rate) - fines + ubi
    utilities = np.array([
        utility(c, s, h, alpha, beta, max_hours, vsl, p_base, exponent)
        for c, s, h in zip(consumptions, speeding, hours)
    ])

    return EquilibriumResult(
        hours=hours,
        speeding=speeding,
        incomes=incomes,
        consumptions=consumptions,
        utilities=utilities,
        fines_paid=fines,
        ubi=ubi,
        gini=_gini_coefficient(consumptions),
        iterations=iteration,
        max_delta=max_delta,
        converged=converged,
        total_welfare=float(np.sum(utilities)),
        mean_speeding=float(np.mean(speeding)),
        total_fine_revenue=float(fine_revenue),
        total_tax_revenue=float(tax_revenue),
    )
