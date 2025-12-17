"""Welfare optimizer for finding optimal fine parameters.

Finds fine parameters that maximize total social welfare.
"""

from typing import Dict, Any, List, Callable, Optional, Union
import numpy as np
from scipy.optimize import minimize_scalar, minimize

from traffic_fines.core.agent import Agent
from traffic_fines.core.society import Society
from traffic_fines.core.fines import FlatFine, IncomeBasedFine, HybridFine
from traffic_fines.utils.parameters import DEFAULT_PARAMS


def utilitarian_welfare(utilities: np.ndarray) -> float:
    """Sum of utilities."""
    return np.sum(utilities)


def rawlsian_welfare(utilities: np.ndarray) -> float:
    """Minimum utility (maximin)."""
    return np.min(utilities)


def atkinson_welfare(utilities: np.ndarray, gamma: float = 1.0) -> float:
    """Atkinson welfare with inequality aversion parameter gamma.

    Higher gamma means more weight on worse-off individuals.
    gamma=0 is utilitarian, gamma->inf is Rawlsian.
    """
    # Shift utilities to be positive
    u_shifted = utilities - np.min(utilities) + 1
    if gamma == 1:
        return np.sum(np.log(u_shifted))
    else:
        return np.sum(u_shifted ** (1 - gamma)) / (1 - gamma)


class WelfareOptimizer:
    """Optimizer for finding welfare-maximizing fine parameters."""

    def __init__(
        self,
        agents: List[Agent],
        externality_factor: float = DEFAULT_PARAMS.externality_factor,
    ):
        """Initialize optimizer.

        Args:
            agents: List of agents to use in simulations
            externality_factor: Social cost of speeding externality
        """
        self.agents = agents
        self.externality_factor = externality_factor
        self._history: List[Dict[str, Any]] = []

    def _evaluate_flat_fine(self, fine_amount: float, tax_rate: float) -> float:
        """Evaluate welfare for a given flat fine amount.

        Args:
            fine_amount: Flat fine amount
            tax_rate: Tax rate

        Returns:
            Negative social welfare (for minimization)
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
        society = Society(
            agents, fine, tax_rate, externality_factor=self.externality_factor
        )
        results = society.simulate(max_iterations=20)

        self._history.append(
            {
                "type": "flat",
                "fine_amount": fine_amount,
                "welfare": results["social_welfare"],
                "speeding": results["avg_speeding"],
            }
        )

        return -results["social_welfare"]

    def _evaluate_income_based_fine(self, fine_rate: float, tax_rate: float) -> float:
        """Evaluate welfare for a given income-based fine rate.

        Args:
            fine_rate: Income-based fine rate
            tax_rate: Tax rate

        Returns:
            Negative social welfare (for minimization)
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
        society = Society(
            agents, fine, tax_rate, externality_factor=self.externality_factor
        )
        results = society.simulate(max_iterations=20)

        self._history.append(
            {
                "type": "income_based",
                "fine_rate": fine_rate,
                "welfare": results["social_welfare"],
                "speeding": results["avg_speeding"],
            }
        )

        return -results["social_welfare"]

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

    def _get_welfare_function(
        self,
        welfare_function: str = "utilitarian",
        inequality_aversion: float = 1.0,
    ) -> Callable[[np.ndarray], float]:
        """Get welfare function by name.

        Args:
            welfare_function: One of "utilitarian", "rawlsian", "atkinson"
            inequality_aversion: Gamma parameter for Atkinson welfare

        Returns:
            Callable that takes utilities array and returns welfare value
        """
        if welfare_function == "utilitarian":
            return utilitarian_welfare
        elif welfare_function == "rawlsian":
            return rawlsian_welfare
        elif welfare_function == "atkinson":
            return lambda u: atkinson_welfare(u, inequality_aversion)
        else:
            raise ValueError(f"Unknown welfare function: {welfare_function}")

    def _evaluate_with_welfare(
        self,
        fine,
        tax_rate: float,
        welfare_fn: Callable[[np.ndarray], float],
    ) -> float:
        """Evaluate fine structure with custom welfare function.

        Args:
            fine: Fine structure to evaluate
            tax_rate: Tax rate
            welfare_fn: Custom welfare function

        Returns:
            Negative welfare (for minimization)
        """
        agents = [
            Agent(
                wage=a.wage,
                labor_disutility=a.labor_disutility,
                speeding_utility=a.speeding_utility,
                vsl=a.vsl,
            )
            for a in self.agents
        ]

        society = Society(
            agents, fine, tax_rate, externality_factor=self.externality_factor
        )
        results = society.simulate(max_iterations=20)

        # Compute individual utilities
        utilities = np.array(
            [
                a.total_utility(
                    a.optimal_hours,
                    a.optimal_speeding,
                    fine,
                    tax_rate,
                    results["death_prob"],
                    results["ubi"],
                )
                for a in agents
            ]
        )

        welfare = welfare_fn(utilities) - results["externality_cost"]

        # Track history
        self._history.append(
            {
                "welfare": welfare,
                "speeding": results["avg_speeding"],
            }
        )

        return -welfare

    def optimize_flat_fine(
        self,
        tax_rate: float,
        bounds: tuple = (0.0, 10000.0),
        welfare_function: str = "utilitarian",
        inequality_aversion: float = 1.0,
    ) -> Dict[str, Any]:
        """Find optimal flat fine amount.

        Args:
            tax_rate: Tax rate to use
            bounds: (min, max) bounds for fine amount
            welfare_function: One of "utilitarian", "rawlsian", "atkinson"
            inequality_aversion: Gamma parameter for Atkinson welfare

        Returns:
            Dict with optimal fine and welfare
        """
        self._history = []
        welfare_fn = self._get_welfare_function(welfare_function, inequality_aversion)

        def objective(fine_amount):
            return self._evaluate_with_welfare(
                FlatFine(amount=fine_amount), tax_rate, welfare_fn
            )

        result = minimize_scalar(objective, bounds=bounds, method="bounded")

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
        welfare_function: str = "utilitarian",
        inequality_aversion: float = 1.0,
    ) -> Dict[str, Any]:
        """Find optimal income-based fine rate.

        Args:
            tax_rate: Tax rate to use
            bounds: (min, max) bounds for fine rate
            welfare_function: One of "utilitarian", "rawlsian", "atkinson"
            inequality_aversion: Gamma parameter for Atkinson welfare

        Returns:
            Dict with optimal rate and welfare
        """
        self._history = []
        welfare_fn = self._get_welfare_function(welfare_function, inequality_aversion)

        def objective(fine_rate):
            return self._evaluate_with_welfare(
                IncomeBasedFine(rate=fine_rate), tax_rate, welfare_fn
            )

        result = minimize_scalar(objective, bounds=bounds, method="bounded")

        return {
            "optimal_rate": result.x,
            "welfare": -result.fun,
            "converged": result.success if hasattr(result, "success") else True,
            "history": self._history.copy(),
        }

    def optimize_hybrid_fine(
        self,
        tax_rate: float,
        constrain_rate_nonnegative: bool = True,
        welfare_function: str = "utilitarian",
        inequality_aversion: float = 1.0,
        flat_bounds: tuple = (0.0, 2000.0),
        rate_bounds: tuple = (-0.5, 0.1),
    ) -> Dict[str, Any]:
        """Find optimal hybrid fine (flat + income rate).

        Args:
            tax_rate: Tax rate to use
            constrain_rate_nonnegative: If True, income rate must be >= 0
            welfare_function: One of "utilitarian", "rawlsian", "atkinson"
            inequality_aversion: Gamma parameter for Atkinson welfare
            flat_bounds: (min, max) bounds for flat amount
            rate_bounds: (min, max) bounds for income rate

        Returns:
            Dict with optimal flat amount, income rate, and welfare
        """
        self._history = []
        welfare_fn = self._get_welfare_function(welfare_function, inequality_aversion)

        def objective(params):
            flat, rate = params
            # Check bounds
            if flat < flat_bounds[0] or flat > flat_bounds[1]:
                return 1e10
            if constrain_rate_nonnegative and rate < 0:
                return 1e10
            if rate < rate_bounds[0] or rate > rate_bounds[1]:
                return 1e10

            return self._evaluate_with_welfare(
                HybridFine(flat_amount=flat, income_rate=rate), tax_rate, welfare_fn
            )

        # Get initial guess from optimal flat (multi-start)
        flat_opt = self.optimize_flat_fine(
            tax_rate,
            welfare_function=welfare_function,
            inequality_aversion=inequality_aversion,
        )
        x0_base = [flat_opt["optimal_fine"], 0.0]

        # Use flat optimum welfare as baseline (hybrid with rate=0 should match)
        baseline_welfare = flat_opt["welfare"]

        # Try multiple starting points
        best_result = None
        starting_points = [
            x0_base,
            [500.0, 0.005 if constrain_rate_nonnegative else 0.0],
            [flat_opt["optimal_fine"], 0.01],
        ]

        for x0 in starting_points:
            result = minimize(
                objective,
                x0=x0,
                method="Nelder-Mead",
                options={"xatol": 1, "fatol": 0.001, "maxiter": 500},
            )
            if best_result is None or result.fun < best_result.fun:
                best_result = result

        result = best_result

        # Ensure we're at least as good as the flat optimum with rate=0
        if -result.fun < baseline_welfare:
            # Optimization found worse result, use flat optimum
            opt_flat = flat_opt["optimal_fine"]
            opt_rate = 0.0
            final_welfare = baseline_welfare
        else:
            opt_flat, opt_rate = result.x
            final_welfare = -result.fun

        return {
            "optimal_flat": opt_flat,
            "optimal_rate": opt_rate,
            "welfare": final_welfare,
            "converged": result.success,
            "history": self._history.copy(),
        }

    def sensitivity_analysis(
        self,
        tax_rate: float,
        parameter: str,
        values: List[float],
        welfare_function: str = "utilitarian",
        inequality_aversion: float = 1.0,
    ) -> List[Dict[str, Any]]:
        """Run sensitivity analysis over a parameter.

        Args:
            tax_rate: Baseline tax rate
            parameter: Parameter to vary ("externality_factor" or "tax_rate")
            values: List of values to test
            welfare_function: Welfare function to use
            inequality_aversion: Gamma for Atkinson welfare

        Returns:
            List of results for each parameter value
        """
        results = []

        for val in values:
            if parameter == "externality_factor":
                # Temporarily change externality factor
                old_ef = self.externality_factor
                self.externality_factor = val
                opt = self.optimize_flat_fine(
                    tax_rate=tax_rate,
                    welfare_function=welfare_function,
                    inequality_aversion=inequality_aversion,
                )
                self.externality_factor = old_ef
                results.append(
                    {
                        "externality_factor": val,
                        "optimal_flat": opt["optimal_fine"],
                        "welfare": opt["welfare"],
                    }
                )
            elif parameter == "tax_rate":
                opt = self.optimize_flat_fine(
                    tax_rate=val,
                    welfare_function=welfare_function,
                    inequality_aversion=inequality_aversion,
                )
                results.append(
                    {
                        "tax_rate": val,
                        "optimal_flat": opt["optimal_fine"],
                        "welfare": opt["welfare"],
                    }
                )
            else:
                raise ValueError(f"Unknown parameter: {parameter}")

        return results

    @staticmethod
    def sample_size_convergence(
        wage_pool: np.ndarray,
        sample_sizes: List[int],
        tax_rate: float,
        labor_disutility: float = 25.0,
        externality_factor: float = 0.2,
        seed: int = 42,
    ) -> List[Dict[str, Any]]:
        """Test convergence of optimal fine across sample sizes.

        Args:
            wage_pool: Pool of wages to sample from
            sample_sizes: List of sample sizes to test
            tax_rate: Tax rate to use
            labor_disutility: Labor disutility parameter
            externality_factor: Externality factor
            seed: Random seed

        Returns:
            List of results for each sample size
        """
        results = []
        np.random.seed(seed)

        for n in sample_sizes:
            # Sample wages
            wages = np.random.choice(wage_pool, size=n, replace=False)

            # Create agents
            agents = [Agent(wage=w, labor_disutility=labor_disutility) for w in wages]

            # Optimize
            optimizer = WelfareOptimizer(agents, externality_factor=externality_factor)
            opt = optimizer.optimize_flat_fine(tax_rate=tax_rate)

            results.append(
                {
                    "n_agents": n,
                    "optimal_flat": opt["optimal_fine"],
                    "welfare": opt["welfare"],
                }
            )

        return results
