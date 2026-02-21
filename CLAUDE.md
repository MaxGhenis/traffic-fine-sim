# CLAUDE.md

## Project overview

Traffic fine simulation: analyzes welfare effects of income-based vs flat traffic fines. Heterogeneous agents optimize labor supply and speeding under different fine regimes. Calibrated to the United States using PolicyEngine Enhanced CPS microdata with per-agent marginal tax rates.

## Development commands

```bash
uv sync                                      # Install
uv run pytest tests/ -v --override-ini="addopts="   # Tests (139 tests, ~4min)
uv run python scripts/generate_cps_data.py   # Regenerate CPS data (requires policyengine-us)
uv run python -c "from traffic_fines.pipeline import run_analysis; r = run_analysis(n_samples=100, n_agents=50); r.save('src/traffic_fines/data/results.json')"  # Generate results (~30min)
```

## Architecture

```
src/traffic_fines/
├── evidence.py        # 35+ Source dataclasses (US sources)
├── config.py          # Typed YAML loaders + validation
├── model.py           # Agent optimization + mean-field equilibrium
├── cps_data.py        # CPS microdata loading + weighted bootstrap sampling
├── montecarlo.py      # Forward MC over parameter uncertainty
├── welfare.py         # Welfare functions + optimizer + decomposition
├── pipeline.py        # Orchestration -> results.json
└── data/
    ├── priors.yaml           # All params with mean, sd, source
    ├── cps_agents.parquet    # Pre-generated CPS data (19.4k workers)
    ├── fine_systems.yaml
    ├── externalities.yaml
    └── results.json          # Generated output (single source of truth)

tests/                 # 139 tests, TDD
paper/                 # MyST (7 chapters), target: ITPF
scripts/               # generate_cps_data.py (PolicyEngine dependency)
```

## Key model

**Utility:** `U = log(1+c) + alpha*log(1+s) - beta*(h/H)^2/2 - p(s)*VSL/(1+c)`

**Death probability (Nilsson 2004):** `p(s) = p_base*(1+s)^n, n~4`

**Budget:** Flat: `c = wh(1-MTR) - Fs + T`; IB: `c = wh(1-MTR-phi*s) + T`

**Per-agent MTRs:** From PolicyEngine Enhanced CPS (federal + state + FICA + EITC + benefit phase-outs)

**Equilibrium:** Mean-field fixed point with damped iteration.

## Evidence tracing

Every parameter in YAML files has a `source` field linking to a `Source` dataclass in `evidence.py`. Every source has DOI or database reference, URL, study type. `validate_sources()` checks integrity.

## Testing

TDD throughout. Tests validate: evidence integrity, config loading, utility properties, equilibrium convergence, MC reproducibility, pipeline end-to-end, JSON serialization, CPS data loading, welfare decomposition.
