"""Default parameters for simulations - calibrated to Finnish day-fine system."""

# Economic parameters (calibrated to Finland)
DEFAULT_VSL = 3_600_000  # EU recommended VSL for Finland (EUR)
DEFAULT_MEAN_INCOME = 42_000  # Finnish median annual income (EUR)
DEFAULT_SD_INCOME = 18_000  # Calibrated to Finnish Gini coefficient of 0.27
DEFAULT_TAX_RATE = 0.4  # Finnish average marginal tax rate

# Utility function parameters (calibrated to empirical elasticities)
DEFAULT_INCOME_UTILITY_FACTOR = 1.0  # Weight on log income utility
DEFAULT_LABOR_DISUTILITY_FACTOR = 0.4  # Calibrated for labor elasticity of 0.25
DEFAULT_SPEEDING_UTILITY_FACTOR = 0.08  # Calibrated for speeding elasticity of -0.075

# Simulation parameters
DEFAULT_NUM_AGENTS = 1000  # Number of agents in simulation
DEFAULT_NUM_ITERATIONS = 100  # Maximum iterations for convergence
DEFAULT_DEATH_PROB_FACTOR = 0.0001  # Factor converting speeding to death probability
DEFAULT_CONVERGENCE_THRESHOLD = 0.01  # Convergence threshold for utility

# Labor parameters
WORK_HOURS_PER_YEAR = 2080  # Standard full-time work hours (52 weeks * 40 hours)

# Fine parameters (Finnish day-fine system)
DEFAULT_FLAT_FINE = 200  # Finnish minimum for motor vehicles (EUR)
DEFAULT_INCOME_FINE_BASE = 200  # Finnish minimum base amount (EUR)
DEFAULT_INCOME_FINE_FACTOR = 0.0167  # Finnish formula: 1/60 of monthly income
FINNISH_BASIC_DEDUCTION = 3060  # Annual basic living allowance (255 EUR/month)
