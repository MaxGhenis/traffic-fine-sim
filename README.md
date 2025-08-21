# Traffic Fines Simulation Framework

A computational framework for analyzing the welfare effects of income-based versus flat traffic fine systems, with particular attention to labor supply distortions and optimal taxation principles.

## Overview

This package implements an agent-based model where heterogeneous agents optimize their labor supply and speeding decisions under different fine regimes. The model captures the implicit marginal tax rate effects of income-based fines and their interaction with existing tax systems.

## Key Features

- Agent-based simulation with utility optimization
- Comparison of flat vs. income-based fine systems
- Endogenous death probability based on aggregate speeding behavior
- Universal Basic Income redistribution mechanism
- Optimization of fine parameters to maximize social welfare
- Analysis of labor supply responses to implicit marginal tax rates

## Installation

```bash
pip install -e .[dev]
```

## Testing

```bash
pytest tests/ --cov=traffic_fines
```

## Documentation

Full documentation and academic paper available in the `paper/` directory, built with Jupyter Book.

## Citation

If you use this framework in your research, please cite:

```bibtex
@software{traffic_fines_2024,
  title={Traffic Fines Simulation Framework},
  author={Author Name},
  year={2024},
  url={https://github.com/yourusername/traffic-fines}
}
```

## License

MIT License - see LICENSE file for details.