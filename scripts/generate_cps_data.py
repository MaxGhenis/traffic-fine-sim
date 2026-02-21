"""Generate CPS agent microdata for the traffic fine simulation.

This script uses PolicyEngine US to extract working-age adult data from the
Current Population Survey (CPS) and saves it as a parquet file for use in
the simulation.

Requirements:
    policyengine_us must be installed. Install with:
        pip install policyengine-us
    or:
        uv pip install policyengine-us

Usage:
    python scripts/generate_cps_data.py
"""

from pathlib import Path

import numpy as np
import pandas as pd


def main() -> None:
    """Extract CPS microdata via PolicyEngine and save to parquet."""
    try:
        from policyengine_us import Microsimulation
    except ImportError:
        raise ImportError(
            "policyengine_us is required to generate CPS data. "
            "Install it with: pip install policyengine-us"
        )

    print("Initializing PolicyEngine microsimulation...")
    sim = Microsimulation()

    print("Extracting variables from CPS microdata...")
    # Use household_weight (calibrated via microcalibrate) rather than
    # person_weight (raw CPS weight, not calibrated to population totals)
    df = sim.calculate_dataframe(
        ["employment_income", "marginal_tax_rate", "age", "household_weight"]
    )

    print(f"Total CPS records: {len(df):,}")

    # Filter to working-age adults (18-64) with positive employment income
    mask = (df["age"] >= 18) & (df["age"] <= 64) & (df["employment_income"] > 0)
    df = df[mask].copy()
    # Rename to person_weight for downstream code (each person inherits
    # their household's calibrated weight)
    df = df.rename(columns={"household_weight": "person_weight"})
    print(f"Working-age adults with employment income > 0: {len(df):,}")

    # Clip marginal tax rates to [0, 0.95]
    # Benefit cliffs can produce MTRs > 100%, which are not meaningful for
    # the labor supply model
    df["marginal_tax_rate"] = np.clip(df["marginal_tax_rate"], 0.0, 0.95)

    # Compute hourly wage assuming 2080 hours/year (40 hrs/week * 52 weeks)
    df["hourly_wage"] = df["employment_income"] / 2080

    # Select and order output columns
    output_columns = [
        "employment_income",
        "marginal_tax_rate",
        "person_weight",
        "age",
        "hourly_wage",
    ]
    df = df[output_columns].reset_index(drop=True)

    # Save to parquet
    output_path = Path(__file__).parent.parent / "src" / "traffic_fines" / "data" / "cps_agents.parquet"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(output_path, index=False)
    print(f"\nSaved {len(df):,} records to {output_path}")

    # Print summary statistics
    print("\n--- Summary statistics ---")
    print(f"{'Observations:':<30} {len(df):>10,}")
    print(f"{'Mean employment income:':<30} ${df['employment_income'].mean():>10,.0f}")
    print(f"{'Median employment income:':<30} ${df['employment_income'].median():>10,.0f}")
    print(f"{'Mean marginal tax rate:':<30} {df['marginal_tax_rate'].mean():>10.3f}")
    print(f"{'Median marginal tax rate:':<30} {df['marginal_tax_rate'].median():>10.3f}")
    print(f"{'Std marginal tax rate:':<30} {df['marginal_tax_rate'].std():>10.3f}")
    print(f"{'Min marginal tax rate:':<30} {df['marginal_tax_rate'].min():>10.3f}")
    print(f"{'Max marginal tax rate:':<30} {df['marginal_tax_rate'].max():>10.3f}")
    print(f"{'Mean hourly wage:':<30} ${df['hourly_wage'].mean():>10.2f}")
    print(f"{'Median hourly wage:':<30} ${df['hourly_wage'].median():>10.2f}")
    print(f"{'Mean age:':<30} {df['age'].mean():>10.1f}")


if __name__ == "__main__":
    main()
