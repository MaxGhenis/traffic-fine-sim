# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Traffic Fine Simulation is a computational framework for analyzing the welfare effects of income-based versus flat traffic fine systems. The package implements an agent-based model where heterogeneous agents optimize their labor supply and speeding decisions under different fine regimes, accounting for the implicit marginal tax rate effects of income-based fines.

**Goal**: Academic paper with gold-standard computational replication following best practices for reproducible research.

## Development Commands

### Installation
```bash
# Install package in development mode with all dependencies
pip install -e .[dev]

# Install just the core requirements
pip install -r requirements.txt

# Note: Currently missing locked dependencies (requirements-lock.txt or poetry.lock)
# This is a reproducibility gap that needs addressing
```

### Running the Application
```bash
# Launch interactive Streamlit web app
streamlit run app.py
```

### Testing
```bash
# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/test_agent.py

# Run specific test
pytest tests/test_agent.py::TestAgent::test_agent_initialization

# Run with coverage (requires pytest-cov installed)
pytest tests/ --cov=traffic_fines --cov-report=html
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

# View built book
open _build/html/index.html  # macOS
xdg-open _build/html/index.html  # Linux
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

paper/              # Jupyter Book academic paper
├── _config.yml     # Jupyter Book configuration
├── _toc.yml        # Table of contents
├── *.md            # Paper chapters (markdown)
└── *.ipynb         # Computational notebooks with results

app.py              # Streamlit interactive app
tests/              # Unit tests
```

### Core Components

**Agent (`traffic_fines/core/agent.py`):**
- Represents economic agents optimizing labor supply (0-2080 hours/year) and speeding (0-1)
- Utility function includes: log income utility, quadratic labor disutility, log speeding utility, VSL-weighted death cost
- Uses scipy's L-BFGS-B optimizer to solve individual maximization problem
- Calculates effective marginal tax rates including fine structure effects
- **Key method**: `optimize()` - solves agent's utility maximization problem

**Society (`traffic_fines/core/society.py`):**
- Simulates equilibrium with multiple agents
- Iterative process: agents optimize → update death probability from aggregate speeding → redistribute fines/taxes as UBI → repeat until convergence
- Analyzes outcomes by income groups (bottom 20%, middle 60%, top 20%)
- Calculates welfare metrics including Gini coefficient and deadweight loss
- **Key method**: `simulate()` - runs society to equilibrium
- **Key method**: `calculate_welfare_metrics()` - computes Gini, deadweight loss, efficiency ratio

**Fine Structures (`traffic_fines/core/fines.py`):**
- `FineStructure`: Abstract base class defining interface
- `FlatFine`: Fixed fine amount (marginal rate = 0)
- `IncomeBasedFine`: Linear in income (base + factor × income)
- `ProgressiveFine`: Bracket-based progressive system with income brackets
- All implement: `calculate_fine()`, `get_marginal_rate()`, `get_parameters()`, `set_parameters()`

**Optimizer (`traffic_fines/core/optimizer.py`):**
- `WelfareOptimizer`: Finds welfare-maximizing fine and tax parameters
- Uses scipy's minimize to maximize total social utility
- **Key method**: `compare_fine_structures()` - runs optimization for both flat and income-based fines
- Tracks optimization history for analysis
- Returns optimal parameters and welfare comparison

**Streamlit App (`app.py`):**
- Interactive web interface for running simulations
- Configurable parameters: population, income distribution, utility weights, VSL, tax rates
- Visualizations: optimization convergence, income group analysis, welfare comparisons
- Educational tool with policy insights

**Paper (`paper/`):**
- Jupyter Book format for academic publication
- Combines markdown chapters with computational notebooks (`05_results.ipynb`)
- **Critical**: Notebooks should be executed with deterministic results (seed=42)
- **Critical**: All figures should be generated from code, not manually created

### Key Simulation Flow

1. **Income Generation**: Generate heterogeneous agent incomes from specified distribution (lognormal, normal, Pareto, or uniform)
   - Always use `seed=42` for reproducibility in paper results

2. **Individual Optimization**: Each agent solves:
   ```
   max_{hours, speeding} U(net_income, hours, speeding, death_prob)
   ```
   subject to budget constraint and bounded choices

3. **Society Equilibrium**: Iterate until convergence:
   - Update death probability = death_prob_factor × avg_speeding
   - Agents optimize given current UBI and death probability
   - Collect fines and taxes, redistribute as UBI
   - Check convergence of total utility (threshold = 0.01)

4. **Welfare Optimization**: Social planner chooses fine parameters and tax rate to maximize total utility
   - Uses scipy.optimize.minimize with L-BFGS-B method
   - Searches over bounded parameter space

### Important Implementation Details

**Numerical Stability:**
- Uses `numpy.float64` extensively for numerical stability
- Net income clamped to `max(net_income, 1e-10)` to avoid log(0)
- Optimization uses L-BFGS-B with fallback to Nelder-Mead if it fails

**Calibration Values:**
- **Labor Hours**: 2080 = full-time annual hours (52 weeks × 40 hours)
- **VSL**: Default 3.6M EUR (EU recommendation for Finland)
- **Finnish Income**: Mean 42,000 EUR, SD 18,000 EUR (Gini ≈ 0.27)
- **Finnish Tax Rate**: 0.4 (40% average marginal rate)
- **Labor Elasticity**: ~0.25 (achieved with labor_disutility_factor=0.4)
- **Speeding Elasticity**: ~-0.075 (achieved with speeding_utility_factor=0.08)

**Optimization Bounds:**
- Fine amounts: [0, 10000]
- Income factors: [0, 0.01]
- Tax rates: [0, 0.9]

**Convergence Criteria:**
- Society simulation: abs(utility_change) < 0.01 or max_iterations (default 100)
- Welfare optimization: default scipy tolerances with maxiter=100

### Testing Strategy

- Unit tests for each component (Agent, Society, Fines)
- Tests verify optimization succeeds and produces sensible results
- Fixtures avoid redundant agent/society creation
- **Gap**: Coverage reporting requires pytest-cov (not currently working)
- **Gap**: No integration tests for full simulation pipeline
- **Gap**: No regression tests for paper results

## Academic Paper Reproducibility

### Current Status
- ✅ Package structure with proper imports
- ✅ Paper structure with Jupyter Book
- ✅ Computational notebook with analysis (`paper/05_results.ipynb`)
- ✅ Calibrated parameters documented
- ⚠️ **Missing**: Locked dependency versions
- ⚠️ **Missing**: Executed notebook outputs in repo (clean notebooks only)
- ⚠️ **Missing**: Cached simulation results
- ⚠️ **Missing**: Pre-commit hooks for code quality
- ⚠️ **Missing**: Citation metadata (CITATION.cff)

### Reproducibility Best Practices

**For Gold Standard Replication:**

1. **Always use deterministic seeds**: `np.random.seed(42)` in all paper results
2. **Cache expensive computations**: Save simulation results to CSV files
3. **Version control figures**: All figures generated from code, committed to `paper/figures/`
4. **Document environment**: Need locked requirements (poetry.lock or requirements-lock.txt)
5. **Execute notebooks with caching**: Use Jupyter Book's execution cache
6. **Never commit manual edits**: All paper content should be reproducible from source

**When modifying simulations for paper:**
```python
# ALWAYS include at top of notebook cells:
np.random.seed(42)  # Deterministic results

# ALWAYS save results:
results.to_csv(f'data/results_{datetime.now().strftime("%Y%m%d")}.csv')

# ALWAYS version figures:
plt.savefig('paper/figures/figure1_labor_supply.pdf', bbox_inches='tight', dpi=300)
```

## Common Workflows

### Adding a New Fine Structure

1. Create class inheriting from `FineStructure` in `traffic_fines/core/fines.py`
2. Implement required methods:
   - `calculate_fine(income)` - returns fine amount
   - `get_marginal_rate(income)` - returns marginal fine rate
   - `get_parameters()` - returns list of parameters
   - `set_parameters(params)` - sets parameters from list
3. Add tests in `tests/test_fines.py`
4. Update optimizer bounds in `WelfareOptimizer.__init__()` or `optimize()` if needed

### Modifying Agent Behavior

1. Edit utility function in `Agent.calculate_utility()` in `traffic_fines/core/agent.py`
2. Update optimization bounds in `Agent.optimize()` if adding new choice variables
3. Add corresponding tests in `tests/test_agent.py`
4. **Critical**: Re-calibrate utility parameters if changing functional form
5. Document calibration in `traffic_fines/utils/parameters.py`

### Running Paper Simulations

```python
# Standard pattern for paper results
from traffic_fines.core.agent import Agent
from traffic_fines.core.society import Society
from traffic_fines.core.fines import IncomeBasedFine
from traffic_fines.core.optimizer import WelfareOptimizer
from traffic_fines.utils.income_generation import generate_income_distribution
from traffic_fines.utils.parameters import *
import numpy as np

# ALWAYS set seed for reproducibility
np.random.seed(42)

# Generate agents with Finnish calibration
incomes = generate_income_distribution(
    1000,
    mean=DEFAULT_MEAN_INCOME,  # 42,000 EUR
    sd=DEFAULT_SD_INCOME,      # 18,000 EUR
    distribution='lognormal',
    seed=42
)

# Create optimizer
optimizer = WelfareOptimizer(
    incomes,
    FlatFine,
    vsl=DEFAULT_VSL,
    death_prob_factor=DEFAULT_DEATH_PROB_FACTOR,
    income_utility_factor=DEFAULT_INCOME_UTILITY_FACTOR,
    labor_disutility_factor=DEFAULT_LABOR_DISUTILITY_FACTOR,
    speeding_utility_factor=DEFAULT_SPEEDING_UTILITY_FACTOR,
    max_iterations=DEFAULT_NUM_ITERATIONS
)

# Compare fine structures
results = optimizer.compare_fine_structures(DEFAULT_TAX_RATE)

# Save results for reproducibility
import pandas as pd
pd.DataFrame([results['flat'], results['income_based']]).to_csv('results.csv')
```

### Building and Publishing Paper

```bash
# Clean previous build
cd paper
jupyter-book clean .

# Build fresh (with execution if configured)
jupyter-book build .

# Check for broken links/references
jupyter-book build . --builder linkcheck

# Generate PDF (requires latex)
jupyter-book build . --builder pdflatex
```

## Known Issues & TODOs

### Critical for Publication
- [ ] Add locked dependency management (poetry.lock or requirements-lock.txt)
- [ ] Set up Jupyter Book execution caching (`.jupyter_cache/`)
- [ ] Create CITATION.cff for proper citation metadata
- [ ] Add pre-commit hooks for code quality
- [ ] Add regression tests for paper results
- [ ] Document computational environment (Python version, OS)

### Nice to Have
- [ ] Docker container for perfect replication
- [ ] Zenodo archival for code/data DOI
- [ ] Automated figure generation scripts
- [ ] DVC or git-lfs for large data files
- [ ] Continuous integration for paper build

## Paper Structure

The paper follows standard economics format:

1. `01_introduction.md` - Motivation and research question
2. `02_literature_review.md` - Related work
3. `03_theoretical_model.md` - Mathematical model
4. `04_calibration.md` - Parameter calibration to Finnish data
5. `05_results.ipynb` - **Computational results** (Jupyter notebook)
6. `06_discussion.md` - Interpretation and policy implications
7. `07_conclusion.md` - Summary and future work
8. `appendix_code.md` - Code documentation
9. `appendix_robustness.md` - Robustness checks

**Key file**: `paper/05_results.ipynb` contains all computational analysis and should produce deterministic results with seed=42.
