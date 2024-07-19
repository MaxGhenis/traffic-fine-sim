import numpy as np
from scipy import optimize

from utils import WORK_HOURS_PER_YEAR, DEFAULT_LABOR_DISUTILITY_FACTOR


class Agent:
    def __init__(
        self,
        potential_income,
        income_utility_factor,
        labor_disutility_factor,
        speeding_utility_factor,
    ):
        self.potential_income = np.float64(potential_income)
        self.wage_rate = self.potential_income / WORK_HOURS_PER_YEAR
        self.labor_supply = 0.0  # In hours
        self.speeding = 0.0
        self.fine = 0.0
        self.income_utility_factor = income_utility_factor
        self.labor_disutility_factor = labor_disutility_factor
        self.speeding_utility_factor = speeding_utility_factor

    def calculate_utility(
        self,
        labor_hours,
        speeding,
        fine_function,
        death_prob,
        ubi,
        tax_rate,
        vsl,
    ):
        gross_income = self.wage_rate * labor_hours
        fine = fine_function(gross_income) * speeding
        tax = gross_income * tax_rate
        net_income = gross_income - fine - tax + ubi

        # Simplified labor disutility calculation
        labor_disutility = (
            self.labor_disutility_factor
            * (labor_hours**2)
            / (2 * WORK_HOURS_PER_YEAR)
        )

        utility = (
            -labor_disutility
            + self.speeding_utility_factor * np.log(1 + speeding)
            - death_prob * speeding * vsl
            + self.income_utility_factor * np.log(1 + net_income)
        )
        return np.float64(utility)

    def optimize(self, fine_function, death_prob, ubi, tax_rate, vsl):
        def objective(x):
            labor_hours, speeding = x
            return -self.calculate_utility(
                labor_hours,
                speeding,
                fine_function,
                death_prob,
                ubi,
                tax_rate,
                vsl,
            )

        bounds = [
            (0, 2080),
            (0, 1),
        ]  # Bounds for labor hours (0 to 2080) and speeding (0 to 1)
        result = optimize.minimize(
            objective, [1040, 0.5], method="L-BFGS-B", bounds=bounds
        )

        self.labor_supply, self.speeding = result.x
        self.fine = np.float64(
            fine_function(self.wage_rate * self.labor_supply) * self.speeding
        )
        return -result.fun  # Return the utility


def simulate_society(
    incomes,
    fine_function,
    fine_params,
    tax_rate,
    num_iterations,
    death_prob_factor,
    income_utility_factor,
    labor_disutility_factor,
    speeding_utility_factor,
    vsl,
):
    try:
        agents = [
            Agent(
                income,
                income_utility_factor,
                labor_disutility_factor,
                speeding_utility_factor,
            )
            for income in incomes
        ]
        total_fines = 0.0
        total_tax = 0.0
        total_utility = 0.0

        for iteration in range(num_iterations):
            death_prob = np.float64(
                death_prob_factor
                * sum(a.speeding for a in agents)
                / len(agents)
            )
            ubi = np.float64((total_fines + total_tax) / len(agents))

            for agent in agents:
                utility = agent.optimize(
                    lambda income: fine_function(income, fine_params),
                    death_prob,
                    ubi,
                    tax_rate,
                    vsl,
                )
                agent.labor_supply = np.clip(agent.labor_supply, 0, 1)
                agent.speeding = np.clip(agent.speeding, 0, 1)

            total_fines = np.float64(sum(a.fine for a in agents))
            total_tax = np.float64(
                sum(a.income * a.labor_supply * tax_rate for a in agents)
            )
            total_utility = np.float64(
                sum(
                    agent.calculate_utility(
                        agent.labor_supply,
                        agent.speeding,
                        lambda income: fine_function(income, fine_params),
                        death_prob,
                        ubi,
                        tax_rate,
                        vsl,
                    )
                    for agent in agents
                )
            )

            print(
                f"Iteration {iteration + 1}: Death prob: {death_prob:.6f}, UBI: {ubi:.2f}, Total utility: {total_utility:.2f}"
            )

        return {
            "total_utility": np.float64(total_utility),
            "avg_speeding": np.float64(np.mean([a.speeding for a in agents])),
            "avg_labor": np.float64(np.mean([a.labor_supply for a in agents])),
            "agents": agents,
        }
    except Exception as e:
        print(f"An error occurred during simulation: {str(e)}")
        return None


def flat_fine(income, params):
    rate = params[0]
    return rate


def income_based_fine(income, params):
    base_rate = params[0]
    income_factor = params[1]
    return base_rate + income_factor * income
