"""Income distribution generation utilities."""

import numpy as np
from typing import Optional


def generate_income_distribution(
    n_agents: int,
    mean_income: float = 60_000,
    sd_income: float = 30_000,
    distribution: str = "lognormal",
    min_income: float = 10_000,
    max_income: float = 1_000_000,
    seed: Optional[int] = None,
) -> np.ndarray:
    """
    Generate income distribution for agents.

    Parameters
    ----------
    n_agents : int
        Number of agents
    mean_income : float
        Mean income
    sd_income : float
        Standard deviation of income
    distribution : str
        Type of distribution ('lognormal', 'normal', 'pareto', 'uniform')
    min_income : float
        Minimum income (for truncation)
    max_income : float
        Maximum income (for truncation)
    seed : int, optional
        Random seed for reproducibility

    Returns
    -------
    np.ndarray
        Array of incomes
    """
    if seed is not None:
        np.random.seed(seed)

    if distribution == "lognormal":
        # Calculate lognormal parameters from desired mean and std
        cv = sd_income / mean_income  # Coefficient of variation
        sigma = np.sqrt(np.log(1 + cv**2))
        mu = np.log(mean_income) - sigma**2 / 2
        incomes = np.random.lognormal(mu, sigma, n_agents)

    elif distribution == "normal":
        incomes = np.random.normal(mean_income, sd_income, n_agents)

    elif distribution == "pareto":
        # Pareto with shape parameter alpha
        alpha = 2.0  # Shape parameter (higher = less inequality)
        scale = mean_income * (alpha - 1) / alpha
        incomes = (np.random.pareto(alpha, n_agents) + 1) * scale

    elif distribution == "uniform":
        # Uniform distribution with same mean
        width = sd_income * np.sqrt(12)  # For matching std
        low = mean_income - width / 2
        high = mean_income + width / 2
        incomes = np.random.uniform(low, high, n_agents)

    else:
        raise ValueError(f"Unknown distribution type: {distribution}")

    # Truncate to reasonable bounds
    incomes = np.clip(incomes, min_income, max_income)

    return incomes.astype(np.float64)
