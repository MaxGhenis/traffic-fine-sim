"""Welfare optimizer for finding optimal fine parameters.

Finds fine parameters that maximize total social welfare.
"""

from typing import Dict, Any, List, Callable
import numpy as np
from scipy.optimize import minimize_scalar, minimize

from traffic_fines.core.agent import Agent
from traffic_fines.core.society import Society
from traffic_fines.core.fines import FlatFine, IncomeBasedFine


class WelfareOptimizer:
    """Optimizer for finding welfare-maximizing fine parameters."""

    def __init__(self, agents: List[Agent]):
        """Initialize optimizer.

        Args:
            agents: List of agents to use in simulations
        """
        self.agents = agents
        self._history: List[Dict[str, Any]] = []

    def _evaluate_flat_fine(
        self, fine_amount: float, tax_rate: float
    ) -> float:
        """Evaluate welfare for a given flat fine amount.

        Args:
            fine_amount: Flat fine amount
            tax_rate: Tax rate

        Returns:
            Negative total welfare (for minimization)
        """
        # Create fresh agents for each evaluation
        agents = [
            Agent(
                wage=a.wage,
                labor_disutility=a.labor_disutility,
                speeding_utility=a.speeding_utility,
                vsl=a.vsl,
            )
            for a in self.agents
        ]

        fine = FlatFine(amount=fine_amount)
        society = Society(agents, fine, tax_rate)
        results = society.simulate(max_iterations=20)

        self._history.append(
            {
                "type": "flat",
                "fine_amount": fine_amount,
                "welfare": results["total_utility"],
            }
        )

        return -results["total_utility"]

    def _evaluate_income_based_fine(
        self, fine_rate: float, tax_rate: float
    ) -> float:
        """Evaluate welfare for a given income-based fine rate.

        Args:
            fine_rate: Income-based fine rate
            tax_rate: Tax rate

        Returns:
            Negative total welfare (for minimization)
        """
        # Create fresh agents for each evaluation
        agents = [
            Agent(
                wage=a.wage,
                labor_disutility=a.labor_disutility,
                speeding_utility=a.speeding_utility,
                vsl=a.vsl,
            )
            for a in self.agents
        ]

        fine = IncomeBasedFine(rate=fine_rate)
        society = Society(agents, fine, tax_rate)
        results = society.simulate(max_iterations=20)

        self._history.append(
            {
                "type": "income_based",
                "fine_rate": fine_rate,
                "welfare": results["total_utility"],
            }
        )

        return -results["total_utility"]

    def optimize_flat_fine(
        self,
        tax_rate: float,
        bounds: tuple = (0.0, 10000.0),
    ) -> Dict[str, Any]:
        """Find optimal flat fine amount.

        Args:
            tax_rate: Tax rate to use
            bounds: (min, max) bounds for fine amount

        Returns:
            Dict with optimal fine and welfare
        """
        self._history = []

        result = minimize_scalar(
            lambda x: self._evaluate_flat_fine(x, tax_rate),
            bounds=bounds,
            method="bounded",
        )

        return {
            "optimal_fine": result.x,
            "welfare": -result.fun,
            "converged": result.success if hasattr(result, "success") else True,
            "history": self._history.copy(),
        }

    def optimize_income_based_fine(
        self,
        tax_rate: float,
        bounds: tuple = (0.0, 0.1),
    ) -> Dict[str, Any]:
        """Find optimal income-based fine rate.

        Args:
            tax_rate: Tax rate to use
            bounds: (min, max) bounds for fine rate

        Returns:
            Dict with optimal rate and welfare
        """
        self._history = []

        result = minimize_scalar(
            lambda x: self._evaluate_income_based_fine(x, tax_rate),
            bounds=bounds,
            method="bounded",
        )

        return {
            "optimal_rate": result.x,
            "welfare": -result.fun,
            "converged": result.success if hasattr(result, "success") else True,
            "history": self._history.copy(),
        }

    def compare_systems(self, tax_rate: float) -> Dict[str, Any]:
        """Compare optimal flat vs income-based fines.

        Args:
            tax_rate: Tax rate to use

        Returns:
            Dict with results for both systems and comparison
        """
        flat_result = self.optimize_flat_fine(tax_rate)
        ib_result = self.optimize_income_based_fine(tax_rate)

        return {
            "flat": flat_result,
            "income_based": ib_result,
            "welfare_difference": flat_result["welfare"] - ib_result["welfare"],
            "flat_better": flat_result["welfare"] > ib_result["welfare"],
        }

    @property
    def history(self) -> List[Dict[str, Any]]:
        """Return optimization history."""
        return self._history
