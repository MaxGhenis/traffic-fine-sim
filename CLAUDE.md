# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Traffic Fine Simulation is a Streamlit application that simulates the impact of different traffic fine structures (flat vs income-based) on social welfare. The simulation models agents with different income levels who make decisions about labor supply and speeding behavior based on utility optimization.

## Development Commands

### Run the application
```bash
streamlit run app.py
```

### Install dependencies
```bash
pip install -r requirements.txt
```

## Architecture

### Core Components

1. **app.py**: Main Streamlit application entry point. Handles UI, parameter configuration, and orchestrates simulations for both flat and income-based fine systems.

2. **model.py**: Contains the core simulation logic:
   - `Agent` class: Represents individuals who optimize their utility based on labor/leisure tradeoffs, speeding behavior, and income
   - `simulate_society`: Runs the multi-iteration society simulation with UBI redistribution
   - Fine functions: `flat_fine` and `income_based_fine`

3. **optimization.py**: Implements the scipy-based optimization to find optimal fine rates and tax rates that maximize total social utility.

4. **visualization.py**: Handles plotting of optimization history and income group analysis.

5. **utils.py**: Contains default parameters and utility functions:
   - Default simulation parameters (VSL, income distribution, utility factors)
   - Income generation functions
   - Constants like WORK_HOURS_PER_YEAR

6. **utility_explorer.py**: Interactive tool for exploring the utility function behavior with different parameters.

### Key Simulation Flow

1. Agents optimize their labor supply and speeding decisions based on:
   - Income utility (log utility from net income)
   - Labor disutility (quadratic in hours worked)
   - Speeding utility (log utility from speeding)
   - Death probability cost (VSL-weighted)

2. Society simulation iterates with:
   - Dynamic death probability based on average speeding
   - UBI calculated from total fines and taxes
   - Agents re-optimizing each iteration

3. Optimization searches for parameters that maximize total social utility using scipy's minimize with bounds.

## Important Notes

- The application uses numpy float64 types extensively for numerical stability
- Labor supply is measured in hours (0-2080 per year) and normalized to 0-1
- Speeding is a continuous variable between 0 and 1
- The simulation includes redistribution through UBI from collected fines and taxes