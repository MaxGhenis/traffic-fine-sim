import streamlit as st
import pandas as pd
from model import flat_fine, income_based_fine, simulate_society
from optimization import optimize_fine
from visualization import plot_results, analyze_income_groups
from utils import (
    generate_incomes,
    DEFAULT_MEAN_INCOME,
    DEFAULT_SD_INCOME,
    DEFAULT_NUM_AGENTS,
    DEFAULT_DEATH_PROB_FACTOR,
    DEFAULT_VSL,
    DEFAULT_LABOR_DISUTILITY_FACTOR,
    DEFAULT_SPEEDING_UTILITY_FACTOR,
    DEFAULT_INCOME_UTILITY_FACTOR,
    DEFAULT_NUM_ITERATIONS,
    DEFAULT_TAX_RATE,
)
from gather_code import gather_code
from utility_explorer import utility_explorer


def run_simulation(
    fine_function,
    initial_params,
    name,
    incomes,
    tax_rate,
    num_iterations,
    death_prob_factor,
    income_utility_factor,
    labor_disutility_factor,
    speeding_utility_factor,
    vsl,
):
    st.write(f"\nOptimizing {name} fine and tax rate...")
    try:
        optimal_params, utility, history = optimize_fine(
            fine_function,
            initial_params,
            incomes,
            tax_rate,
            num_iterations,
            death_prob_factor,
            income_utility_factor,
            labor_disutility_factor,
            speeding_utility_factor,
            vsl,
        )
    except Exception as e:
        st.write(f"Error in optimization: {e}")
        return None, None, None, None

    if optimal_params is None or utility is None or history is None:
        st.write("Optimization failed.")
        return None, None, None, None

    if fine_function == flat_fine:
        fine_rate, tax_rate = optimal_params
        fine_params = [fine_rate]
    else:  # income_based_fine
        base_rate, income_factor, tax_rate = optimal_params
        fine_params = [base_rate, income_factor]

    result = simulate_society(
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
    )

    if result is None:
        st.write("Simulation failed.")
        return None, None, None, None

    st.write(f"\n{name.capitalize()} Fine Results:")
    if fine_function == flat_fine:
        st.write(f"Optimal fine rate: {fine_rate:.4f}")
    else:
        st.write(f"Optimal base rate: {base_rate:.4f}")
        st.write(f"Optimal income factor: {income_factor:.6f}")
    st.write(f"Optimal tax rate: {tax_rate:.4f}")
    st.write(f"Total utility: {utility:.2f}")
    st.write(f"Average speeding: {result['avg_speeding']:.2f}")
    st.write(f"Average labor supply: {result['avg_labor']:.2f}")

    st.write("\nOptimization Trace:")
    trace_data = []
    for i, (params, util) in enumerate(history):
        if i % 10 == 0:  # Print every 10th step to keep output manageable
            if fine_function == flat_fine:
                trace_data.append((i, params[0], params[1], util))
            else:
                trace_data.append((i, params[0], params[1], params[2], util))

    if fine_function == flat_fine:
        trace_df = pd.DataFrame(
            trace_data, columns=["Step", "Fine Rate", "Tax Rate", "Utility"]
        )
    else:
        trace_df = pd.DataFrame(
            trace_data,
            columns=[
                "Step",
                "Base Rate",
                "Income Factor",
                "Tax Rate",
                "Utility",
            ],
        )

    st.dataframe(trace_df)

    return optimal_params, utility, result, history


def main():
    st.title("Traffic Fine Simulation")

    if st.sidebar.button("Explore Utility Function"):
        utility_explorer()
        return

    st.sidebar.header("Simulation Parameters")
    num_agents = st.sidebar.slider(
        "Number of Agents",
        1,
        int(DEFAULT_NUM_AGENTS * 10),
        DEFAULT_NUM_AGENTS,
    )
    num_iterations = st.sidebar.slider(
        "Number of Iterations",
        1,
        int(DEFAULT_NUM_ITERATIONS * 10),
        DEFAULT_NUM_ITERATIONS,
    )
    initial_tax_rate = st.sidebar.slider(
        "Initial Tax Rate", 0.0, 1.0, DEFAULT_TAX_RATE
    )
    vsl = st.sidebar.number_input(
        "Value of Statistical Life",
        int(DEFAULT_VSL / 10),
        int(DEFAULT_VSL * 10),
        DEFAULT_VSL,
        format="%.2e",
    )
    death_prob_factor = st.sidebar.number_input(
        "Death Probability Factor",
        DEFAULT_DEATH_PROB_FACTOR / 10,
        DEFAULT_DEATH_PROB_FACTOR * 10,
        DEFAULT_DEATH_PROB_FACTOR,
        format="%.6f",
    )
    income_mean = st.sidebar.number_input(
        "Income Distribution Mean",
        int(DEFAULT_MEAN_INCOME / 10),
        int(DEFAULT_MEAN_INCOME * 10),
        DEFAULT_MEAN_INCOME,
    )
    income_std = st.sidebar.number_input(
        "Income Distribution Std Dev",
        int(DEFAULT_SD_INCOME / 10),
        int(DEFAULT_SD_INCOME * 10),
        DEFAULT_SD_INCOME,
    )

    advanced_params = st.sidebar.expander("Advanced Parameters")
    with advanced_params:
        labor_disutility_factor = st.number_input(
            "Labor Disutility Factor",
            DEFAULT_LABOR_DISUTILITY_FACTOR / 10,
            DEFAULT_LABOR_DISUTILITY_FACTOR * 10,
            DEFAULT_LABOR_DISUTILITY_FACTOR,
        )
        speeding_utility_factor = st.number_input(
            "Speeding Utility Factor",
            DEFAULT_SPEEDING_UTILITY_FACTOR / 10,
            DEFAULT_SPEEDING_UTILITY_FACTOR * 10,
            DEFAULT_SPEEDING_UTILITY_FACTOR,
        )
        income_utility_factor = st.number_input(
            "Income Utility Factor",
            DEFAULT_INCOME_UTILITY_FACTOR / 10,
            DEFAULT_INCOME_UTILITY_FACTOR * 10,
            DEFAULT_INCOME_UTILITY_FACTOR,
        )

    if st.sidebar.button("Run Simulation"):
        incomes = generate_incomes(num_agents, income_mean, income_std)

        initial_flat_fine = death_prob_factor * vsl
        st.write(
            f"Initial flat fine based on expected harm: ${initial_flat_fine:.2f}"
        )
        st.write(f"Initial tax rate: {initial_tax_rate:.2f}")

        with st.spinner("Running flat fine simulation..."):
            flat_params, flat_utility, flat_result, flat_history = (
                run_simulation(
                    flat_fine,
                    [initial_flat_fine, initial_tax_rate],
                    "flat",
                    incomes,
                    initial_tax_rate,
                    num_iterations,
                    death_prob_factor,
                    income_utility_factor,
                    labor_disutility_factor,
                    speeding_utility_factor,
                    vsl,
                )
            )

        if flat_params is None:
            st.write("Flat fine simulation failed.")
            return

        with st.spinner("Running income-based fine simulation..."):
            income_params, income_utility, income_result, income_history = (
                run_simulation(
                    income_based_fine,
                    [initial_flat_fine, 0, initial_tax_rate],
                    "income-based",
                    incomes,
                    initial_tax_rate,
                    num_iterations,
                    death_prob_factor,
                    income_utility_factor,
                    labor_disutility_factor,
                    speeding_utility_factor,
                    vsl,
                )
            )

        if income_params is None:
            st.write("Income-based fine simulation failed.")
            return

        plot_results(flat_history, income_history, initial_flat_fine)

        st.write("\nUtility Comparison:")
        utility_difference = income_utility - flat_utility
        st.write(
            f"Income-based fines {'improve' if utility_difference > 0 else 'reduce'} utility by {abs(utility_difference):.2f}"
        )
        st.write(
            f"Percentage change: {(utility_difference / flat_utility) * 100:.2f}%"
        )

        st.write("\nFlat Fine Income Group Analysis:")
        analyze_income_groups(flat_result["agents"])

        st.write("\nIncome-Based Fine Income Group Analysis:")
        analyze_income_groups(income_result["agents"])

    st.sidebar.header("Developer Tools")
    all_code = gather_code()
    with st.sidebar.expander("View All Code"):
        st.code(all_code, language="python", line_numbers=True)


if __name__ == "__main__":
    main()
