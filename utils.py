import numpy as np


def generate_incomes(num_agents, mean, std):
    return np.random.lognormal(mean=mean, sigma=std, size=num_agents)
