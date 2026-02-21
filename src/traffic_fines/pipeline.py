"""Pipeline: config → model → Monte Carlo → results.json.

Single entry point for generating all paper results.
"""

import json
from dataclasses import dataclass, field
from pathlib import Path

import numpy as np

from traffic_fines.config import load_priors
from traffic_fines.cps_data import sample_agents
from traffic_fines.model import FlatFine, IncomeBasedFine, solve_equilibrium
from traffic_fines.welfare import find_optimal_flat_fine, find_optimal_ib_rate

DATA_DIR = Path(__file__).parent / "data"


@dataclass
class AnalysisResults:
    """All results needed for the paper."""

    seed: int
    n_samples: int
    flat: dict = field(default_factory=dict)
    income_based: dict = field(default_factory=dict)
    comparison: dict = field(default_factory=dict)
    parameters: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {
            "seed": self.seed,
            "n_samples": self.n_samples,
            "flat": self.flat,
            "income_based": self.income_based,
            "comparison": self.comparison,
            "parameters": self.parameters,
        }

    def save(self, path: Path) -> None:
        with open(path, "w") as f:
            json.dump(self.to_dict(), f, indent=2)

    @classmethod
    def load(cls, path: Path) -> "AnalysisResults":
        with open(path) as f:
            d = json.load(f)
        return cls(
            seed=d["seed"],
            n_samples=d["n_samples"],
            flat=d["flat"],
            income_based=d["income_based"],
            comparison=d["comparison"],
            parameters=d.get("parameters", {}),
        )


def _clip_positive(val: float, min_val: float = 1e-6) -> float:
    return max(val, min_val)


def _summarize(values: np.ndarray, prefix: str) -> dict:
    """Summarize an array with mean and 95% CI, keyed by prefix."""
    return {
        f"{prefix}_mean": float(np.mean(values)),
        f"{prefix}_ci": [float(np.percentile(values, 2.5)), float(np.percentile(values, 97.5))],
    }


def run_analysis(
    n_samples: int = 100,
    n_agents: int = 10,
    seed: int = 42,
    flat_grid: list[float] | None = None,
    ib_grid: list[float] | None = None,
) -> AnalysisResults:
    """Run full Monte Carlo analysis with optimized fine levels.

    For each sample:
    1. Draw parameters from priors
    2. Generate wage distribution
    3. Find welfare-maximizing flat fine (grid search)
    4. Find welfare-maximizing income-based rate (grid search)
    5. Compare optimal flat vs optimal income-based
    """
    if flat_grid is None:
        flat_grid = [50, 100, 200, 500, 1000, 1500, 2000, 3000, 5000]
    if ib_grid is None:
        ib_grid = [0.001, 0.005, 0.01, 0.02, 0.03, 0.05, 0.08, 0.1]

    rng = np.random.default_rng(seed)
    priors = load_priors()

    # Storage
    flat_welfare = np.zeros(n_samples)
    ib_welfare = np.zeros(n_samples)
    flat_speeding = np.zeros(n_samples)
    ib_speeding = np.zeros(n_samples)
    flat_gini = np.zeros(n_samples)
    ib_gini = np.zeros(n_samples)
    optimal_flat_amounts = np.zeros(n_samples)
    optimal_ib_rates = np.zeros(n_samples)

    max_hours = priors.agent.max_hours.mean  # Fixed (sd=0 in priors)

    for i in range(n_samples):
        # Draw parameters from priors (clip to valid ranges)
        alpha = _clip_positive(rng.normal(priors.agent.alpha.mean, priors.agent.alpha.sd))
        beta = _clip_positive(rng.normal(priors.agent.beta.mean, priors.agent.beta.sd))
        vsl = _clip_positive(
            rng.normal(priors.safety.vsl.mean, priors.safety.vsl.sd), 100_000
        )
        p_base = _clip_positive(
            rng.normal(
                priors.safety.death_prob_base.mean, priors.safety.death_prob_base.sd
            )
        )
        exponent = max(
            1.0,
            rng.normal(
                priors.safety.speed_fatality_exponent.mean,
                priors.safety.speed_fatality_exponent.sd,
            ),
        )
        # Sample agents from CPS microdata
        agent_sample = sample_agents(n_agents, rng)
        wages = agent_sample.wages
        tax_rates = agent_sample.tax_rates

        shared = dict(
            alpha=alpha, beta=beta, max_hours=max_hours,
            tax_rates=tax_rates, vsl=vsl, p_base=p_base, exponent=exponent,
        )

        # Find optimal flat fine
        opt_flat_amt, _ = find_optimal_flat_fine(wages, fine_grid=flat_grid, **shared)
        eq_flat = solve_equilibrium(
            wages=wages, fine_system=FlatFine(amount=opt_flat_amt), **shared,
        )

        # Find optimal income-based rate
        opt_ib_rate, _ = find_optimal_ib_rate(wages, rate_grid=ib_grid, **shared)
        eq_ib = solve_equilibrium(
            wages=wages, fine_system=IncomeBasedFine(rate=opt_ib_rate), **shared,
        )

        flat_welfare[i] = eq_flat.total_welfare
        ib_welfare[i] = eq_ib.total_welfare
        flat_speeding[i] = eq_flat.mean_speeding
        ib_speeding[i] = eq_ib.mean_speeding
        flat_gini[i] = eq_flat.gini
        ib_gini[i] = eq_ib.gini
        optimal_flat_amounts[i] = opt_flat_amt
        optimal_ib_rates[i] = opt_ib_rate

    # Sign convention: flat - IB (negative means IB dominates).
    # Paper reports Delta W = IB - flat = -1 * this quantity.
    welfare_diff = flat_welfare - ib_welfare

    return AnalysisResults(
        seed=seed,
        n_samples=n_samples,
        flat={
            **_summarize(flat_welfare, "welfare"),
            **_summarize(flat_speeding, "speeding"),
            "gini_mean": float(np.mean(flat_gini)),
            **_summarize(optimal_flat_amounts, "optimal_amount"),
        },
        income_based={
            **_summarize(ib_welfare, "welfare"),
            **_summarize(ib_speeding, "speeding"),
            "gini_mean": float(np.mean(ib_gini)),
            **_summarize(optimal_ib_rates, "optimal_rate"),
        },
        comparison={
            **_summarize(welfare_diff, "welfare_difference"),
            "p_flat_better": float(np.mean(welfare_diff > 0)),
        },
        parameters={
            "alpha_mean": priors.agent.alpha.mean,
            "beta_mean": priors.agent.beta.mean,
            "vsl_mean": priors.safety.vsl.mean,
            "p_base_mean": priors.safety.death_prob_base.mean,
            "exponent_mean": priors.safety.speed_fatality_exponent.mean,
            "mtr_source": "PolicyEngine US Enhanced CPS 2024",
            "n_agents": n_agents,
            "flat_grid": flat_grid,
            "ib_grid": ib_grid,
        },
    )
