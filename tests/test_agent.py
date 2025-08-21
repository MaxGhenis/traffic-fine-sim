"""Tests for Agent module."""

import pytest
import numpy as np
from traffic_fines.core.agent import Agent
from traffic_fines.core.fines import FlatFine, IncomeBasedFine


class TestAgent:
    """Test suite for Agent class."""
    
    def test_agent_initialization(self):
        """Test agent initialization with default parameters."""
        agent = Agent(potential_income=60000)
        
        assert agent.potential_income == 60000
        assert agent.wage_rate == pytest.approx(60000 / 2080)
        assert agent.labor_hours == 0.0
        assert agent.speeding == 0.0
        assert agent.fine_paid == 0.0
    
    def test_utility_calculation_zero_labor(self):
        """Test utility calculation with zero labor supply."""
        agent = Agent(potential_income=60000)
        fine_structure = FlatFine(100)
        
        utility = agent.calculate_utility(
            labor_hours=0,
            speeding=0,
            fine_function=lambda income: fine_structure.calculate_fine(income),
            death_prob=0.0001,
            ubi=1000,
            tax_rate=0.3,
            vsl=10_000_000
        )
        
        # With zero labor and speeding, utility should come only from UBI
        assert utility > 0  # Log(1 + 1000) > 0
    
    def test_utility_calculation_full_labor(self):
        """Test utility calculation with full labor supply."""
        agent = Agent(potential_income=60000)
        fine_structure = FlatFine(100)
        
        utility = agent.calculate_utility(
            labor_hours=2080,
            speeding=0,
            fine_function=lambda income: fine_structure.calculate_fine(income),
            death_prob=0.0001,
            ubi=0,
            tax_rate=0.3,
            vsl=10_000_000
        )
        
        # Utility should balance income gain against labor disutility
        assert isinstance(utility, (float, np.float64))
    
    def test_optimization_flat_fine(self):
        """Test agent optimization with flat fine."""
        agent = Agent(
            potential_income=60000,
            income_utility_factor=1.0,
            labor_disutility_factor=0.5,
            speeding_utility_factor=0.1
        )
        fine_structure = FlatFine(100)
        
        labor, speeding, utility = agent.optimize(
            fine_function=lambda income: fine_structure.calculate_fine(income),
            death_prob=0.0001,
            ubi=0,
            tax_rate=0.3,
            vsl=10_000_000
        )
        
        # Check optimization results are reasonable
        assert 0 <= labor <= 2080
        assert 0 <= speeding <= 1
        assert isinstance(utility, (float, np.float64))
        assert agent.labor_hours == labor
        assert agent.speeding == speeding
    
    def test_optimization_income_based_fine(self):
        """Test agent optimization with income-based fine."""
        agent = Agent(
            potential_income=60000,
            income_utility_factor=1.0,
            labor_disutility_factor=0.5,
            speeding_utility_factor=0.1
        )
        fine_structure = IncomeBasedFine(base_amount=50, income_factor=0.001)
        
        labor, speeding, utility = agent.optimize(
            fine_function=lambda income: fine_structure.calculate_fine(income),
            death_prob=0.0001,
            ubi=0,
            tax_rate=0.3,
            vsl=10_000_000
        )
        
        # Check optimization results
        assert 0 <= labor <= 2080
        assert 0 <= speeding <= 1
        assert isinstance(utility, (float, np.float64))
    
    def test_effective_mtr_flat_fine(self):
        """Test effective MTR calculation with flat fine."""
        agent = Agent(potential_income=60000)
        agent.labor_hours = 1040  # Half-time
        agent.speeding = 0.5
        
        fine_structure = FlatFine(100)
        effective_mtr = agent.get_effective_mtr(
            lambda income: fine_structure.calculate_fine(income),
            tax_rate=0.3
        )
        
        # Flat fine shouldn't add to MTR
        assert effective_mtr == pytest.approx(0.3, rel=0.01)
    
    def test_effective_mtr_income_based_fine(self):
        """Test effective MTR calculation with income-based fine."""
        agent = Agent(potential_income=60000)
        agent.labor_hours = 1040  # Half-time
        agent.speeding = 0.5
        
        fine_structure = IncomeBasedFine(base_amount=50, income_factor=0.001)
        effective_mtr = agent.get_effective_mtr(
            lambda income: fine_structure.calculate_fine(income),
            tax_rate=0.3
        )
        
        # Income-based fine should increase effective MTR
        # MTR = 0.3 + 0.001 * 0.5 = 0.3005
        assert effective_mtr > 0.3
        assert effective_mtr == pytest.approx(0.3 + 0.001 * 0.5, rel=0.01)
    
    def test_high_income_agent(self):
        """Test behavior of high-income agent."""
        agent = Agent(
            potential_income=200000,
            income_utility_factor=1.0,
            labor_disutility_factor=0.5,
            speeding_utility_factor=0.1
        )
        fine_structure = IncomeBasedFine(base_amount=50, income_factor=0.001)
        
        labor, speeding, utility = agent.optimize(
            fine_function=lambda income: fine_structure.calculate_fine(income),
            death_prob=0.0001,
            ubi=0,
            tax_rate=0.3,
            vsl=10_000_000
        )
        
        # High income agents should still optimize rationally
        assert 0 <= labor <= 2080
        assert 0 <= speeding <= 1
    
    def test_low_income_agent(self):
        """Test behavior of low-income agent."""
        agent = Agent(
            potential_income=20000,
            income_utility_factor=1.0,
            labor_disutility_factor=0.5,
            speeding_utility_factor=0.1
        )
        fine_structure = FlatFine(100)
        
        labor, speeding, utility = agent.optimize(
            fine_function=lambda income: fine_structure.calculate_fine(income),
            death_prob=0.0001,
            ubi=500,
            tax_rate=0.3,
            vsl=10_000_000
        )
        
        # Low income agents should respond to incentives
        assert 0 <= labor <= 2080
        assert 0 <= speeding <= 1