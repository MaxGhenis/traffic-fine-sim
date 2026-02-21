"""CPS microdata loading and sampling for the traffic fine simulation.

This module provides functions to load pre-generated CPS agent data and
sample from it using survey weights. The data must first be generated
by running `python scripts/generate_cps_data.py` (requires policyengine_us).
"""

from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

import numpy as np
import pandas as pd

DATA_DIR = Path(__file__).parent / "data"
PARQUET_PATH = DATA_DIR / "cps_agents.parquet"


@dataclass
class AgentSample:
    """Sample of agents drawn from CPS microdata."""

    wages: np.ndarray  # hourly wages
    tax_rates: np.ndarray  # marginal tax rates
    employment_incomes: np.ndarray
    weights: np.ndarray  # original survey weights


@lru_cache(maxsize=1)
def load_cps_data() -> pd.DataFrame:
    """Load CPS agent data from parquet. Cached after first call."""
    if not PARQUET_PATH.exists():
        raise FileNotFoundError(
            f"CPS data not found at {PARQUET_PATH}. "
            "Run `python scripts/generate_cps_data.py` first "
            "(requires policyengine_us)."
        )
    return pd.read_parquet(PARQUET_PATH)


def sample_agents(n_agents: int, rng: np.random.Generator) -> AgentSample:
    """Weighted bootstrap sample from CPS microdata.

    Samples with replacement using person_weight as probability weights.

    Args:
        n_agents: Number of agents to sample.
        rng: NumPy random generator for reproducibility.

    Returns:
        AgentSample with arrays of length n_agents.
    """
    df = load_cps_data()
    weights = df["person_weight"].values
    probs = weights / weights.sum()
    indices = rng.choice(len(df), size=n_agents, replace=True, p=probs)
    sampled = df.iloc[indices]
    return AgentSample(
        wages=sampled["hourly_wage"].values.copy(),
        tax_rates=sampled["marginal_tax_rate"].values.copy(),
        employment_incomes=sampled["employment_income"].values.copy(),
        weights=sampled["person_weight"].values.copy(),
    )


def get_summary_statistics() -> dict:
    """Summary statistics for the CPS agent data.

    Returns:
        Dictionary with descriptive statistics including counts,
        means, medians, and ranges for key variables.
    """
    df = load_cps_data()
    return {
        "n_observations": len(df),
        "mean_income": float(df["employment_income"].mean()),
        "median_income": float(df["employment_income"].median()),
        "mean_mtr": float(df["marginal_tax_rate"].mean()),
        "median_mtr": float(df["marginal_tax_rate"].median()),
        "std_mtr": float(df["marginal_tax_rate"].std()),
        "mean_hourly_wage": float(df["hourly_wage"].mean()),
        "min_mtr": float(df["marginal_tax_rate"].min()),
        "max_mtr": float(df["marginal_tax_rate"].max()),
    }
