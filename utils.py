import numpy as np

DEFAULT_MEAN_INCOME = 70_000
DEFAULT_SD_INCOME = 50_000
DEFAULT_NUM_AGENTS = 100
DEFAULT_DEATH_PROB_FACTOR = 0.00001
DEFAULT_VSL = 10_000_000
DEFAULT_LABOR_DISUTILITY_FACTOR = 3.0
DEFAULT_SPEEDING_UTILITY_FACTOR = 1.0
DEFAULT_INCOME_UTILITY_FACTOR = 2.0
DEFAULT_NUM_ITERATIONS = 20
DEFAULT_TAX_RATE = 0.3


def generate_incomes(num_agents, mean, std):
    return np.random.lognormal(
        mean=np.log(mean), sigma=np.log(std / mean + 1), size=num_agents
    )
