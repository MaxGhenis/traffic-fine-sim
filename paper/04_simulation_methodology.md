# Simulation Methodology

This section describes the computational approach used to implement and analyze our theoretical model.

## Agent-Based Simulation Framework

We implement an agent-based simulation where heterogeneous individuals optimize their labor supply and speeding decisions. The simulation proceeds through the following steps:

1. **Initialization**: Generate N agents with incomes drawn from a log-normal distribution
2. **Individual Optimization**: Each agent solves their utility maximization problem
3. **Aggregate Outcomes**: Calculate society-wide death probability and total revenues
4. **Redistribution**: Compute universal basic income from collected fines and taxes
5. **Iteration**: Repeat until convergence or maximum iterations reached

## Parameter Calibration

### Baseline Parameters
- Number of agents: 1,000
- Income distribution: Log-normal(μ=60,000, σ=30,000)
- Value of statistical life: $10 million (EPA standard)
- Death probability factor: 0.0001
- Initial tax rate: 30%

### Utility Function Parameters
- Income utility factor: 1.0
- Labor disutility factor: 0.5
- Speeding utility factor: 0.1

These values are calibrated to match observed labor supply elasticities and speeding behavior in the United States.

## Optimization Algorithm

We use scipy's L-BFGS-B algorithm for both:
1. Individual agent optimization (labor and speeding choices)
2. Social planner optimization (fine parameters and tax rates)

The bounded optimization ensures:
- Labor hours ∈ [0, 2080]
- Speeding intensity ∈ [0, 1]
- Tax rate ∈ [0, 0.9]
- Fine amounts ≥ 0

## Convergence Criteria

The simulation converges when:
- Change in total utility < 0.01 between iterations
- Or maximum 100 iterations reached

## Computational Implementation

The simulation is implemented in Python using:
- NumPy for numerical computations
- SciPy for optimization
- Pandas for data management
- Matplotlib/Seaborn for visualization

Code is structured using object-oriented programming with separate classes for agents, society, and fine structures, enabling modular testing and extension.