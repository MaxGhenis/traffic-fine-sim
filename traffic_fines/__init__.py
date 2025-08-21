"""
Traffic Fines Simulation Framework

A computational framework for analyzing welfare effects of income-based traffic fines.
"""

__version__ = "0.1.0"
__author__ = "Your Name"

from .core.agent import Agent
from .core.society import Society
from .core.fines import FlatFine, IncomeBasedFine
from .core.optimizer import WelfareOptimizer

__all__ = ["Agent", "Society", "FlatFine", "IncomeBasedFine", "WelfareOptimizer"]