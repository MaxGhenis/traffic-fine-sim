"""Society simulation module."""

import numpy as np
from typing import List, Dict, Any, Optional
from .agent import Agent
from .fines import FineStructure


class Society:
    """
    Simulates a society of agents making labor and speeding decisions.
    
    The society evolves through iterations where:
    1. Agents optimize their decisions given current conditions
    2. Death probability updates based on aggregate speeding
    3. UBI is calculated from collected fines and taxes
    4. Process repeats until convergence or max iterations
    """
    
    def __init__(
        self,
        agents: List[Agent],
        fine_structure: FineStructure,
        tax_rate: float = 0.3,
        death_prob_factor: float = 0.0001,
        vsl: float = 10_000_000,
        convergence_threshold: float = 0.01,
    ):
        """
        Initialize society simulation.
        
        Parameters
        ----------
        agents : List[Agent]
            List of agents in the society
        fine_structure : FineStructure
            Fine system to use (flat or income-based)
        tax_rate : float
            Marginal tax rate on labor income
        death_prob_factor : float
            Factor converting average speeding to death probability
        vsl : float
            Value of statistical life
        convergence_threshold : float
            Threshold for convergence check
        """
        self.agents = agents
        self.fine_structure = fine_structure
        self.tax_rate = tax_rate
        self.death_prob_factor = death_prob_factor
        self.vsl = vsl
        self.convergence_threshold = convergence_threshold
        
        # State variables
        self.ubi = 0.0
        self.death_prob = 0.0
        self.total_utility = 0.0
        self.iteration = 0
        self.history = []
        
    def simulate(self, max_iterations: int = 100) -> Dict[str, Any]:
        """
        Run society simulation until convergence or max iterations.
        
        Parameters
        ----------
        max_iterations : int
            Maximum number of iterations
            
        Returns
        -------
        Dict[str, Any]
            Simulation results including final utilities, behaviors, etc.
        """
        previous_utility = -np.inf
        
        for self.iteration in range(max_iterations):
            # Update death probability based on current speeding
            avg_speeding = np.mean([a.speeding for a in self.agents])
            self.death_prob = self.death_prob_factor * avg_speeding
            
            # Each agent optimizes given current conditions
            total_fines = 0.0
            total_taxes = 0.0
            
            for agent in self.agents:
                labor, speeding, utility = agent.optimize(
                    lambda income: self.fine_structure.calculate_fine(income),
                    self.death_prob,
                    self.ubi,
                    self.tax_rate,
                    self.vsl
                )
                
                # Collect fines and taxes
                gross_income = agent.wage_rate * agent.labor_hours
                total_fines += agent.fine_paid
                total_taxes += gross_income * self.tax_rate
            
            # Update UBI from redistribution
            self.ubi = (total_fines + total_taxes) / len(self.agents)
            
            # Calculate total utility
            self.total_utility = sum(a.utility for a in self.agents)
            
            # Store history
            self.history.append({
                'iteration': self.iteration,
                'total_utility': self.total_utility,
                'avg_speeding': avg_speeding,
                'avg_labor': np.mean([a.labor_hours for a in self.agents]),
                'ubi': self.ubi,
                'death_prob': self.death_prob,
                'total_fines': total_fines,
                'total_taxes': total_taxes,
            })
            
            # Check for convergence
            if abs(self.total_utility - previous_utility) < self.convergence_threshold:
                print(f"Converged after {self.iteration + 1} iterations")
                break
            
            previous_utility = self.total_utility
        
        return self._compile_results()
    
    def _compile_results(self) -> Dict[str, Any]:
        """Compile simulation results."""
        # Income distribution analysis
        incomes = [a.potential_income for a in self.agents]
        income_quintiles = np.percentile(incomes, [20, 40, 60, 80])
        
        # Behavioral patterns by income group
        income_groups = {
            'bottom_20': [],
            'middle_60': [],
            'top_20': []
        }
        
        for agent in self.agents:
            if agent.potential_income <= income_quintiles[0]:
                group = 'bottom_20'
            elif agent.potential_income >= income_quintiles[3]:
                group = 'top_20'
            else:
                group = 'middle_60'
            
            income_groups[group].append({
                'labor_hours': agent.labor_hours,
                'speeding': agent.speeding,
                'utility': agent.utility,
                'fine_paid': agent.fine_paid,
                'effective_mtr': agent.get_effective_mtr(
                    lambda income: self.fine_structure.calculate_fine(income),
                    self.tax_rate
                )
            })
        
        # Calculate group averages
        group_stats = {}
        for group, agents_data in income_groups.items():
            if agents_data:
                group_stats[group] = {
                    'avg_labor': np.mean([a['labor_hours'] for a in agents_data]),
                    'avg_speeding': np.mean([a['speeding'] for a in agents_data]),
                    'avg_utility': np.mean([a['utility'] for a in agents_data]),
                    'avg_fine': np.mean([a['fine_paid'] for a in agents_data]),
                    'avg_effective_mtr': np.mean([a['effective_mtr'] for a in agents_data]),
                    'count': len(agents_data)
                }
        
        return {
            'total_utility': self.total_utility,
            'avg_utility': self.total_utility / len(self.agents),
            'avg_speeding': np.mean([a.speeding for a in self.agents]),
            'avg_labor_hours': np.mean([a.labor_hours for a in self.agents]),
            'avg_labor_supply': np.mean([a.labor_hours / Agent.WORK_HOURS_PER_YEAR 
                                         for a in self.agents]),
            'ubi': self.ubi,
            'death_prob': self.death_prob,
            'iterations': self.iteration + 1,
            'converged': self.iteration < 99,
            'income_groups': group_stats,
            'history': self.history,
            'agents': self.agents,
        }
    
    def calculate_welfare_metrics(self) -> Dict[str, float]:
        """
        Calculate various welfare metrics for the society.
        
        Returns
        -------
        Dict[str, float]
            Dictionary of welfare metrics
        """
        # Gini coefficient for utility
        utilities = sorted([a.utility for a in self.agents])
        n = len(utilities)
        cumsum = np.cumsum(utilities)
        gini = (2 * np.sum((i + 1) * u for i, u in enumerate(utilities))) / (n * cumsum[-1]) - (n + 1) / n
        
        # Deadweight loss approximation
        # Compare to first-best where speeding = 0 and labor is undistorted
        first_best_utility = 0
        for agent in self.agents:
            # First-best: no speeding, no fines, optimal labor given only tax
            def first_best_labor(hours):
                gross_income = agent.wage_rate * hours
                net_income = gross_income * (1 - self.tax_rate) + self.ubi
                labor_disutility = (
                    agent.labor_disutility_factor 
                    * (hours ** 2) 
                    / (2 * Agent.WORK_HOURS_PER_YEAR)
                )
                return -(agent.income_utility_factor * np.log(1 + net_income) - labor_disutility)
            
            from scipy.optimize import minimize_scalar
            result = minimize_scalar(first_best_labor, bounds=(0, Agent.WORK_HOURS_PER_YEAR), method='bounded')
            optimal_hours = result.x
            optimal_utility = -result.fun
            first_best_utility += optimal_utility
        
        deadweight_loss = first_best_utility - self.total_utility
        
        return {
            'total_utility': self.total_utility,
            'avg_utility': self.total_utility / len(self.agents),
            'utility_gini': gini,
            'deadweight_loss': deadweight_loss,
            'efficiency_ratio': self.total_utility / first_best_utility if first_best_utility > 0 else 0,
        }