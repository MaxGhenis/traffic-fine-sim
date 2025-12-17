# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Traffic Fine Simulation is a computational framework for analyzing the welfare effects of income-based versus flat traffic fine systems. The package implements an agent-based model where heterogeneous agents optimize their labor supply and speeding decisions under different fine regimes, accounting for the implicit marginal tax rate effects of income-based fines.

## Development Commands

### Installation
```bash
# Install package in development mode with all dependencies
pip install -e .[dev]

# Install just the core requirements
pip install -r requirements.txt
```

### Running the Application
```bash
# Launch interactive Streamlit web app
streamlit run app.py
```

### Testing
```bash
# Run all tests with coverage
pytest tests/ --cov=traffic_fines

# Run specific test file
pytest tests/test_agent.py

# Run specific test
pytest tests/test_agent.py::TestAgent::test_agent_initialization

# Run tests verbosely
pytest tests/ -v
```

### Code Quality
```bash
# Format code with black
black traffic_fines tests

# Check formatting without changes
black --check traffic_fines tests

# Lint with flake8
flake8 traffic_fines tests --count --select=E9,F63,F7,F82 --show-source --statistics
```

### Building Documentation
```bash
# Build Jupyter Book documentation from paper/ directory
cd paper
jupyter-book build .
```

## Architecture

### Package Structure

The project is organized as a proper Python package:

```
traffic_fines/
├── core/          # Core simulation logic
│   ├── agent.py        # Agent class with utility optimization
│   ├── society.py      # Society simulation with equilibrium dynamics
│   ├── fines.py        # Fine structure implementations (flat, income-based, progressive)
│   ├── optimizer.py    # Welfare optimization for fine parameters
│   └── counterfactual.py  # Counterfactual analysis tools
└── utils/         # Utility functions and parameters
    ├── parameters.py        # Default calibrated parameters (Finnish system)
    ├── income_generation.py # Income distribution generators
    └── analysis.py          # Analysis tools (e.g., Gini calculation)
```

### Core Components

**Agent (`traffic_fines/core/agent.py`):**
- Represents economic agents optimizing labor supply (0-2080 hours/year) and speeding (0-1)
- Utility function includes: log income utility, quadratic labor disutility, log speeding utility, VSL-weighted death cost
- Uses scipy's L-BFGS-B optimizer to solve individual maximization problem
- Calculates effective marginal tax rates including fine structure effects

**Society (`traffic_fines/core/society.py`):**
- Simulates equilibrium with multiple agents
- Iterative process: agents optimize → update death probability from aggregate speeding → redistribute fines/taxes as UBI → repeat until convergence
- Analyzes outcomes by income groups (bottom 20%, middle 60%, top 20%)
- Calculates welfare metrics including Gini coefficient and deadweight loss

**Fine Structures (`traffic_fines/core/fines.py`):**
- `FineStructure`: Abstract base class defining interface
- `FlatFine`: Fixed fine amount (marginal rate = 0)
- `IncomeBasedFine`: Linear in income (base + factor × income)
- `ProgressiveFine`: Bracket-based progressive system

**Optimizer (`traffic_fines/core/optimizer.py`):**
- `WelfareOptimizer`: Finds welfare-maximizing fine and tax parameters
- Uses scipy's minimize to maximize total social utility
- Supports comparison between different fine structures
- Tracks optimization history for analysis

**Streamlit App (`app.py`):**
- Interactive web interface for running simulations
- Configurable parameters: population, income distribution, utility weights, VSL, tax rates
- Visualizations: optimization convergence, income group analysis, welfare comparisons
- Educational tool with policy insights

### Key Simulation Flow

1. **Income Generation**: Generate heterogeneous agent incomes from specified distribution (lognormal, normal, Pareto, or uniform)

2. **Individual Optimization**: Each agent solves:
   ```
   max_{hours, speeding} U(net_income, hours, speeding, death_prob)
   ```
   subject to budget constraint and bounded choices

3. **Society Equilibrium**: Iterate until convergence:
   - Update death probability = death_prob_factor × avg_speeding
   - Agents optimize given current UBI and death probability
   - Collect fines and taxes, redistribute as UBI
   - Check convergence of total utility

4. **Welfare Optimization**: Social planner chooses fine parameters and tax rate to maximize total utility

### Important Implementation Details

- **Numerical Types**: Uses `numpy.float64` extensively for stability
- **Labor Hours**: 2080 = full-time annual hours (52 weeks × 40 hours)
- **VSL Calibration**: Default 3.6M EUR (EU recommendation for Finland)
- **Utility Parameters**: Calibrated to match empirical labor elasticity (~0.25) and speeding elasticity (~-0.075)
- **Finnish Calibration**: Default parameters match Finnish day-fine system
- **Convergence**: Society simulation stops when utility change < threshold or max iterations reached
- **Optimization Bounds**: Fine amounts [0, 10000], income factors [0, 0.01], tax rates [0, 0.9]

### Testing Strategy

- Unit tests for each component (Agent, Society, Fines)
- Tests verify optimization succeeds and produces sensible results
- Fixtures avoid redundant agent/society creation
- Coverage reporting with pytest-cov

## Common Workflows

### Adding a New Fine Structure

1. Create class inheriting from `FineStructure` in `traffic_fines/core/fines.py`
2. Implement: `calculate_fine()`, `get_marginal_rate()`, `get_parameters()`, `set_parameters()`
3. Add tests in `tests/test_fines.py`
4. Update optimizer bounds in `WelfareOptimizer` if needed

### Modifying Agent Behavior

1. Edit utility function in `Agent.calculate_utility()` in `traffic_fines/core/agent.py`
2. Update optimization bounds in `Agent.optimize()` if adding new choice variables
3. Add corresponding tests in `tests/test_agent.py`
4. Re-calibrate utility parameters if changing functional form

### Running Custom Simulations

Create a script that imports the package:
```python
from traffic_fines.core.agent import Agent
from traffic_fines.core.society import Society
from traffic_fines.core.fines import IncomeBasedFine
from traffic_fines.utils.income_generation import generate_income_distribution

# Generate agents
incomes = generate_income_distribution(1000, mean=50000, sd=20000)
agents = [Agent(inc) for inc in incomes]

# Run simulation
fine_structure = IncomeBasedFine(base_amount=100, income_factor=0.002)
society = Society(agents, fine_structure, tax_rate=0.3)
results = society.simulate()
```
