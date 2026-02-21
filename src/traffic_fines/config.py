"""Configuration module: loads YAML data, defines typed dataclasses, validates.

Single entry point for all data used by the model.
All YAML files live in src/traffic_fines/data/.
"""

from dataclasses import dataclass
from pathlib import Path
from typing import Optional

import yaml

DATA_DIR = Path(__file__).parent / "data"

# Cache for loaded YAML files
_cache: dict = {}


def _load_yaml(filename: str) -> dict:
    if filename not in _cache:
        with open(DATA_DIR / filename) as f:
            _cache[filename] = yaml.safe_load(f)
    return _cache[filename]


# --- Dataclasses ---


@dataclass(frozen=True)
class Prior:
    mean: float
    sd: float
    source: str
    description: str
    unit: Optional[str] = None


@dataclass(frozen=True)
class AgentPriors:
    alpha: Prior
    beta: Prior
    max_hours: Prior


@dataclass(frozen=True)
class SafetyPriors:
    vsl: Prior
    death_prob_base: Prior
    speed_fatality_exponent: Prior


@dataclass(frozen=True)
class FiscalPriors:
    """Fiscal priors (tax rates now come from CPS microdata)."""
    pass


@dataclass(frozen=True)
class LaborPriors:
    elasticity: Prior


@dataclass(frozen=True)
class ModelPriors:
    agent: AgentPriors
    safety: SafetyPriors
    fiscal: FiscalPriors
    labor: LaborPriors


@dataclass(frozen=True)
class IncomeDistribution:
    type: str
    mean_income: float
    income_std: float
    unit: str
    n_agents: int


@dataclass(frozen=True)
class FlatFineConfig:
    amount: float
    unit: str


@dataclass(frozen=True)
class IncomeFineConfig:
    rate: float
    min_fine: float
    unit: str
    severity_days: int


@dataclass(frozen=True)
class FineSystemConfig:
    flat: FlatFineConfig
    income_based: IncomeFineConfig


# --- Accessor functions ---


def _make_prior(d: dict) -> Prior:
    return Prior(
        mean=d["mean"],
        sd=d["sd"],
        source=d["source"],
        description=d["description"],
        unit=d.get("unit"),
    )


def load_priors() -> ModelPriors:
    if "priors" in _cache:
        return _cache["priors"]
    raw = _load_yaml("priors.yaml")
    result = ModelPriors(
        agent=AgentPriors(
            alpha=_make_prior(raw["agent"]["alpha"]),
            beta=_make_prior(raw["agent"]["beta"]),
            max_hours=_make_prior(raw["agent"]["max_hours"]),
        ),
        safety=SafetyPriors(
            vsl=_make_prior(raw["safety"]["vsl"]),
            death_prob_base=_make_prior(raw["safety"]["death_prob_base"]),
            speed_fatality_exponent=_make_prior(
                raw["safety"]["speed_fatality_exponent"]
            ),
        ),
        fiscal=FiscalPriors(),
        labor=LaborPriors(
            elasticity=_make_prior(raw["labor"]["elasticity"]),
        ),
    )
    _cache["priors"] = result
    return result


def load_income_distribution() -> IncomeDistribution:
    if "income_dist" in _cache:
        return _cache["income_dist"]
    raw = _load_yaml("income_distribution.yaml")
    result = IncomeDistribution(
        type=raw["distribution"]["type"],
        mean_income=raw["distribution"]["mean_income"],
        income_std=raw["distribution"]["income_std"],
        unit=raw["distribution"]["unit"],
        n_agents=raw["simulation"]["n_agents"],
    )
    _cache["income_dist"] = result
    return result


def load_fine_systems() -> FineSystemConfig:
    if "fine_systems" in _cache:
        return _cache["fine_systems"]
    raw = _load_yaml("fine_systems.yaml")
    result = FineSystemConfig(
        flat=FlatFineConfig(
            amount=raw["flat"]["amount"],
            unit=raw["flat"]["unit"],
        ),
        income_based=IncomeFineConfig(
            rate=raw["income_based"]["rate"],
            min_fine=raw["income_based"]["min_fine"],
            unit=raw["income_based"]["unit"],
            severity_days=raw["income_based"]["severity_days"],
        ),
    )
    _cache["fine_systems"] = result
    return result


def load_externalities() -> dict:
    return _load_yaml("externalities.yaml")


def clear_cache() -> None:
    _cache.clear()


def validate() -> list[str]:
    """Check data integrity. Returns list of error strings (empty = OK)."""
    errors = []
    priors = load_priors()

    # Priors with positive sd (skip fixed params like max_hours)
    for name, prior in [
        ("alpha", priors.agent.alpha),
        ("beta", priors.agent.beta),
        ("vsl", priors.safety.vsl),
        ("death_prob_base", priors.safety.death_prob_base),
        ("speed_fatality_exponent", priors.safety.speed_fatality_exponent),
        ("elasticity", priors.labor.elasticity),
    ]:
        if prior.sd < 0:
            errors.append(f"Prior '{name}' has negative sd: {prior.sd}")

    # Reasonableness checks
    if not (0 < priors.agent.alpha.mean < 2):
        errors.append(f"alpha mean {priors.agent.alpha.mean} not in (0, 2)")
    if not (5_000_000 < priors.safety.vsl.mean < 20_000_000):
        errors.append(f"VSL mean {priors.safety.vsl.mean} not in (5M, 20M)")
    if not (0 < priors.safety.speed_fatality_exponent.mean < 8):
        errors.append(
            f"Exponent mean {priors.safety.speed_fatality_exponent.mean} not in (0, 8)"
        )

    # Income distribution
    dist = load_income_distribution()
    if dist.mean_income <= 0:
        errors.append(f"mean_income must be positive, got {dist.mean_income}")
    if dist.income_std <= 0:
        errors.append(f"income_std must be positive, got {dist.income_std}")

    # Fine systems
    fines = load_fine_systems()
    if fines.flat.amount <= 0:
        errors.append(f"flat fine amount must be positive, got {fines.flat.amount}")
    if not (0 < fines.income_based.rate < 1):
        errors.append(
            f"income fine rate must be in (0, 1), got {fines.income_based.rate}"
        )

    clear_cache()
    return errors
