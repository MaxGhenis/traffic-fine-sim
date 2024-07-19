from scipy import optimize
from model import simulate_society


class ObjectiveFunction:
    def __init__(
        self,
        fine_function,
        incomes,
        tax_rate,
        num_iterations,
        death_prob_factor,
        income_utility_factor,
        labor_disutility_factor,
        speeding_utility_factor,
    ):
        self.fine_function = fine_function
        self.incomes = incomes
        self.tax_rate = tax_rate
        self.num_iterations = num_iterations
        self.death_prob_factor = death_prob_factor
        self.income_utility_factor = income_utility_factor
        self.labor_disutility_factor = labor_disutility_factor
        self.speeding_utility_factor = speeding_utility_factor
        self.optimization_history = []

    def __call__(self, params):
        print(f"Objective function called with params: {params}")

        if len(params) == 2:  # Flat fine
            fine_params = [params[0]]
            tax_rate = params[1]
        elif len(params) == 3:  # Income-based fine
            fine_params = [params[0], params[1]]
            tax_rate = params[2]
        else:
            raise ValueError(f"Unexpected number of parameters: {len(params)}")

        try:
            result = simulate_society(
                self.incomes,
                self.fine_function,
                fine_params,
                tax_rate,
                self.num_iterations,
                self.death_prob_factor,
                self.income_utility_factor,
                self.labor_disutility_factor,
                self.speeding_utility_factor,
            )
            utility = result["total_utility"]
            print(f"Simulation result: {result}")
            self.optimization_history.append((params, utility))
            # We're maximizing utility, so return negative for minimization
            return -utility
        except Exception as e:
            print(f"Error in simulate_society: {e}")
            # Return a large value on error to guide optimization away from problematic params
            return float("inf")


def optimize_fine(
    fine_function,
    initial_params,
    incomes,
    TAX_RATE,
    num_iterations,
    death_prob_factor,
    income_utility_factor,
    labor_disutility_factor,
    speeding_utility_factor,
):
    objective = ObjectiveFunction(
        fine_function,
        incomes,
        TAX_RATE,
        num_iterations,
        death_prob_factor,
        income_utility_factor,
        labor_disutility_factor,
        speeding_utility_factor,
    )

    if len(initial_params) == 2:  # Flat fine and tax rate
        bounds = [(0, 1e6), (0, 1)]  # Fine rate and tax rate bounds
    elif len(initial_params) == 3:  # Income-based fine
        bounds = [
            (0, 1e6),
            (0, 1),
            (0, 1),
        ]  # Base rate, income factor, and tax rate bounds
    else:
        raise ValueError("Initial params length not supported")

    print(f"Initial params: {initial_params}")
    print(f"Optimization bounds: {bounds}")

    result = optimize.minimize(
        objective,
        initial_params,
        method="L-BFGS-B",
        bounds=bounds,
        options={"maxiter": 100, "disp": True},
    )

    return result.x, -result.fun, objective.optimization_history
