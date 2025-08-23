"""Counterfactual analysis with fixed labor supply."""

import numpy as np
from typing import List, Dict, Any, Tuple
from .agent import Agent
from .society import Society
from .fines import FineStructure


class FixedLaborAgent(Agent):
    """Agent with fixed labor supply for counterfactual analysis."""
    
    def __init__(
        self,
        potential_income: float,
        fixed_labor_supply: float = 0.5,  # Fixed at 50% of full-time
        income_utility_factor: float = 1.0,
        labor_disutility_factor: float = 0.5,
        speeding_utility_factor: float = 0.1,
    ):
        """Initialize agent with fixed labor supply."""
        super().__init__(
            potential_income,
            income_utility_factor,
            labor_disutility_factor,
            speeding_utility_factor
        )
        self.fixed_labor_supply = fixed_labor_supply
        
    def optimize(
        self,
        fine_function,
        death_prob: float,
        ubi: float,
        tax_rate: float,
        vsl: float,
    ) -> Tuple[float, float, float]:
        """
        Optimize only speeding decision with fixed labor supply.
        
        This counterfactual removes the labor supply channel to isolate
        the pure deterrence effect of different fine structures.
        """
        # Fix labor at predetermined level
        self.labor_hours = self.fixed_labor_supply * self.WORK_HOURS_PER_YEAR
        
        # Optimize only speeding
        from scipy.optimize import minimize_scalar
        
        def speeding_objective(speeding):
            return -self.calculate_utility(
                self.labor_hours,
                speeding,
                fine_function,
                death_prob,
                ubi,
                tax_rate,
                vsl
            )
        
        result = minimize_scalar(
            speeding_objective,
            bounds=(0, 1),
            method='bounded'
        )
        
        self.speeding = result.x
        self.utility = -result.fun
        
        # Calculate fine paid
        gross_income = self.wage_rate * self.labor_hours
        self.fine_paid = fine_function(gross_income) * self.speeding
        
        return self.labor_hours, self.speeding, self.utility


def compare_with_without_labor_response(
    incomes: np.ndarray,
    fine_structure_flat: FineStructure,
    fine_structure_income: FineStructure,
    tax_rate: float = 0.3,
    death_prob_factor: float = 0.0001,
    vsl: float = 10_000_000,
    max_iterations: int = 100,
    fixed_labor_supply: float = 0.5,
) -> Dict[str, Any]:
    """
    Compare welfare with and without labor supply responses.
    
    This function runs four simulations:
    1. Flat fine with endogenous labor
    2. Flat fine with fixed labor
    3. Income-based fine with endogenous labor
    4. Income-based fine with fixed labor
    
    Returns
    -------
    Dict containing welfare comparisons and decomposition
    """
    results = {}
    
    # 1. Flat fine with endogenous labor
    agents_flat_endo = [Agent(inc) for inc in incomes]
    society_flat_endo = Society(
        agents_flat_endo, fine_structure_flat, 
        tax_rate, death_prob_factor, vsl
    )
    results['flat_endogenous'] = society_flat_endo.simulate(max_iterations)
    
    # 2. Flat fine with fixed labor
    agents_flat_fixed = [
        FixedLaborAgent(inc, fixed_labor_supply) for inc in incomes
    ]
    society_flat_fixed = Society(
        agents_flat_fixed, fine_structure_flat,
        tax_rate, death_prob_factor, vsl
    )
    results['flat_fixed'] = society_flat_fixed.simulate(max_iterations)
    
    # 3. Income-based fine with endogenous labor
    agents_income_endo = [Agent(inc) for inc in incomes]
    society_income_endo = Society(
        agents_income_endo, fine_structure_income,
        tax_rate, death_prob_factor, vsl
    )
    results['income_endogenous'] = society_income_endo.simulate(max_iterations)
    
    # 4. Income-based fine with fixed labor
    agents_income_fixed = [
        FixedLaborAgent(inc, fixed_labor_supply) for inc in incomes
    ]
    society_income_fixed = Society(
        agents_income_fixed, fine_structure_income,
        tax_rate, death_prob_factor, vsl
    )
    results['income_fixed'] = society_income_fixed.simulate(max_iterations)
    
    # Calculate decomposition
    decomposition = {}
    
    # Total welfare effects
    decomposition['total_effect'] = (
        results['income_endogenous']['total_utility'] - 
        results['flat_endogenous']['total_utility']
    )
    
    # Pure deterrence effect (with fixed labor)
    decomposition['pure_deterrence'] = (
        results['income_fixed']['total_utility'] - 
        results['flat_fixed']['total_utility']
    )
    
    # Labor supply distortion effect
    decomposition['labor_distortion'] = (
        decomposition['total_effect'] - decomposition['pure_deterrence']
    )
    
    # Transfer/income effects
    decomposition['transfer_effect_flat'] = (
        results['flat_endogenous']['ubi'] * len(incomes)
    )
    decomposition['transfer_effect_income'] = (
        results['income_endogenous']['ubi'] * len(incomes)
    )
    decomposition['transfer_difference'] = (
        decomposition['transfer_effect_income'] - 
        decomposition['transfer_effect_flat']
    )
    
    return {
        'results': results,
        'decomposition': decomposition,
        'summary': {
            'total_welfare_change': decomposition['total_effect'],
            'due_to_deterrence': decomposition['pure_deterrence'],
            'due_to_labor_distortion': decomposition['labor_distortion'],
            'optimal_without_labor_response': 'Income-based' if decomposition['pure_deterrence'] > 0 else 'Flat',
            'optimal_with_labor_response': 'Income-based' if decomposition['total_effect'] > 0 else 'Flat',
        }
    }