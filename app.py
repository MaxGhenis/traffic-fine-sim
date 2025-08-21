"""
Streamlit application for traffic fine simulation.

This app allows users to explore the welfare effects of different
traffic fine structures (flat vs income-based) with interactive parameters.
"""

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Dict, Any

from traffic_fines.core.agent import Agent
from traffic_fines.core.society import Society
from traffic_fines.core.fines import FlatFine, IncomeBasedFine
from traffic_fines.core.optimizer import WelfareOptimizer
from traffic_fines.utils.income_generation import generate_income_distribution
from traffic_fines.utils.analysis import calculate_gini
from traffic_fines.utils.parameters import *

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (10, 6)


def plot_optimization_history(flat_history: list, income_history: list):
    """Plot optimization history for both fine structures."""
    fig, axes = plt.subplots(2, 2, figsize=(12, 8))
    
    # Extract data from histories
    flat_utils = [h['utility'] for h in flat_history]
    income_utils = [h['utility'] for h in income_history]
    
    # Plot utility convergence
    ax = axes[0, 0]
    ax.plot(flat_utils, label='Flat Fine', color='blue', alpha=0.7)
    ax.plot(income_utils, label='Income-Based', color='red', alpha=0.7)
    ax.set_xlabel('Optimization Step')
    ax.set_ylabel('Total Utility')
    ax.set_title('Utility Convergence')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    # Plot parameter evolution for flat fine
    ax = axes[0, 1]
    flat_params = [h['params'] for h in flat_history]
    flat_fines = [p[0] for p in flat_params]
    flat_taxes = [p[1] for p in flat_params]
    ax.plot(flat_fines, label='Fine Amount', color='blue')
    ax.plot([t * 1000 for t in flat_taxes], label='Tax Rate (×1000)', color='green')
    ax.set_xlabel('Optimization Step')
    ax.set_ylabel('Parameter Value')
    ax.set_title('Flat Fine Parameters')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    # Plot parameter evolution for income-based fine
    ax = axes[1, 0]
    income_params = [h['params'] for h in income_history]
    base_rates = [p[0] for p in income_params]
    income_factors = [p[1] * 10000 for p in income_params]  # Scale for visibility
    income_taxes = [p[2] * 1000 for p in income_params]
    ax.plot(base_rates, label='Base Rate', color='blue')
    ax.plot(income_factors, label='Income Factor (×10000)', color='red')
    ax.plot(income_taxes, label='Tax Rate (×1000)', color='green')
    ax.set_xlabel('Optimization Step')
    ax.set_ylabel('Parameter Value')
    ax.set_title('Income-Based Fine Parameters')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    # Plot welfare comparison
    ax = axes[1, 1]
    categories = ['Flat Fine', 'Income-Based']
    final_utils = [flat_utils[-1], income_utils[-1]]
    colors = ['blue', 'red']
    bars = ax.bar(categories, final_utils, color=colors, alpha=0.7)
    ax.set_ylabel('Final Total Utility')
    ax.set_title('Welfare Comparison')
    
    # Add value labels on bars
    for bar, value in zip(bars, final_utils):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{value:.0f}', ha='center', va='bottom')
    
    plt.tight_layout()
    return fig


def plot_income_group_analysis(results: Dict[str, Any], title: str):
    """Plot analysis by income group."""
    fig, axes = plt.subplots(2, 2, figsize=(12, 8))
    
    groups = results['income_groups']
    group_names = list(groups.keys())
    
    # Plot labor supply by group
    ax = axes[0, 0]
    labor_values = [groups[g]['avg_labor'] / WORK_HOURS_PER_YEAR for g in group_names]
    ax.bar(group_names, labor_values, color='steelblue', alpha=0.7)
    ax.set_ylabel('Average Labor Supply')
    ax.set_title(f'{title}: Labor Supply by Income Group')
    ax.set_ylim(0, 1)
    
    # Plot speeding by group
    ax = axes[0, 1]
    speeding_values = [groups[g]['avg_speeding'] for g in group_names]
    ax.bar(group_names, speeding_values, color='coral', alpha=0.7)
    ax.set_ylabel('Average Speeding')
    ax.set_title(f'{title}: Speeding by Income Group')
    ax.set_ylim(0, 1)
    
    # Plot effective MTR by group
    ax = axes[1, 0]
    mtr_values = [groups[g]['avg_effective_mtr'] for g in group_names]
    ax.bar(group_names, mtr_values, color='green', alpha=0.7)
    ax.set_ylabel('Effective MTR')
    ax.set_title(f'{title}: Effective Marginal Tax Rate by Income Group')
    
    # Plot utility by group
    ax = axes[1, 1]
    utility_values = [groups[g]['avg_utility'] for g in group_names]
    ax.bar(group_names, utility_values, color='purple', alpha=0.7)
    ax.set_ylabel('Average Utility')
    ax.set_title(f'{title}: Utility by Income Group')
    
    plt.tight_layout()
    return fig


def main():
    """Main Streamlit application."""
    st.set_page_config(
        page_title="Traffic Fine Simulation",
        page_icon="🚗",
        layout="wide"
    )
    
    st.title("🚗 Traffic Fine Simulation: Welfare Effects of Income-Based Penalties")
    
    st.markdown("""
    This simulation explores the welfare implications of income-based traffic fines,
    with particular attention to their effects as implicit marginal tax rates on labor supply.
    """)
    
    # Sidebar parameters
    st.sidebar.header("📊 Simulation Parameters")
    
    with st.sidebar.expander("Population Settings", expanded=True):
        num_agents = st.slider(
            "Number of Agents",
            min_value=10,
            max_value=5000,
            value=DEFAULT_NUM_AGENTS,
            step=10
        )
        
        income_dist = st.selectbox(
            "Income Distribution",
            ["lognormal", "normal", "pareto", "uniform"]
        )
        
        mean_income = st.number_input(
            "Mean Income ($)",
            min_value=10000,
            max_value=200000,
            value=DEFAULT_MEAN_INCOME,
            step=5000
        )
        
        sd_income = st.number_input(
            "Income Std Dev ($)",
            min_value=5000,
            max_value=100000,
            value=DEFAULT_SD_INCOME,
            step=5000
        )
    
    with st.sidebar.expander("Economic Parameters"):
        vsl = st.number_input(
            "Value of Statistical Life ($)",
            min_value=1000000,
            max_value=50000000,
            value=DEFAULT_VSL,
            step=1000000,
            format="%d"
        )
        
        death_prob_factor = st.number_input(
            "Death Probability Factor",
            min_value=0.00001,
            max_value=0.001,
            value=DEFAULT_DEATH_PROB_FACTOR,
            format="%.6f"
        )
        
        initial_tax_rate = st.slider(
            "Initial Tax Rate",
            min_value=0.0,
            max_value=0.7,
            value=DEFAULT_TAX_RATE,
            step=0.05
        )
    
    with st.sidebar.expander("Utility Parameters"):
        income_utility_factor = st.number_input(
            "Income Utility Weight",
            min_value=0.1,
            max_value=5.0,
            value=DEFAULT_INCOME_UTILITY_FACTOR,
            step=0.1
        )
        
        labor_disutility_factor = st.number_input(
            "Labor Disutility Weight",
            min_value=0.1,
            max_value=2.0,
            value=DEFAULT_LABOR_DISUTILITY_FACTOR,
            step=0.1
        )
        
        speeding_utility_factor = st.number_input(
            "Speeding Utility Weight",
            min_value=0.01,
            max_value=1.0,
            value=DEFAULT_SPEEDING_UTILITY_FACTOR,
            step=0.01
        )
    
    with st.sidebar.expander("Simulation Settings"):
        max_iterations = st.slider(
            "Max Iterations",
            min_value=10,
            max_value=200,
            value=DEFAULT_NUM_ITERATIONS,
            step=10
        )
        
        random_seed = st.number_input(
            "Random Seed (for reproducibility)",
            min_value=0,
            max_value=9999,
            value=42
        )
    
    # Run simulation button
    if st.sidebar.button("🚀 Run Simulation", type="primary"):
        with st.spinner("Generating income distribution..."):
            incomes = generate_income_distribution(
                num_agents, mean_income, sd_income, 
                distribution=income_dist, seed=random_seed
            )
        
        # Display income distribution
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Income Distribution")
            fig, ax = plt.subplots(figsize=(8, 4))
            ax.hist(incomes, bins=30, alpha=0.7, color='steelblue', edgecolor='black')
            ax.axvline(np.mean(incomes), color='red', linestyle='--', label=f'Mean: ${np.mean(incomes):,.0f}')
            ax.axvline(np.median(incomes), color='green', linestyle='--', label=f'Median: ${np.median(incomes):,.0f}')
            ax.set_xlabel('Income ($)')
            ax.set_ylabel('Number of Agents')
            ax.set_title('Agent Income Distribution')
            ax.legend()
            st.pyplot(fig)
        
        with col2:
            st.subheader("Distribution Statistics")
            stats_df = pd.DataFrame({
                'Statistic': ['Mean', 'Median', 'Std Dev', 'Min', 'Max', 'Gini'],
                'Value': [
                    f"${np.mean(incomes):,.0f}",
                    f"${np.median(incomes):,.0f}",
                    f"${np.std(incomes):,.0f}",
                    f"${np.min(incomes):,.0f}",
                    f"${np.max(incomes):,.0f}",
                    f"{calculate_gini(incomes):.3f}"
                ]
            })
            st.dataframe(stats_df, hide_index=True)
        
        # Run optimizations
        st.header("🔍 Optimization Results")
        
        # Compare fine structures
        optimizer = WelfareOptimizer(
            incomes,
            FlatFine,  # Will be used for comparison
            vsl,
            death_prob_factor,
            income_utility_factor,
            labor_disutility_factor,
            speeding_utility_factor,
            max_iterations
        )
        
        with st.spinner("Optimizing fine structures..."):
            comparison = optimizer.compare_fine_structures(initial_tax_rate)
        
        # Display results
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📊 Flat Fine System")
            flat_results = comparison['flat']
            st.metric("Optimal Fine Amount", f"${flat_results['fine_amount']:.2f}")
            st.metric("Optimal Tax Rate", f"{flat_results['tax_rate']:.2%}")
            st.metric("Total Welfare", f"{flat_results['utility']:.0f}")
        
        with col2:
            st.subheader("📈 Income-Based Fine System")
            income_results = comparison['income_based']
            st.metric("Base Fine Amount", f"${income_results['base_amount']:.2f}")
            st.metric("Income Factor", f"{income_results['income_factor']:.4f}")
            st.metric("Optimal Tax Rate", f"{income_results['tax_rate']:.2%}")
            st.metric("Total Welfare", f"{income_results['utility']:.0f}")
        
        # Welfare comparison
        st.header("📊 Welfare Comparison")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            welfare_diff = comparison['welfare_difference']
            st.metric(
                "Welfare Difference",
                f"{abs(welfare_diff):.0f}",
                delta=f"{'↑' if welfare_diff > 0 else '↓'} Income-based {'better' if welfare_diff > 0 else 'worse'}"
            )
        
        with col2:
            pct_change = comparison['welfare_pct_change']
            st.metric(
                "Percentage Change",
                f"{abs(pct_change):.2f}%",
                delta=f"{'↑' if pct_change > 0 else '↓'}"
            )
        
        with col3:
            st.metric(
                "Policy Recommendation",
                "Income-Based" if welfare_diff > 0 else "Flat Fine",
                delta=f"Welfare gain: {abs(welfare_diff):.0f}" if welfare_diff > 0 else f"Welfare loss: {abs(welfare_diff):.0f}"
            )
        
        # Optimization history plot
        st.header("📈 Optimization History")
        fig = plot_optimization_history(
            comparison['flat']['history'],
            comparison['income_based']['history']
        )
        st.pyplot(fig)
        
        # Run detailed simulations for income group analysis
        st.header("👥 Income Group Analysis")
        
        with st.spinner("Running detailed simulations..."):
            # Flat fine simulation
            agents_flat = [Agent(inc, income_utility_factor, labor_disutility_factor, speeding_utility_factor) 
                          for inc in incomes]
            flat_fine = FlatFine(flat_results['fine_amount'])
            society_flat = Society(agents_flat, flat_fine, flat_results['tax_rate'], death_prob_factor, vsl)
            results_flat = society_flat.simulate(max_iterations)
            
            # Income-based fine simulation
            agents_income = [Agent(inc, income_utility_factor, labor_disutility_factor, speeding_utility_factor) 
                            for inc in incomes]
            income_fine = IncomeBasedFine(income_results['base_amount'], income_results['income_factor'])
            society_income = Society(agents_income, income_fine, income_results['tax_rate'], death_prob_factor, vsl)
            results_income = society_income.simulate(max_iterations)
        
        # Display income group analysis
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Flat Fine System")
            fig = plot_income_group_analysis(results_flat, "Flat Fine")
            st.pyplot(fig)
        
        with col2:
            st.subheader("Income-Based Fine System")
            fig = plot_income_group_analysis(results_income, "Income-Based")
            st.pyplot(fig)
        
        # Key insights
        st.header("🔍 Key Insights")
        
        insights = []
        
        # Labor supply distortion
        if 'top_20' in results_income['income_groups'] and 'top_20' in results_flat['income_groups']:
            labor_diff = (results_income['income_groups']['top_20']['avg_labor'] - 
                         results_flat['income_groups']['top_20']['avg_labor'])
            if abs(labor_diff) > 10:  # Significant difference
                insights.append(f"• High-income earners work {abs(labor_diff):.0f} hours {'less' if labor_diff < 0 else 'more'} under income-based fines")
        
        # Speeding behavior
        speeding_diff = results_income['avg_speeding'] - results_flat['avg_speeding']
        if abs(speeding_diff) > 0.05:
            insights.append(f"• Average speeding is {abs(speeding_diff*100):.1f}% {'lower' if speeding_diff < 0 else 'higher'} with income-based fines")
        
        # Effective MTR impact
        if 'top_20' in results_income['income_groups']:
            mtr_income = results_income['income_groups']['top_20']['avg_effective_mtr']
            if mtr_income > 0.4:
                insights.append(f"• High earners face effective MTR of {mtr_income:.1%} with income-based fines")
        
        # Welfare distribution
        welfare_metrics_flat = society_flat.calculate_welfare_metrics()
        welfare_metrics_income = society_income.calculate_welfare_metrics()
        gini_diff = welfare_metrics_income['utility_gini'] - welfare_metrics_flat['utility_gini']
        if abs(gini_diff) > 0.02:
            insights.append(f"• Utility inequality (Gini) is {abs(gini_diff):.3f} {'lower' if gini_diff < 0 else 'higher'} with income-based fines")
        
        # Deadweight loss
        dwl_diff = welfare_metrics_income['deadweight_loss'] - welfare_metrics_flat['deadweight_loss']
        if abs(dwl_diff) > 100:
            insights.append(f"• Deadweight loss is ${abs(dwl_diff):.0f} {'lower' if dwl_diff < 0 else 'higher'} with income-based fines")
        
        if insights:
            for insight in insights:
                st.write(insight)
        else:
            st.write("No significant differences detected between the two systems.")
    
    # Information section
    with st.expander("ℹ️ About This Simulation"):
        st.markdown("""
        ### Model Overview
        
        This simulation models a society where agents make joint decisions about:
        1. **Labor Supply**: How many hours to work (0-2080 per year)
        2. **Speeding Behavior**: How much to speed (0-1 intensity scale)
        
        ### Key Mechanisms
        
        **Income-Based Fines as Implicit Taxes:**
        - Income-based fines create an additional marginal tax rate on speeders
        - This distorts labor supply decisions, particularly for high earners
        - The model captures this "double distortion" effect
        
        **Dynamic Equilibrium:**
        - Death probability depends on aggregate speeding behavior
        - Fines and taxes are redistributed as Universal Basic Income
        - Society iterates until reaching equilibrium
        
        **Welfare Optimization:**
        - The social planner chooses fine parameters and tax rates
        - Goal is to maximize total social utility
        - Must balance deterrence benefits against labor supply distortions
        
        ### Policy Implications
        
        While income-based fines may seem fairer (equal burden across income levels),
        they introduce labor supply distortions that flat fines avoid. The optimal
        policy depends on the relative magnitudes of:
        - Fairness gains from proportional penalties
        - Efficiency losses from additional labor market distortions
        - Behavioral responses across the income distribution
        """)


if __name__ == "__main__":
    main()