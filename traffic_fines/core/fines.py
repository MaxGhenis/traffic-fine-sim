"""Fine structure implementations.

Defines abstract interface and concrete implementations for:
- FlatFine: Fixed amount independent of income
- IncomeBasedFine: Scales with income (Finnish day-fine style)
"""

from abc import ABC, abstractmethod


class FineStructure(ABC):
    """Abstract base class for fine structures."""

    @abstractmethod
    def calculate(self, income: float, speeding: float) -> float:
        """Calculate fine amount.

        Args:
            income: Agent's gross income
            speeding: Speeding intensity in [0, 1]

        Returns:
            Fine amount
        """
        pass

    @abstractmethod
    def marginal_rate(self, income: float, speeding: float) -> float:
        """Calculate marginal rate of fine with respect to income.

        This determines how much additional fine is paid per additional
        dollar of income, which affects labor supply incentives.

        Args:
            income: Agent's gross income
            speeding: Speeding intensity in [0, 1]

        Returns:
            Marginal fine rate (d Fine / d Income)
        """
        pass

    def effective_tax_rate(
        self, base_tax_rate: float, income: float, speeding: float
    ) -> float:
        """Calculate effective marginal tax rate including fine.

        Args:
            base_tax_rate: Base income tax rate
            income: Agent's gross income
            speeding: Speeding intensity in [0, 1]

        Returns:
            Effective marginal tax rate
        """
        return base_tax_rate + self.marginal_rate(income, speeding)


class FlatFine(FineStructure):
    """Flat fine structure - fixed amount independent of income.

    Fine = amount * speeding

    The marginal rate on income is zero, so this does not distort
    labor supply decisions (beyond income effects).
    """

    def __init__(self, amount: float):
        """Initialize flat fine.

        Args:
            amount: Fine amount at maximum speeding (speeding=1)
        """
        self.amount = amount

    def calculate(self, income: float, speeding: float) -> float:
        """Calculate fine: amount * speeding."""
        return self.amount * speeding

    def marginal_rate(self, income: float, speeding: float) -> float:
        """Marginal rate is zero for flat fines."""
        return 0.0


class IncomeBasedFine(FineStructure):
    """Income-based fine structure - scales with income.

    Fine = rate * income * speeding

    The marginal rate on income is (rate * speeding), creating an
    implicit tax that increases with speeding behavior.
    """

    def __init__(self, rate: float):
        """Initialize income-based fine.

        Args:
            rate: Fine rate as fraction of income per unit speeding
        """
        self.rate = rate

    def calculate(self, income: float, speeding: float) -> float:
        """Calculate fine: rate * income * speeding."""
        return self.rate * income * speeding

    def marginal_rate(self, income: float, speeding: float) -> float:
        """Marginal rate is rate * speeding."""
        return self.rate * speeding
