import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from model import Agent
from utils import (
    DEFAULT_MEAN_INCOME,
    DEFAULT_TAX_RATE,
    DEFAULT_VSL,
    DEFAULT_DEATH_PROB_FACTOR,
    DEFAULT_INCOME_UTILITY_FACTOR,
    DEFAULT_LABOR_DISUTILITY_FACTOR,
    DEFAULT_SPEEDING_UTILITY_FACTOR,
    WORK_HOURS_PER_YEAR,
)


class UtilityExplorer(Agent):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def explore(self):
        st.title("Utility Function Explorer")

        # Input parameters
        income = st.slider(
            "Income", 0, int(DEFAULT_MEAN_INCOME * 4), DEFAULT_MEAN_INCOME
        )
        labor_supply = st.slider(
            "Labor Supply (hours)",
            0,
            WORK_HOURS_PER_YEAR,
            WORK_HOURS_PER_YEAR // 2,
        )
        speeding = st.slider("Speeding", 0.0, 1.0, 0.1)
        fine_rate = st.slider("Fine Rate", 0, 10000, 100)
        tax_rate = st.slider("Tax Rate", 0.0, 1.0, DEFAULT_TAX_RATE)
        death_prob_factor = st.slider(
            "Death Probability Factor",
            DEFAULT_DEATH_PROB_FACTOR / 10,
            DEFAULT_DEATH_PROB_FACTOR * 10,
            DEFAULT_DEATH_PROB_FACTOR,
            format="%.7f",
        )
        vsl = st.slider(
            "Value of Statistical Life",
            int(DEFAULT_VSL / 10),
            int(DEFAULT_VSL * 10),
            DEFAULT_VSL,
        )

        # Update agent parameters
        self.potential_income = income
        self.wage_rate = self.potential_income / WORK_HOURS_PER_YEAR
        self.income_utility_factor = st.slider(
            "Income Utility Factor", 0.1, 5.0, DEFAULT_INCOME_UTILITY_FACTOR
        )
        self.labor_disutility_factor = st.slider(
            "Labor Disutility Factor",
            DEFAULT_LABOR_DISUTILITY_FACTOR / 10,
            DEFAULT_LABOR_DISUTILITY_FACTOR * 10,
            DEFAULT_LABOR_DISUTILITY_FACTOR,
            format="%.7f",
        )
        self.speeding_utility_factor = st.slider(
            "Speeding Utility Factor",
            0.1,
            5.0,
            DEFAULT_SPEEDING_UTILITY_FACTOR,
        )

        # Calculate utility
        death_prob = death_prob_factor * speeding
        utility = self.calculate_utility(
            labor_supply,
            speeding,
            lambda x: fine_rate,
            death_prob,
            0,
            tax_rate,
            vsl,
        )

        st.write(f"Total Utility: {utility:.2f}")

        # Plot utility components
        self.plot_utility_components(
            labor_supply, speeding, fine_rate, tax_rate, death_prob, vsl
        )

        # Explore labor supply vs utility
        self.plot_labor_supply_vs_utility(
            tax_rate, fine_rate, speeding, death_prob, vsl
        )

    def plot_utility_components(
        self, labor_supply, speeding, fine_rate, tax_rate, death_prob, vsl
    ):
        gross_income = self.wage_rate * labor_supply
        fine = min(fine_rate * speeding, 0.5 * gross_income)
        tax = gross_income * tax_rate
        net_income = gross_income - fine - tax

        labor_disutility = (
            self.labor_disutility_factor
            * (labor_supply**2)
            / (2 * WORK_HOURS_PER_YEAR)
        )
        speeding_utility = self.speeding_utility_factor * np.log(1 + speeding)
        death_disutility = death_prob * vsl
        income_utility = self.income_utility_factor * np.log(1 + net_income)

        fig, ax = plt.subplots()
        components = [
            ("Labor Disutility", -labor_disutility),
            ("Speeding Utility", speeding_utility),
            ("Death Disutility", -death_disutility),
            ("Income Utility", income_utility),
        ]

        labels, values = zip(*components)
        ax.bar(labels, values)
        ax.set_ylabel("Utility")
        ax.set_title("Utility Components")
        plt.xticks(rotation=45, ha="right")
        st.pyplot(fig)

    def plot_labor_supply_vs_utility(
        self, tax_rate, fine_rate, speeding, death_prob, vsl
    ):
        labor_range = np.linspace(0, WORK_HOURS_PER_YEAR, 100)
        labor_utilities = [
            self.calculate_utility(
                l, speeding, lambda x: fine_rate, death_prob, 0, tax_rate, vsl
            )
            for l in labor_range
        ]

        fig, ax = plt.subplots()
        ax.plot(labor_range / WORK_HOURS_PER_YEAR, labor_utilities)
        ax.set_xlabel("Labor Supply (fraction of total work hours)")
        ax.set_ylabel("Utility")
        ax.set_title("Labor Supply vs Utility")
        st.pyplot(fig)


def utility_explorer():
    explorer = UtilityExplorer(
        DEFAULT_MEAN_INCOME,
        DEFAULT_INCOME_UTILITY_FACTOR,
        DEFAULT_LABOR_DISUTILITY_FACTOR,
        DEFAULT_SPEEDING_UTILITY_FACTOR,
    )
    explorer.explore()
