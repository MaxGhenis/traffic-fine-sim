import numpy as np

# Income-related constants
DEFAULT_MEAN_INCOME = 70_000
DEFAULT_SD_INCOME = 50_000

# Time-related constants
HOURS_PER_YEAR = 8760
WORK_HOURS_PER_YEAR = 2080

# Simulation constants
DEFAULT_NUM_AGENTS = 100
DEFAULT_NUM_ITERATIONS = 20

# Economic constants
DEFAULT_TAX_RATE = 0.3

# Utility function constants
DEFAULT_VSL = 10_000_000  # Value of Statistical Life
DEFAULT_DEATH_PROB_FACTOR = 0.00001
DEFAULT_INCOME_UTILITY_FACTOR = 2.0
DEFAULT_SPEEDING_UTILITY_FACTOR = 1.0

# Labor supply constants
DEFAULT_LABOR_DISUTILITY_FACTOR = 1 / WORK_HOURS_PER_YEAR


def generate_incomes(num_agents, mean, std):
    return np.random.lognormal(
        mean=np.log(mean), sigma=np.log(std / mean + 1), size=num_agents
    )
