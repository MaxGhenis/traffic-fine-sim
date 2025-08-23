# Model Calibration

To ground our analysis in real-world data, we calibrate our model using parameters from Finland's day-fine system, which has been in operation since 1921 and provides the most comprehensive implementation of income-based traffic fines.

## Finnish Day-Fine System

Finland's system calculates fines for serious speeding violations (exceeding the limit by more than 20 km/h) using the following formula:

```
Day-fine amount = (Monthly net income - €255) / 60
```

The total fine equals the day-fine amount multiplied by the number of day-fines assigned based on violation severity. For our calibration, we focus on the income-dependency structure rather than the severity multiplier.

### Key Parameters from Finland

Based on the Finnish system and empirical evidence from Kaila (2024), we calibrate:

1. **Income gradient**: The Finnish formula implies a fine that is approximately 1.67% of monthly net income per day-fine (1/60 ≈ 0.0167), with a €255 monthly deduction for basic living expenses.

2. **Behavioral response**: Kaila (2024) finds that a €200 increase in fine amount reduces reoffending by 15% over six months, though this effect dissipates after 12 months. This suggests a short-term elasticity of speeding with respect to fine amount of approximately -0.075.

3. **Threshold effects**: Fines become income-based only for violations exceeding 20 km/h over the limit. Below this threshold, flat fines apply (€200 for cars, €100 for mopeds).

4. **Income distribution**: Finland's relatively compressed income distribution (Gini coefficient ≈ 0.27) differs from more unequal societies, affecting the welfare implications of income-based fines.

## Calibrated Model Parameters

### Fine Structure
For the income-based system, we model the Finnish approach as:
- Base fine: €200 (minimum for motor vehicles)
- Income factor: 0.0167 of monthly income per severity unit
- Basic deduction: €255 monthly (€3,060 annual)

This translates to our model's income-based fine function:

```
F(y) = max(200, 0.0167 × max(0, y_monthly - 255) × s)
```

where `y_monthly` is monthly income and `s` is the severity factor.

### Behavioral Parameters

**Speeding elasticity**: Based on Kaila's findings, we calibrate the utility from speeding to generate an elasticity of -0.075 in the short run. This relatively low elasticity suggests that speeding behavior is not highly responsive to fine amounts, consistent with information frictions or habitual behavior.

**Labor supply elasticity**: While Finland-specific estimates are limited, we use the consensus range from the labor economics literature of 0.2-0.4 for the intensive margin elasticity. Finland's high labor force participation suggests using the lower end of this range (0.25) for our baseline.

**Value of Statistical Life (VSL)**: We adopt the European Commission's recommended VSL of €3.6 million for Finland, adjusted to our model's units.

### Tax Environment

Finland's tax system features:
- Progressive income tax with marginal rates from 0% to 31.25% at the municipal level
- Additional state income tax up to 31.75% for high earners
- Combined top marginal rate approaching 60%

For our baseline calibration, we use an average marginal tax rate of 40%, representative of middle-to-upper income earners who are most affected by income-based fines.

## Validation Against Empirical Patterns

Our calibrated model reproduces several key empirical patterns:

1. **No bunching at thresholds**: Consistent with Kaila's findings, our model with information frictions does not generate bunching just below the 20 km/h threshold where fines become income-based.

2. **Temporary deterrence**: The model's dynamic extension (not shown in main results) generates temporary reductions in speeding following fine receipt, matching the 6-month effect found empirically.

3. **Income gradient of violations**: While comprehensive data on speeding by income is unavailable, our model's prediction that speeding increases modestly with income aligns with general patterns in traffic violations.

## Sensitivity to Context

We note that Finland's institutional context differs from other potential adopters of income-based fines:

- **Lower inequality**: Finland's compressed income distribution reduces the variance in fine amounts, limiting potential labor supply distortions
- **High trust in government**: May increase compliance and reduce enforcement costs
- **Strong social safety net**: Could reduce the marginal utility of income, affecting both deterrence and labor supply responses

These factors suggest that the optimal degree of income-basedness may be higher in Finland than in countries with greater inequality, lower institutional trust, or weaker safety nets.

## Optimal Income Gradients: Three Benchmarks

Our calibrated model allows us to compare three different income gradients for fines:

1. **Deterrence-only optimum (no LSR)**: When we ignore labor supply responses and focus solely on achieving uniform deterrence across income levels, the optimal fine gradient is approximately 2.5% of monthly income. This steep gradient reflects the declining marginal utility of income - higher earners need proportionally larger fines to achieve the same deterrent effect.

2. **Current Finnish policy**: Finland sets fines at 1.67% of monthly income (1/60), which represents a compromise between deterrence objectives and practical/political constraints. This gradient is already 33% lower than the pure deterrence optimum.

3. **Full optimum (with LSR)**: When labor supply responses are incorporated, the optimal gradient falls dramatically to just 0.5% of monthly income. This represents an 80% reduction from the deterrence-only optimum and is 70% below current Finnish policy.

The large gap between these benchmarks illustrates the quantitative importance of labor supply considerations. Ignoring these effects would lead policymakers to set income gradients that are far too steep from a total welfare perspective.

## Alternative Calibrations

To test robustness, we also consider:

1. **High inequality calibration**: Using U.S. income distribution (Gini ≈ 0.48)
2. **High elasticity calibration**: Labor supply elasticity of 0.5, speeding elasticity of -0.15
3. **Low tax calibration**: Average marginal rate of 25%, typical of countries with flatter tax structures

Results from these alternative calibrations are presented in the sensitivity analysis (Section 5.3).