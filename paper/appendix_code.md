# Appendix A: Code Documentation

## Package Structure

The `traffic_fines` package is organized as follows:

```
traffic_fines/
├── core/
│   ├── agent.py          # Individual agent optimization
│   ├── society.py        # Society simulation
│   ├── fines.py          # Fine structure implementations
│   └── optimizer.py      # Welfare optimization
└── utils/
    ├── parameters.py      # Default parameters
    ├── income_generation.py  # Income distribution utilities
    └── analysis.py        # Welfare metrics calculation
```

## Key Classes

### Agent Class
Represents an individual economic agent who optimizes labor supply and speeding decisions.

```python
class Agent:
    def optimize(self, fine_function, death_prob, ubi, tax_rate, vsl):
        """Optimize labor supply and speeding decisions."""
        # Returns: (labor_hours, speeding, utility)
```

### Society Class
Simulates a society of agents through iterative equilibrium.

```python
class Society:
    def simulate(self, max_iterations=100):
        """Run society simulation until convergence."""
        # Returns: dict with results
```

### Fine Structures
Abstract base class with concrete implementations:
- `FlatFine`: Fixed fine amount for all violators
- `IncomeBasedFine`: Fine proportional to income
- `ProgressiveFine`: Bracket-based progressive fines

## Installation

```bash
pip install -e .
```

## Testing

```bash
pytest tests/ --cov=traffic_fines
```

## Replication

All results can be replicated by running:
```bash
cd paper
make full-build
```

Source code available at: https://github.com/yourusername/traffic-fine-sim