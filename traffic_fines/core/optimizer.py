"""Optimization module for finding welfare-maximizing parameters."""

import numpy as np
from scipy import optimize
from typing import Callable, Tuple, List, Dict, Any, Optional
from .society import Society
from .agent import Agent
from .fines import FineStructure, FlatFine, IncomeBasedFine


class WelfareOptimizer:
    """
    Optimizer for finding welfare-maximizing fine and tax parameters.

    This class implements the social planner's problem of choosing
    fine structures and tax rates to maximize total social welfare,
    accounting for behavioral responses including labor supply effects.
    """

    def __init__(
        self,
        incomes: np.ndarray,
        fine_structure_class: type,
        vsl: float = 10_000_000,
        death_prob_factor: float = 0.0001,
        income_utility_factor: float = 1.0,
        labor_disutility_factor: float = 0.5,
        speeding_utility_factor: float = 0.1,
        max_iterations: int = 100,
    ):
        """
        Initialize welfare optimizer.

        Parameters
        ----------
        incomes : np.ndarray
            Array of potential incomes for agents
        fine_structure_class : type
            Class of fine structure to optimize (FlatFine or IncomeBasedFine)
        vsl : float
            Value of statistical life
        death_prob_factor : float
            Factor converting average speeding to death probability
        income_utility_factor : float
            Weight on income in utility function
        labor_disutility_factor : float
            Weight on labor disutility
        speeding_utility_factor : float
            Weight on speeding pleasure
        max_iterations : int
            Maximum iterations for society simulation
        """
        self.incomes = incomes
        self.fine_structure_class = fine_structure_class
        self.vsl = vsl
        self.death_prob_factor = death_prob_factor
        self.income_utility_factor = income_utility_factor
        self.labor_disutility_factor = labor_disutility_factor
        self.speeding_utility_factor = speeding_utility_factor
        self.max_iterations = max_iterations

        # Optimization history
        self.history = []
        self.best_params = None
        self.best_utility = -np.inf

    def objective_function(self, params: np.ndarray) -> float:
        """
        Objective function for optimization (negative social welfare).

        Parameters
        ----------
        params : np.ndarray
            Parameters to optimize [fine_params..., tax_rate]

        Returns
        -------
        float
            Negative total utility (for minimization)
        """
        # Extract tax rate (last parameter)
        tax_rate = params[-1]
        fine_params = params[:-1]

        # Bounds checking
        if tax_rate < 0 or tax_rate > 1:
            return 1e10  # Penalty for invalid tax rate

        # Create fine structure with given parameters
        if self.fine_structure_class == FlatFine:
            fine_structure = FlatFine(fine_params[0])
        elif self.fine_structure_class == IncomeBasedFine:
            fine_structure = IncomeBasedFine(fine_params[0], fine_params[1])
        else:
            raise ValueError(
                f"Unknown fine structure class: {self.fine_structure_class}"
            )

        # Create agents
        agents = [
            Agent(
                income,
                self.income_utility_factor,
                self.labor_disutility_factor,
                self.speeding_utility_factor,
            )
            for income in self.incomes
        ]

        # Create and run society simulation
        society = Society(
            agents, fine_structure, tax_rate, self.death_prob_factor, self.vsl
        )

        try:
            results = society.simulate(self.max_iterations)
            total_utility = results["total_utility"]

            # Store in history
            self.history.append(
                {"params": params.copy(), "utility": total_utility, "results": results}
            )

            # Update best if improved
            if total_utility > self.best_utility:
                self.best_utility = total_utility
                self.best_params = params.copy()

            return -total_utility  # Negative for minimization

        except Exception as e:
            print(f"Simulation failed with params {params}: {e}")
            return 1e10  # Large penalty for failed simulation

    def optimize(
        self,
        initial_params: Optional[np.ndarray] = None,
        method: str = "L-BFGS-B",
        options: Optional[Dict] = None,
    ) -> Tuple[np.ndarray, float, List[Dict]]:
        """
        Find optimal fine and tax parameters.

        Parameters
        ----------
        initial_params : np.ndarray, optional
            Initial parameter values
        method : str
            Optimization method for scipy.optimize.minimize
        options : dict, optional
            Options for optimizer

        Returns
        -------
        Tuple[np.ndarray, float, List[Dict]]
            (optimal_params, optimal_utility, optimization_history)
        """
        # Set default initial parameters if not provided
        if initial_params is None:
            if self.fine_structure_class == FlatFine:
                # [fine_amount, tax_rate]
                initial_params = np.array([100.0, 0.3])
            elif self.fine_structure_class == IncomeBasedFine:
                # [base_amount, income_factor, tax_rate]
                initial_params = np.array([50.0, 0.001, 0.3])
            else:
                raise ValueError(
                    f"Unknown fine structure class: {self.fine_structure_class}"
                )

        # Set bounds based on fine structure
        if self.fine_structure_class == FlatFine:
            bounds = [
                (0, 10000),  # fine_amount
                (0, 0.9),  # tax_rate
            ]
        elif self.fine_structure_class == IncomeBasedFine:
            bounds = [
                (0, 1000),  # base_amount
                (0, 0.01),  # income_factor
                (0, 0.9),  # tax_rate
            ]
        else:
            bounds = None

        # Default options
        if options is None:
            options = {
                "maxiter": 100,
                "disp": True,
            }

        # Clear history
        self.history = []
        self.best_params = None
        self.best_utility = -np.inf

        # Run optimization
        result = optimize.minimize(
            self.objective_function,
            initial_params,
            method=method,
            bounds=bounds,
            options=options,
        )

        # Return best found (might not be final if optimization failed)
        if self.best_params is not None:
            return self.best_params, self.best_utility, self.history
        else:
            return result.x, -result.fun, self.history

    def compare_fine_structures(self, initial_tax_rate: float = 0.3) -> Dict[str, Any]:
        """
        Compare welfare under flat vs income-based fine structures.

        Parameters
        ----------
        initial_tax_rate : float
            Initial tax rate for both optimizations

        Returns
        -------
        Dict[str, Any]
            Comparison results including optimal parameters and welfare
        """
        results = {}

        # Optimize flat fine
        print("Optimizing flat fine structure...")
        flat_optimizer = WelfareOptimizer(
            self.incomes,
            FlatFine,
            self.vsl,
            self.death_prob_factor,
            self.income_utility_factor,
            self.labor_disutility_factor,
            self.speeding_utility_factor,
            self.max_iterations,
        )

        flat_initial = np.array([self.death_prob_factor * self.vsl, initial_tax_rate])
        flat_params, flat_utility, flat_history = flat_optimizer.optimize(flat_initial)

        results["flat"] = {
            "params": flat_params,
            "utility": flat_utility,
            "history": flat_history,
            "fine_amount": flat_params[0],
            "tax_rate": flat_params[1],
        }

        # Optimize income-based fine
        print("\nOptimizing income-based fine structure...")
        income_optimizer = WelfareOptimizer(
            self.incomes,
            IncomeBasedFine,
            self.vsl,
            self.death_prob_factor,
            self.income_utility_factor,
            self.labor_disutility_factor,
            self.speeding_utility_factor,
            self.max_iterations,
        )

        income_initial = np.array([50.0, 0.001, initial_tax_rate])
        income_params, income_utility, income_history = income_optimizer.optimize(
            income_initial
        )

        results["income_based"] = {
            "params": income_params,
            "utility": income_utility,
            "history": income_history,
            "base_amount": income_params[0],
            "income_factor": income_params[1],
            "tax_rate": income_params[2],
        }

        # Calculate welfare difference
        results["welfare_difference"] = income_utility - flat_utility
        results["welfare_pct_change"] = (
            (income_utility - flat_utility) / flat_utility * 100
        )

        return results
