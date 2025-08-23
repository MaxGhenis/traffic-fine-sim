"""Default parameters for simulations."""

# Economic parameters
DEFAULT_VSL = 10_000_000  # Value of statistical life
DEFAULT_MEAN_INCOME = 60_000  # Mean annual income
DEFAULT_SD_INCOME = 30_000  # Standard deviation of income
DEFAULT_TAX_RATE = 0.3  # Default marginal tax rate

# Utility function parameters
DEFAULT_INCOME_UTILITY_FACTOR = 1.0  # Weight on log income utility
DEFAULT_LABOR_DISUTILITY_FACTOR = 0.5  # Weight on quadratic labor disutility
DEFAULT_SPEEDING_UTILITY_FACTOR = 0.1  # Weight on log speeding utility

# Simulation parameters
DEFAULT_NUM_AGENTS = 1000  # Number of agents in simulation
DEFAULT_NUM_ITERATIONS = 100  # Maximum iterations for convergence
DEFAULT_DEATH_PROB_FACTOR = 0.0001  # Factor converting speeding to death probability
DEFAULT_CONVERGENCE_THRESHOLD = 0.01  # Convergence threshold for utility

# Labor parameters
WORK_HOURS_PER_YEAR = 2080  # Standard full-time work hours (52 weeks * 40 hours)
