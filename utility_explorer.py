import streamlit as st
import numpy as np
import matplotlib.pyplot as plt


def utility_explorer():
    st.title("Utility Function Explorer")

    # Input parameters
    income = st.slider("Income", 0, 200000, 50000)
    labor_supply = st.slider("Labor Supply", 0.0, 1.0, 0.5)
    speeding = st.slider("Speeding", 0.0, 1.0, 0.1)
    fine_rate = st.slider("Fine Rate", 0, 10000, 100)
    tax_rate = st.slider("Tax Rate", 0.0, 1.0, 0.3)
    death_prob_factor = st.slider(
        "Death Probability Factor", 0.00001, 0.0001, 0.00005, format="%.5f"
    )
    income_utility_factor = st.slider("Income Utility Factor", 0.1, 5.0, 2.0)
    labor_disutility_factor = st.slider(
        "Labor Disutility Factor", 0.1, 10.0, 3.0
    )
    speeding_utility_factor = st.slider(
        "Speeding Utility Factor", 0.1, 5.0, 1.0
    )
    vsl = st.slider("Value of Statistical Life", 1000000, 20000000, 10000000)

    # Calculate utility
    gross_income = max(income * labor_supply, 1000)
    fine = min(fine_rate * speeding, 0.5 * gross_income)
    tax = gross_income * tax_rate
    net_income = gross_income - fine - tax
    death_prob = death_prob_factor * speeding

    utility = (
        -labor_disutility_factor * labor_supply**2
        + speeding_utility_factor * np.log(1 + speeding)
        - death_prob * vsl
        + income_utility_factor * np.log(1 + net_income)
    )

    st.write(f"Total Utility: {utility:.2f}")

    # Plot utility components
    fig, ax = plt.subplots()
    components = [
        ("Labor Disutility", -labor_disutility_factor * labor_supply**2),
        ("Speeding Utility", speeding_utility_factor * np.log(1 + speeding)),
        ("Death Disutility", -death_prob * vsl),
        ("Income Utility", income_utility_factor * np.log(1 + net_income)),
    ]

    labels, values = zip(*components)
    ax.bar(labels, values)
    ax.set_ylabel("Utility")
    ax.set_title("Utility Components")
    plt.xticks(rotation=45, ha="right")
    st.pyplot(fig)

    # Explore labor supply vs utility
    labor_range = np.linspace(0, 1, 100)
    labor_utilities = [
        -labor_disutility_factor * l**2
        + income_utility_factor
        * np.log(1 + max(income * l, 1000) * (1 - tax_rate))
        for l in labor_range
    ]

    fig, ax = plt.subplots()
    ax.plot(labor_range, labor_utilities)
    ax.set_xlabel("Labor Supply")
    ax.set_ylabel("Utility")
    ax.set_title("Labor Supply vs Utility")
    st.pyplot(fig)
