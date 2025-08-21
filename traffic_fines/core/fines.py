"""Fine structure implementations."""

from abc import ABC, abstractmethod
from typing import List
import numpy as np


class FineStructure(ABC):
    """Abstract base class for fine structures."""
    
    @abstractmethod
    def calculate_fine(self, income: float) -> float:
        """Calculate fine amount for given income."""
        pass
    
    @abstractmethod
    def get_parameters(self) -> List[float]:
        """Get current fine parameters."""
        pass
    
    @abstractmethod
    def set_parameters(self, params: List[float]) -> None:
        """Set fine parameters."""
        pass
    
    @abstractmethod
    def get_marginal_rate(self, income: float) -> float:
        """Get marginal fine rate at given income level."""
        pass


class FlatFine(FineStructure):
    """
    Flat fine structure where all individuals pay the same amount.
    
    This represents the traditional approach where fines are set
    at a fixed dollar amount regardless of the violator's income.
    """
    
    def __init__(self, fine_amount: float = 100.0):
        """
        Initialize flat fine structure.
        
        Parameters
        ----------
        fine_amount : float
            Fixed fine amount for all violators
        """
        self.fine_amount = fine_amount
    
    def calculate_fine(self, income: float) -> float:
        """
        Calculate fine (constant regardless of income).
        
        Parameters
        ----------
        income : float
            Violator's income (ignored for flat fines)
            
        Returns
        -------
        float
            Fine amount
        """
        return self.fine_amount
    
    def get_parameters(self) -> List[float]:
        """Get fine parameters [fine_amount]."""
        return [self.fine_amount]
    
    def set_parameters(self, params: List[float]) -> None:
        """Set fine parameters from list."""
        if len(params) != 1:
            raise ValueError("FlatFine requires exactly 1 parameter")
        self.fine_amount = params[0]
    
    def get_marginal_rate(self, income: float) -> float:
        """
        Get marginal fine rate (always zero for flat fines).
        
        Parameters
        ----------
        income : float
            Income level
            
        Returns
        -------
        float
            Marginal rate (0 for flat fines)
        """
        return 0.0


class IncomeBasedFine(FineStructure):
    """
    Income-based fine structure where fines increase with income.
    
    This represents progressive fine systems like Finland's day-fine
    system, where fines are proportional to the violator's income.
    """
    
    def __init__(self, base_amount: float = 50.0, income_factor: float = 0.001):
        """
        Initialize income-based fine structure.
        
        Parameters
        ----------
        base_amount : float
            Minimum fine amount (for zero income)
        income_factor : float
            Proportion of income added to base amount
        """
        self.base_amount = base_amount
        self.income_factor = income_factor
    
    def calculate_fine(self, income: float) -> float:
        """
        Calculate fine based on income.
        
        Fine = base_amount + income_factor * income
        
        Parameters
        ----------
        income : float
            Violator's income
            
        Returns
        -------
        float
            Fine amount
        """
        return self.base_amount + self.income_factor * income
    
    def get_parameters(self) -> List[float]:
        """Get fine parameters [base_amount, income_factor]."""
        return [self.base_amount, self.income_factor]
    
    def set_parameters(self, params: List[float]) -> None:
        """Set fine parameters from list."""
        if len(params) != 2:
            raise ValueError("IncomeBasedFine requires exactly 2 parameters")
        self.base_amount = params[0]
        self.income_factor = params[1]
    
    def get_marginal_rate(self, income: float) -> float:
        """
        Get marginal fine rate (constant for linear income-based fines).
        
        Parameters
        ----------
        income : float
            Income level
            
        Returns
        -------
        float
            Marginal rate (income_factor)
        """
        return self.income_factor


class ProgressiveFine(FineStructure):
    """
    Progressive fine structure with increasing marginal rates.
    
    This implements a more complex progressive system where the
    marginal fine rate increases with income, similar to progressive
    income taxation.
    """
    
    def __init__(
        self,
        brackets: List[float] = None,
        rates: List[float] = None
    ):
        """
        Initialize progressive fine structure.
        
        Parameters
        ----------
        brackets : List[float]
            Income brackets for different rates
        rates : List[float]
            Fine rates for each bracket
        """
        if brackets is None:
            brackets = [0, 30000, 75000, 150000]
        if rates is None:
            rates = [0.001, 0.002, 0.004, 0.008]
        
        if len(brackets) != len(rates):
            raise ValueError("Number of brackets must equal number of rates")
        
        self.brackets = brackets
        self.rates = rates
    
    def calculate_fine(self, income: float) -> float:
        """
        Calculate fine using progressive brackets.
        
        Parameters
        ----------
        income : float
            Violator's income
            
        Returns
        -------
        float
            Fine amount
        """
        fine = 0.0
        
        for i in range(len(self.brackets)):
            if i == len(self.brackets) - 1:
                # Last bracket
                bracket_income = max(0, income - self.brackets[i])
                fine += bracket_income * self.rates[i]
            else:
                # Intermediate bracket
                bracket_start = self.brackets[i]
                bracket_end = self.brackets[i + 1]
                bracket_income = max(0, min(income, bracket_end) - bracket_start)
                fine += bracket_income * self.rates[i]
                
                if income <= bracket_end:
                    break
        
        return fine
    
    def get_parameters(self) -> List[float]:
        """Get fine parameters (flattened brackets and rates)."""
        return self.brackets + self.rates
    
    def set_parameters(self, params: List[float]) -> None:
        """Set fine parameters from list."""
        n = len(params) // 2
        self.brackets = params[:n]
        self.rates = params[n:]
    
    def get_marginal_rate(self, income: float) -> float:
        """
        Get marginal fine rate at given income level.
        
        Parameters
        ----------
        income : float
            Income level
            
        Returns
        -------
        float
            Marginal rate at this income
        """
        for i in range(len(self.brackets) - 1, -1, -1):
            if income >= self.brackets[i]:
                return self.rates[i]
        return self.rates[0]