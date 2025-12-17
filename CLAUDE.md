# CLAUDE.md

This file provides guidance to Claude Code when working with this repository.

## Project Overview

Traffic Fines Simulation is a Python package for analyzing the welfare effects of income-based versus flat traffic fine systems. The package implements an agent-based model where heterogeneous agents optimize their labor supply and speeding decisions under different fine regimes.

## Development Commands

```bash
# Install with uv (recommended)
uv sync

# Run tests
uv run pytest tests/ -v

# Run tests with coverage
uv run pytest tests/ --cov=traffic_fines --cov-report=term-missing

# Build paper (JupyterBook 2.0)
cd paper && uv run jupyter-book build .
```

## Architecture

```
traffic_fines/           # Core Python package
├── core/
│   ├── agent.py         # Agent class with utility optimization
│   ├── fines.py         # FlatFine, IncomeBasedFine structures
│   ├── society.py       # Society simulation with equilibrium dynamics
│   └── optimizer.py     # WelfareOptimizer for finding optimal parameters
└── utils/
    └── parameters.py    # Default parameters (Finnish calibration)

paper/                   # JupyterBook 2.0 academic paper
tests/                   # pytest test suite (54 tests, 98% coverage)
```

## Key Components

**Agent (`traffic_fines/core/agent.py`):**
- Optimizes labor supply (0-2080 hours/year) and speeding (0-1)
- Utility: log(consumption) + α·log(1+speeding) - β·hours²/2 - p(s)·VSL
- Uses scipy L-BFGS-B optimizer

**Fine Structures (`traffic_fines/core/fines.py`):**
- `FlatFine`: Fixed amount, marginal rate = 0
- `IncomeBasedFine`: Fine = rate × income × speeding, creates implicit tax

**Society (`traffic_fines/core/society.py`):**
- Iterates: agents optimize → update death probability → redistribute as UBI → repeat
- Tracks convergence, calculates Gini coefficient

**WelfareOptimizer (`traffic_fines/core/optimizer.py`):**
- Finds welfare-maximizing fine parameters
- Compares flat vs income-based systems

## Testing

All code follows TDD (Test-Driven Development). Tests are in `tests/` using pytest.

```bash
uv run pytest tests/test_agent.py -v      # Agent tests
uv run pytest tests/test_fines.py -v      # Fine structure tests
uv run pytest tests/test_society.py -v    # Society tests
uv run pytest tests/test_optimizer.py -v  # Optimizer tests
```

## Paper

The academic paper is in `paper/` using JupyterBook 2.0 with MyST markdown.
Configuration is in `paper/myst.yml`.
