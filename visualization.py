import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns


def plot_optimization_progress(history):
    plt.figure(figsize=(10, 6))
    plt.plot([i for i in range(len(history))], [util for _, util in history])
    plt.title("Optimization Progress")
    plt.xlabel("Iteration")
    plt.ylabel("Utility")
    plt.show()


def plot_agent_distributions(agents):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

    sns.histplot([a.labor_supply for a in agents], ax=ax1, kde=True)
    ax1.set_title("Distribution of Labor Supply")
    ax1.set_xlabel("Labor Supply")

    sns.histplot([a.speeding for a in agents], ax=ax2, kde=True)
    ax2.set_title("Distribution of Speeding")
    ax2.set_xlabel("Speeding")

    plt.tight_layout()
    plt.show()


def plot_results(flat_history, income_history, initial_flat_fine):
    plt.figure(figsize=(15, 6))

    # Flat fines
    plt.subplot(1, 2, 1)
    flat_rates = [params[0] for params, _ in flat_history]
    flat_utilities = [utility for _, utility in flat_history]
    plt.scatter(flat_rates, flat_utilities, alpha=0.5)
    plt.title("Utility vs Flat Fine Rate")
    plt.xlabel("Fine Rate")
    plt.ylabel("Total Utility")
    plt.axvline(
        x=initial_flat_fine, color="r", linestyle="--", label="Initial Fine"
    )
    plt.legend()

    # Income-based fines
    plt.subplot(1, 2, 2)
    base_rates = [params[0] for params, _ in income_history]
    income_factors = [params[1] for params, _ in income_history]
    utilities = [utility for _, utility in income_history]
    plt.scatter(
        base_rates, income_factors, c=utilities, cmap="viridis", alpha=0.5
    )
    plt.colorbar(label="Total Utility")
    plt.title("Utility for Income-Based Fines")
    plt.xlabel("Base Rate")
    plt.ylabel("Income Factor")

    plt.tight_layout()
    plt.show()


def analyze_income_groups(agents):
    agents.sort(key=lambda a: a.income)
    low_income = agents[: len(agents) // 3]
    mid_income = agents[len(agents) // 3 : 2 * len(agents) // 3]
    high_income = agents[2 * len(agents) // 3 :]

    for group, name in [
        (low_income, "Low"),
        (mid_income, "Middle"),
        (high_income, "High"),
    ]:
        print(f"\n{name} income group:")
        avg_income = np.mean([a.income for a in group])
        avg_labor = np.mean([a.labor_supply for a in group])
        print(f"  Average potential income: {avg_income:.2f}")
        print(f"  Average labor supply: {avg_labor:.2f}")
        print(f"  Average actual income: {avg_income * avg_labor:.2f}")
        print(
            f"  Average speeding: {np.mean([a.speeding for a in group]):.2f}"
        )
