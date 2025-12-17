"""Default parameters calibrated to Finnish day-fine system."""

from dataclasses import dataclass, field
from typing import Dict, Any


@dataclass
class Parameters:
    """Simulation parameters with Finnish calibration defaults."""

    # Income distribution (EUR)
    mean_income: float = 45_000.0  # Finnish median ~45k EUR
    income_std: float = 25_000.0

    # Labor supply
    max_hours: float = 2080.0  # 52 weeks * 40 hours
    labor_disutility: float = 1.0  # Beta in h(l) = beta * l^2 / 2

    # Speeding utility
    speeding_utility: float = 0.5  # Alpha in v(s) = alpha * log(1 + s)

    # Safety
    vsl: float = 3_600_000.0  # EU recommendation for Finland (EUR)
    death_prob_factor: float = 0.0001  # Scales avg speeding to death probability

    # Tax system
    tax_rate: float = 0.30  # Base income tax rate

    # Fine structures
    flat_fine_amount: float = 200.0  # EUR
    income_fine_rate: float = 0.002  # Fraction of income per unit speeding

    # Simulation
    n_agents: int = 1000
    max_iterations: int = 100
    convergence_threshold: float = 1e-6

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "mean_income": self.mean_income,
            "income_std": self.income_std,
            "max_hours": self.max_hours,
            "labor_disutility": self.labor_disutility,
            "speeding_utility": self.speeding_utility,
            "vsl": self.vsl,
            "death_prob_factor": self.death_prob_factor,
            "tax_rate": self.tax_rate,
            "flat_fine_amount": self.flat_fine_amount,
            "income_fine_rate": self.income_fine_rate,
            "n_agents": self.n_agents,
            "max_iterations": self.max_iterations,
            "convergence_threshold": self.convergence_threshold,
        }


DEFAULT_PARAMS = Parameters()
