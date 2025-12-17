"""Agent class for economic optimization.

Agents optimize their labor supply and speeding decisions given:
- Wage rate (productivity)
- Tax rate
- Fine structure
- Death probability from speeding
- UBI transfers
"""

import numpy as np
from scipy.optimize import minimize

from traffic_fines.core.fines import FineStructure
from traffic_fines.utils.parameters import DEFAULT_PARAMS


class Agent:
    """Economic agent who optimizes labor supply and speeding decisions.

    Utility function:
        U = log(1 + consumption) + alpha*log(1 + speeding) - beta*hours^2/2 - death_prob*VSL

    Budget constraint:
        consumption = wage*hours*(1-tax) - fine(income, speeding) + ubi
    """

    def __init__(
        self,
        wage: float,
        labor_disutility: float = DEFAULT_PARAMS.labor_disutility,
        speeding_utility: float = DEFAULT_PARAMS.speeding_utility,
        vsl: float = DEFAULT_PARAMS.vsl,
        max_hours: float = DEFAULT_PARAMS.max_hours,
    ):
        """Initialize agent.

        Args:
            wage: Hourly wage rate
            labor_disutility: Beta parameter for h(l) = beta * l^2 / 2
            speeding_utility: Alpha parameter for v(s) = alpha * log(1 + s)
            vsl: Value of statistical life
            max_hours: Maximum annual work hours (default 2080)
        """
        self.wage = wage
        self.labor_disutility = labor_disutility
        self.speeding_utility = speeding_utility
        self.vsl = vsl
        self.max_hours = max_hours

        # Cached optimization results
        self._optimal_hours: float | None = None
        self._optimal_speeding: float | None = None

    def consumption_utility(self, consumption: float) -> float:
        """Log utility from consumption: u(c) = log(1 + c)."""
        return np.log(1 + max(0, consumption))

    def labor_disutility_fn(self, hours: float) -> float:
        """Quadratic disutility from labor: h(l) = beta * l^2 / 2.

        Args:
            hours: Work hours (0 to max_hours)
        """
        # Normalize to 0-1 scale for numerical stability
        l = hours / self.max_hours
        return self.labor_disutility * (l**2) / 2

    def speeding_utility_fn(self, speeding: float) -> float:
        """Log utility from speeding: v(s) = alpha * log(1 + s)."""
        return self.speeding_utility * np.log(1 + speeding)

    def death_cost(self, speeding: float, base_death_prob: float) -> float:
        """Expected cost of death: (base_prob + speeding * base_prob) * VSL.

        Individual death risk increases with speeding intensity.

        Args:
            speeding: Individual speeding intensity [0, 1]
            base_death_prob: Base death probability from aggregate speeding
        """
        individual_risk = base_death_prob * (1 + speeding)
        return individual_risk * self.vsl

    def gross_income(self, hours: float) -> float:
        """Calculate gross income: wage * hours."""
        return self.wage * hours

    def net_income(
        self,
        hours: float,
        speeding: float,
        fine: FineStructure,
        tax_rate: float,
        ubi: float,
    ) -> float:
        """Calculate net income after taxes, fines, and transfers.

        Args:
            hours: Work hours
            speeding: Speeding intensity [0, 1]
            fine: Fine structure
            tax_rate: Income tax rate
            ubi: Universal basic income transfer

        Returns:
            Net income (consumption)
        """
        gross = self.gross_income(hours)
        tax = gross * tax_rate
        fine_amount = fine.calculate(gross, speeding)
        return gross - tax - fine_amount + ubi

    def total_utility(
        self,
        hours: float,
        speeding: float,
        fine: FineStructure,
        tax_rate: float,
        death_prob: float,
        ubi: float,
    ) -> float:
        """Calculate total utility.

        U = log(1 + c) + alpha*log(1 + s) - beta*l^2/2 - p(s)*VSL
        """
        consumption = self.net_income(hours, speeding, fine, tax_rate, ubi)
        return (
            self.consumption_utility(consumption)
            + self.speeding_utility_fn(speeding)
            - self.labor_disutility_fn(hours)
            - self.death_cost(speeding, death_prob)
        )

    def optimize(
        self,
        fine: FineStructure,
        tax_rate: float,
        death_prob: float,
        ubi: float,
    ) -> tuple[float, float]:
        """Find optimal labor supply and speeding.

        Args:
            fine: Fine structure
            tax_rate: Income tax rate
            death_prob: Probability of death from speeding
            ubi: Universal basic income transfer

        Returns:
            Tuple of (optimal_hours, optimal_speeding)
        """

        def neg_utility(x: np.ndarray) -> float:
            hours, speeding = x[0], x[1]
            return -self.total_utility(hours, speeding, fine, tax_rate, death_prob, ubi)

        # Initial guess: work half time, moderate speeding
        x0 = np.array([self.max_hours / 2, 0.3])

        # Bounds: hours in [0, max_hours], speeding in [0, 1]
        bounds = [(0, self.max_hours), (1e-6, 1 - 1e-6)]

        result = minimize(
            neg_utility,
            x0,
            method="L-BFGS-B",
            bounds=bounds,
            options={"ftol": 1e-10, "gtol": 1e-8},
        )

        self._optimal_hours = float(result.x[0])
        self._optimal_speeding = float(result.x[1])

        return self._optimal_hours, self._optimal_speeding

    @property
    def optimal_hours(self) -> float | None:
        """Return cached optimal hours."""
        return self._optimal_hours

    @property
    def optimal_speeding(self) -> float | None:
        """Return cached optimal speeding."""
        return self._optimal_speeding
