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


class HybridFine(FineStructure):
    """Hybrid fine structure - flat base plus income component.

    Fine = (flat_amount + rate * income) * speeding

    This allows optimizing over both flat and income-based components
    to find the welfare-maximizing combination.
    """

    def __init__(self, flat_amount: float, income_rate: float):
        """Initialize hybrid fine.

        Args:
            flat_amount: Base flat fine amount
            income_rate: Additional rate as fraction of income
        """
        self.flat_amount = flat_amount
        self.income_rate = income_rate

    def calculate(self, income: float, speeding: float) -> float:
        """Calculate fine: (flat_amount + rate * income) * speeding."""
        return max(0, (self.flat_amount + self.income_rate * income) * speeding)

    def marginal_rate(self, income: float, speeding: float) -> float:
        """Marginal rate is income_rate * speeding."""
        return self.income_rate * speeding


class BackwardLookingFine(FineStructure):
    """Backward-looking income-based fine (Finnish system).

    Fine = rate * lagged_income * speeding

    Uses previous year's income, so current labor decisions don't
    affect current fine liability. Marginal rate on current income is zero.
    """

    def __init__(self, rate: float, lagged_income: float):
        """Initialize backward-looking fine.

        Args:
            rate: Fine rate as fraction of lagged income
            lagged_income: Previous period's income (fixed)
        """
        self.rate = rate
        self.lagged_income = lagged_income

    def calculate(self, income: float, speeding: float) -> float:
        """Calculate fine based on lagged income."""
        return max(0, self.rate * self.lagged_income * speeding)

    def marginal_rate(self, income: float, speeding: float) -> float:
        """Marginal rate is zero - no current labor distortion."""
        return 0.0
