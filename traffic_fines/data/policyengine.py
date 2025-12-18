"""PolicyEngine US integration for computing marginal tax rates.

This module provides functions to compute marginal tax rates (MTRs) using
PolicyEngine US, which models the complete US federal and state tax system.
"""

from typing import List, Optional
import numpy as np

from traffic_fines.core.agent import Agent
from traffic_fines.utils.parameters import DEFAULT_PARAMS

# Lazy import to avoid requiring policyengine-us unless needed
_simulation = None


def _get_simulation():
    """Get or create PolicyEngine US simulation (cached)."""
    global _simulation
    if _simulation is None:
        from policyengine_us import Simulation

        _simulation = Simulation
    return _simulation


def compute_mtr(
    income: float,
    state_code: str = "CA",
    filing_status: str = "SINGLE",
    year: int = 2024,
) -> float:
    """Compute marginal tax rate for a given income level.

    Uses PolicyEngine US to calculate the combined federal and state
    marginal tax rate on employment income.

    Args:
        income: Annual employment income in USD
        state_code: Two-letter state code (default: CA)
        filing_status: Filing status (SINGLE, JOINT, etc.)
        year: Tax year

    Returns:
        Marginal tax rate as a decimal (e.g., 0.32 for 32%)
    """
    Simulation = _get_simulation()

    # Create situation with the given income
    situation = {
        "people": {
            "person": {
                "age": {year: 40},
                "employment_income": {year: income},
            }
        },
        "tax_units": {
            "tax_unit": {
                "members": ["person"],
                "filing_status": {year: filing_status},
            }
        },
        "spm_units": {
            "spm_unit": {
                "members": ["person"],
            }
        },
        "households": {
            "household": {
                "members": ["person"],
                "state_code": {year: state_code},
            }
        },
    }

    sim = Simulation(situation=situation)

    # Get MTR on employment income
    # This includes federal income tax, state income tax, and payroll taxes
    mtr = sim.calculate("marginal_tax_rate", year)

    # Return as scalar
    return float(mtr[0]) if hasattr(mtr, "__len__") else float(mtr)


def compute_mtrs_for_incomes(
    incomes: List[float],
    state_code: str = "CA",
    filing_status: str = "SINGLE",
    year: int = 2024,
) -> np.ndarray:
    """Compute MTRs for multiple income levels.

    Args:
        incomes: List of annual incomes
        state_code: Two-letter state code
        filing_status: Filing status
        year: Tax year

    Returns:
        Array of marginal tax rates
    """
    mtrs = np.array(
        [compute_mtr(inc, state_code, filing_status, year) for inc in incomes]
    )
    return mtrs


def create_agents_with_mtrs(
    wages: List[float],
    annual_hours: float = DEFAULT_PARAMS.max_hours,
    state_code: str = "CA",
    filing_status: str = "SINGLE",
    year: int = 2024,
    labor_disutility: float = DEFAULT_PARAMS.labor_disutility,
    speeding_utility: float = DEFAULT_PARAMS.speeding_utility,
    vsl: float = DEFAULT_PARAMS.vsl,
) -> List[Agent]:
    """Create agents with MTRs computed from PolicyEngine US.

    Each agent's MTR is computed based on their expected annual income
    (wage * annual_hours).

    Args:
        wages: List of hourly wage rates
        annual_hours: Hours used to compute expected income for MTR
        state_code: Two-letter state code for tax calculation
        filing_status: Tax filing status
        year: Tax year
        labor_disutility: Labor disutility parameter
        speeding_utility: Speeding utility parameter
        vsl: Value of statistical life

    Returns:
        List of Agent objects with MTRs set
    """
    # Compute expected incomes
    incomes = [wage * annual_hours for wage in wages]

    # Get MTRs for all income levels
    mtrs = compute_mtrs_for_incomes(incomes, state_code, filing_status, year)

    # Create agents with MTRs
    agents = []
    for wage, mtr in zip(wages, mtrs):
        agent = Agent(
            wage=wage,
            labor_disutility=labor_disutility,
            speeding_utility=speeding_utility,
            vsl=vsl,
            mtr=mtr,
        )
        agents.append(agent)

    return agents


def get_income_mtr_schedule(
    min_income: float = 0,
    max_income: float = 500000,
    n_points: int = 50,
    state_code: str = "CA",
    filing_status: str = "SINGLE",
    year: int = 2024,
) -> tuple[np.ndarray, np.ndarray]:
    """Generate income-MTR schedule for visualization.

    Args:
        min_income: Minimum income
        max_income: Maximum income
        n_points: Number of points
        state_code: State code
        filing_status: Filing status
        year: Tax year

    Returns:
        Tuple of (incomes array, mtrs array)
    """
    incomes = np.linspace(min_income, max_income, n_points)
    mtrs = compute_mtrs_for_incomes(incomes.tolist(), state_code, filing_status, year)
    return incomes, mtrs
