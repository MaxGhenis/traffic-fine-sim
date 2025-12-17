"""Society simulation with equilibrium dynamics.

Simulates a society of heterogeneous agents who optimize their labor supply
and speeding decisions under different fine structures.
"""

from typing import Dict, Any, List
import numpy as np

from traffic_fines.core.agent import Agent
from traffic_fines.core.fines import FineStructure
from traffic_fines.utils.parameters import DEFAULT_PARAMS


class Society:
    """Society of agents with equilibrium simulation.

    Simulation iterates:
    1. Agents optimize given current UBI and death probability
    2. Collect fines and taxes
    3. Redistribute as UBI
    4. Update death probability from aggregate speeding
    5. Repeat until convergence
    """

    def __init__(
        self,
        agents: List[Agent],
        fine: FineStructure,
        tax_rate: float,
        death_prob_factor: float = DEFAULT_PARAMS.death_prob_factor,
    ):
        """Initialize society.

        Args:
            agents: List of Agent objects
            fine: Fine structure to use
            tax_rate: Income tax rate
            death_prob_factor: Factor to convert avg speeding to death probability
        """
        self.agents = agents
        self.fine = fine
        self.tax_rate = tax_rate
        self.death_prob_factor = death_prob_factor

        # Results storage
        self._results: Dict[str, Any] | None = None
        self._agent_results: List[Dict[str, Any]] | None = None

    def simulate(
        self,
        max_iterations: int = DEFAULT_PARAMS.max_iterations,
        convergence_threshold: float = DEFAULT_PARAMS.convergence_threshold,
    ) -> Dict[str, Any]:
        """Run equilibrium simulation.

        Args:
            max_iterations: Maximum iterations before stopping
            convergence_threshold: Utility change threshold for convergence

        Returns:
            Dict with simulation results
        """
        n_agents = len(self.agents)

        # Initial values
        ubi = 0.0
        death_prob = self.death_prob_factor * 0.5  # Initial guess

        prev_total_utility = float("-inf")
        converged = False

        for iteration in range(max_iterations):
            # Each agent optimizes
            total_utility = 0.0
            total_speeding = 0.0
            total_fines = 0.0
            total_taxes = 0.0

            agent_results = []
            for agent in self.agents:
                hours, speeding = agent.optimize(
                    self.fine, self.tax_rate, death_prob, ubi
                )

                gross_income = agent.gross_income(hours)
                tax_paid = gross_income * self.tax_rate
                fine_paid = self.fine.calculate(gross_income, speeding)
                net_income = agent.net_income(
                    hours, speeding, self.fine, self.tax_rate, ubi
                )
                utility = agent.total_utility(
                    hours, speeding, self.fine, self.tax_rate, death_prob, ubi
                )

                total_utility += utility
                total_speeding += speeding
                total_fines += fine_paid
                total_taxes += tax_paid

                agent_results.append(
                    {
                        "wage": agent.wage,
                        "hours": hours,
                        "speeding": speeding,
                        "gross_income": gross_income,
                        "net_income": net_income,
                        "tax_paid": tax_paid,
                        "fine_paid": fine_paid,
                        "utility": utility,
                    }
                )

            # Update UBI and death probability
            avg_speeding = total_speeding / n_agents
            ubi = (total_fines + total_taxes) / n_agents
            death_prob = self.death_prob_factor * avg_speeding

            # Check convergence
            if abs(total_utility - prev_total_utility) < convergence_threshold:
                converged = True
                break

            prev_total_utility = total_utility

        # Store results
        self._agent_results = agent_results
        self._results = {
            "total_utility": total_utility,
            "avg_speeding": avg_speeding,
            "total_fines": total_fines,
            "total_taxes": total_taxes,
            "ubi": ubi,
            "death_prob": death_prob,
            "iterations": iteration + 1,
            "converged": converged,
        }

        return self._results

    def analyze_by_income_group(self) -> Dict[str, Dict[str, float]]:
        """Analyze results by income groups (bottom 20%, middle 60%, top 20%).

        Returns:
            Dict with statistics for each income group
        """
        if self._agent_results is None:
            raise ValueError("Must run simulate() first")

        # Sort agents by wage
        sorted_results = sorted(self._agent_results, key=lambda x: x["wage"])
        n = len(sorted_results)

        # Define groups
        bottom_20_idx = int(n * 0.2)
        top_20_idx = int(n * 0.8)

        groups = {
            "bottom_20": sorted_results[:bottom_20_idx],
            "middle_60": sorted_results[bottom_20_idx:top_20_idx],
            "top_20": sorted_results[top_20_idx:],
        }

        analysis = {}
        for group_name, group_data in groups.items():
            if len(group_data) == 0:
                continue

            analysis[group_name] = {
                "avg_hours": np.mean([d["hours"] for d in group_data]),
                "avg_speeding": np.mean([d["speeding"] for d in group_data]),
                "avg_net_income": np.mean([d["net_income"] for d in group_data]),
                "avg_utility": np.mean([d["utility"] for d in group_data]),
                "avg_fine_paid": np.mean([d["fine_paid"] for d in group_data]),
            }

        return analysis

    def gini_coefficient(self) -> float:
        """Calculate Gini coefficient of net income distribution.

        Returns:
            Gini coefficient in [0, 1]
        """
        if self._agent_results is None:
            raise ValueError("Must run simulate() first")

        incomes = np.array([d["net_income"] for d in self._agent_results])
        incomes = np.sort(incomes)
        n = len(incomes)

        # Gini formula
        index = np.arange(1, n + 1)
        return (2 * np.sum(index * incomes) - (n + 1) * np.sum(incomes)) / (
            n * np.sum(incomes)
        )

    @property
    def results(self) -> Dict[str, Any] | None:
        """Return cached simulation results."""
        return self._results

    @property
    def agent_results(self) -> List[Dict[str, Any]] | None:
        """Return cached per-agent results."""
        return self._agent_results
