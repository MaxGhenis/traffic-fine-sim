"""Forward Monte Carlo over parameter uncertainty.

Draws model parameters from their Normal priors, solves equilibrium
under both flat and income-based fine systems, and collects welfare,
speeding, and inequality outcomes across samples.
"""

from dataclasses import dataclass

import numpy as np

from traffic_fines.config import load_income_distribution, load_priors
from traffic_fines.model import FlatFine, IncomeBasedFine, solve_equilibrium


@dataclass
class MonteCarloResult:
    """Results from forward Monte Carlo simulation."""

    n_samples: int
    seed: int
    flat_welfare: np.ndarray  # (n_samples,)
    ib_welfare: np.ndarray  # (n_samples,)
    flat_speeding: np.ndarray  # (n_samples,)
    ib_speeding: np.ndarray  # (n_samples,)
    flat_gini: np.ndarray  # (n_samples,)
    ib_gini: np.ndarray  # (n_samples,)
    welfare_difference: np.ndarray  # flat - income_based
    param_draws: dict[str, np.ndarray]  # parameter name -> (n_samples,)


def run_montecarlo(
    n_samples: int = 100,
    seed: int = 42,
    n_agents: int = 10,
    flat_amount: float = 200.0,
    ib_rate: float = 0.002,
) -> MonteCarloResult:
    """Forward Monte Carlo over parameter uncertainty.

    For each sample:
    1. Draw alpha, beta, vsl, p_base, exponent, tax_rate from Normal priors
       (clipped to valid ranges).
    2. Generate wages from lognormal distribution.
    3. Solve equilibrium for flat fine.
    4. Solve equilibrium for income-based fine.
    5. Record welfare, speeding, gini.

    Args:
        n_samples: Number of Monte Carlo draws.
        seed: Random seed for reproducibility.
        n_agents: Number of agents per simulation.
        flat_amount: Flat fine amount (EUR).
        ib_rate: Income-based fine rate.

    Returns:
        MonteCarloResult with per-sample outcomes and parameter draws.
    """
    rng = np.random.default_rng(seed)
    priors = load_priors()
    income_dist = load_income_distribution()

    # Pre-allocate output arrays
    flat_welfare = np.zeros(n_samples)
    ib_welfare = np.zeros(n_samples)
    flat_speeding = np.zeros(n_samples)
    ib_speeding = np.zeros(n_samples)
    flat_gini = np.zeros(n_samples)
    ib_gini = np.zeros(n_samples)

    def _draw_clipped(prior, low, high) -> np.ndarray:
        """Draw n_samples from a Normal prior, clipped to [low, high]."""
        return np.clip(rng.normal(prior.mean, prior.sd, n_samples), low, high)

    # Draw all parameters up front for reproducibility
    param_draws = {
        "alpha": _draw_clipped(priors.agent.alpha, 0.01, np.inf),
        "beta": _draw_clipped(priors.agent.beta, 0.01, np.inf),
        "vsl": _draw_clipped(priors.safety.vsl, 1e4, np.inf),
        "p_base": _draw_clipped(priors.safety.death_prob_base, 1e-8, 0.1),
        "exponent": _draw_clipped(priors.safety.speed_fatality_exponent, 0.5, 10.0),
        "tax_rate": _draw_clipped(priors.fiscal.tax_rate, 0.01, 0.99),
    }

    # Fixed max_hours (sd=0 in priors)
    max_hours = priors.agent.max_hours.mean

    # Lognormal wage parameters from income distribution
    mu_log = np.log(
        income_dist.mean_income**2
        / np.sqrt(income_dist.income_std**2 + income_dist.mean_income**2)
    )
    sigma_log = np.sqrt(
        np.log(1 + (income_dist.income_std / income_dist.mean_income) ** 2)
    )

    flat_fine = FlatFine(amount=flat_amount)
    ib_fine = IncomeBasedFine(rate=ib_rate)

    for i in range(n_samples):
        # Generate wages (hourly) from lognormal
        annual_incomes = rng.lognormal(mu_log, sigma_log, n_agents)
        wages = annual_incomes / max_hours

        alpha = float(param_draws["alpha"][i])
        beta = float(param_draws["beta"][i])
        vsl = float(param_draws["vsl"][i])
        p_base = float(param_draws["p_base"][i])
        exponent = float(param_draws["exponent"][i])
        tax_rate = float(param_draws["tax_rate"][i])

        # Solve equilibrium under flat fine
        flat_result = solve_equilibrium(
            wages=wages,
            fine_system=flat_fine,
            alpha=alpha,
            beta=beta,
            max_hours=max_hours,
            tax_rate=tax_rate,
            vsl=vsl,
            p_base=p_base,
            exponent=exponent,
        )
        flat_welfare[i] = flat_result.total_welfare
        flat_speeding[i] = flat_result.mean_speeding
        flat_gini[i] = flat_result.gini

        # Solve equilibrium under income-based fine
        ib_result = solve_equilibrium(
            wages=wages,
            fine_system=ib_fine,
            alpha=alpha,
            beta=beta,
            max_hours=max_hours,
            tax_rate=tax_rate,
            vsl=vsl,
            p_base=p_base,
            exponent=exponent,
        )
        ib_welfare[i] = ib_result.total_welfare
        ib_speeding[i] = ib_result.mean_speeding
        ib_gini[i] = ib_result.gini

    return MonteCarloResult(
        n_samples=n_samples,
        seed=seed,
        flat_welfare=flat_welfare,
        ib_welfare=ib_welfare,
        flat_speeding=flat_speeding,
        ib_speeding=ib_speeding,
        flat_gini=flat_gini,
        ib_gini=ib_gini,
        welfare_difference=flat_welfare - ib_welfare,
        param_draws=param_draws,
    )
