"""Agent module for traffic fines simulation."""

import numpy as np
from scipy import optimize
from typing import Callable, Tuple, Optional


class Agent:
    """
    Represents an economic agent who optimizes labor supply and speeding decisions.
    
    Agents face a utility function with:
    - Income utility (log utility from net income)
    - Labor disutility (quadratic in hours worked)
    - Speeding utility (log utility from speeding behavior)
    - Death probability cost (VSL-weighted expected mortality cost)
    """
    
    WORK_HOURS_PER_YEAR = 2080  # Standard full-time hours
    
    def __init__(
        self,
        potential_income: float,
        income_utility_factor: float = 1.0,
        labor_disutility_factor: float = 0.5,
        speeding_utility_factor: float = 0.1,
    ):
        """
        Initialize an agent with given characteristics.
        
        Parameters
        ----------
        potential_income : float
            Maximum annual income if working full-time
        income_utility_factor : float
            Weight on income in utility function
        labor_disutility_factor : float
            Weight on labor disutility
        speeding_utility_factor : float
            Weight on speeding pleasure
        """
        self.potential_income = np.float64(potential_income)
        self.wage_rate = self.potential_income / self.WORK_HOURS_PER_YEAR
        self.income_utility_factor = income_utility_factor
        self.labor_disutility_factor = labor_disutility_factor
        self.speeding_utility_factor = speeding_utility_factor
        
        # State variables (set during optimization)
        self.labor_hours: float = 0.0
        self.speeding: float = 0.0
        self.fine_paid: float = 0.0
        self.utility: float = 0.0
        
    def calculate_utility(
        self,
        labor_hours: float,
        speeding: float,
        fine_function: Callable[[float], float],
        death_prob: float,
        ubi: float,
        tax_rate: float,
        vsl: float,
    ) -> float:
        """
        Calculate agent's utility for given choices.
        
        Parameters
        ----------
        labor_hours : float
            Hours worked (0 to 2080)
        speeding : float
            Speeding intensity (0 to 1)
        fine_function : Callable
            Function mapping income to fine amount
        death_prob : float
            Probability of death per unit speeding
        ubi : float
            Universal basic income payment
        tax_rate : float
            Marginal tax rate on labor income
        vsl : float
            Value of statistical life
            
        Returns
        -------
        float
            Total utility
        """
        # Income calculations
        gross_income = self.wage_rate * labor_hours
        fine = fine_function(gross_income) * speeding
        tax = gross_income * tax_rate
        net_income = gross_income - fine - tax + ubi
        
        # Ensure positive net income for log utility
        net_income = max(net_income, 1e-10)
        
        # Utility components
        labor_disutility = (
            self.labor_disutility_factor 
            * (labor_hours ** 2) 
            / (2 * self.WORK_HOURS_PER_YEAR)
        )
        
        income_utility = self.income_utility_factor * np.log(1 + net_income)
        speeding_utility = self.speeding_utility_factor * np.log(1 + speeding)
        death_cost = death_prob * speeding * vsl
        
        total_utility = (
            income_utility
            + speeding_utility
            - labor_disutility
            - death_cost
        )
        
        return np.float64(total_utility)
    
    def optimize(
        self,
        fine_function: Callable[[float], float],
        death_prob: float,
        ubi: float,
        tax_rate: float,
        vsl: float,
    ) -> Tuple[float, float, float]:
        """
        Optimize agent's labor supply and speeding decisions.
        
        Parameters
        ----------
        fine_function : Callable
            Function mapping income to fine amount
        death_prob : float
            Probability of death per unit speeding
        ubi : float
            Universal basic income payment
        tax_rate : float
            Marginal tax rate on labor income
        vsl : float
            Value of statistical life
            
        Returns
        -------
        Tuple[float, float, float]
            Optimal (labor_hours, speeding, utility)
        """
        def objective(x):
            labor_hours, speeding = x
            return -self.calculate_utility(
                labor_hours, speeding, fine_function,
                death_prob, ubi, tax_rate, vsl
            )
        
        # Optimization bounds
        bounds = [
            (0, self.WORK_HOURS_PER_YEAR),  # Labor hours
            (0, 1),  # Speeding intensity
        ]
        
        # Initial guess (half-time work, moderate speeding)
        x0 = [self.WORK_HOURS_PER_YEAR / 2, 0.5]
        
        # Run optimization
        result = optimize.minimize(
            objective, x0, method="L-BFGS-B", bounds=bounds
        )
        
        if not result.success:
            # Fall back to simpler method if L-BFGS-B fails
            result = optimize.minimize(
                objective, x0, method="Nelder-Mead", bounds=bounds
            )
        
        # Store results
        self.labor_hours, self.speeding = result.x
        self.utility = -result.fun
        
        # Calculate fine paid
        gross_income = self.wage_rate * self.labor_hours
        self.fine_paid = fine_function(gross_income) * self.speeding
        
        return self.labor_hours, self.speeding, self.utility
    
    def get_effective_mtr(self, fine_function: Callable, tax_rate: float) -> float:
        """
        Calculate the effective marginal tax rate faced by the agent.
        
        Parameters
        ----------
        fine_function : Callable
            Function mapping income to fine amount
        tax_rate : float
            Explicit tax rate
            
        Returns
        -------
        float
            Effective marginal tax rate including fine effects
        """
        gross_income = self.wage_rate * self.labor_hours
        
        # Calculate marginal fine rate (derivative of fine function)
        epsilon = 1.0  # Small income change
        fine_base = fine_function(gross_income)
        fine_marginal = fine_function(gross_income + epsilon)
        marginal_fine_rate = (fine_marginal - fine_base) / epsilon * self.speeding
        
        return tax_rate + marginal_fine_rate