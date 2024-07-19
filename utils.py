import numpy as np


def generate_incomes(num_agents, mean, std):
    return np.random.lognormal(
        mean=np.log(mean), sigma=np.log(std / mean + 1), size=num_agents
    )
