# CLAUDE.md

## Project overview

Traffic fine simulation: analyzes welfare effects of income-based vs flat traffic fines. Heterogeneous agents optimize labor supply and speeding under different fine regimes. Calibrated to Finland's day-fine system.

## Development commands

```bash
uv sync                                      # Install
uv run pytest tests/ -v --no-cov             # Fast tests (114 tests, ~2min)
uv run pytest tests/ -v                      # Tests with coverage
uv run python -c "from traffic_fines.pipeline import run_analysis; r = run_analysis(n_samples=200, n_agents=50); r.save('src/traffic_fines/data/results.json')"  # Generate results
```

## Architecture

```
src/traffic_fines/
├── evidence.py        # 35 Source dataclasses (whatnut pattern)
├── config.py          # Typed YAML loaders + validation
├── model.py           # Agent optimization + mean-field equilibrium
├── montecarlo.py      # Forward MC over parameter uncertainty
├── welfare.py         # Welfare functions + optimizer
├── pipeline.py        # Orchestration → results.json
└── data/
    ├── priors.yaml           # All params with mean, sd, source
    ├── income_distribution.yaml
    ├── fine_systems.yaml
    ├── externalities.yaml
    └── results.json          # Generated output (single source of truth)

tests/                 # 114 tests, TDD
paper/                 # JupyterBook 2.0 / MyST (7 chapters)
```

## Key model

**Utility:** `U = log(1+c) + α·log(1+s) - β·(h/H)²/2 - p(s)·VSL/(1+c)`

**Death probability (Nilsson 2004):** `p(s) = p_base·(1+s)^n, n≈4`

**Equilibrium:** Mean-field fixed point with damped iteration (relative convergence).

**Monte Carlo:** Forward sampling from priors (Normal), 10k samples for production.

## Evidence tracing

Every parameter in YAML files has a `source` field linking to a `Source` dataclass in `evidence.py`. Every source has DOI or database reference, URL, study type. `validate_sources()` checks integrity.

## Testing

TDD throughout. Tests validate: evidence integrity, config loading, utility properties, equilibrium convergence, MC reproducibility, pipeline end-to-end, JSON serialization.
