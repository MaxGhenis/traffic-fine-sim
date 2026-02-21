---
title: Calibration
---

# Calibration

We calibrate the model to the United States, using real microdata from the Enhanced Current Population Survey (CPS) via PolicyEngine {cite}`policyengine_us2024`. Rather than fixing parameters at point estimates, we specify informative priors for behavioral parameters and propagate uncertainty through forward Monte Carlo simulation with 10,000 draws. The key innovation is using empirically estimated per-agent marginal tax rates that capture the full complexity of the US tax-benefit system.

## Income distribution and marginal tax rates

### CPS microdata

Agent wages and tax rates are drawn from the Enhanced CPS microdata, processed through PolicyEngine's US microsimulation model {cite}`policyengine_us2024,census_cps2024`. We restrict the sample to working-age adults (18--64) with positive employment income, yielding approximately 70,000 observations representing the US working population.

For each observation, PolicyEngine computes the marginal tax rate accounting for:
- Federal income tax (including bracket structure and standard deduction)
- State income taxes (varying across all 50 states plus DC)
- FICA payroll taxes (Social Security 6.2% + Medicare 1.45%, with Social Security cap)
- Earned Income Tax Credit phase-in and phase-out
- Benefit phase-outs (SNAP, Medicaid, housing assistance, etc.)

The resulting MTR distribution is dramatically heterogeneous. Workers in the EITC phase-out region face effective marginal rates near 40% {cite}`maag_etal2012`, while some middle-income workers above the EITC range but below higher tax brackets face rates around 22--25%. High earners face combined federal-state rates of 40--50%. This heterogeneity is a key empirical contribution: it means income-based fines interact very differently with the tax-benefit system at different income levels, amplifying the double distortion for workers already facing high marginal rates.

We clip marginal tax rates to the range $[0, 0.95]$ to handle occasional values exceeding 100% that arise from benefit cliffs (discrete jumps in program eligibility).

### Sampling procedure

Each Monte Carlo draw samples $N = 1{,}000$ agents with replacement from the CPS microdata, using person survey weights as sampling probabilities. This weighted bootstrap preserves the representative structure of the CPS while allowing independent draws across simulations. Each sampled agent carries their empirical wage (employment income / 2,080 hours) and marginal tax rate.

Hourly wages are derived as $w_i = y_i / H$ where $y_i$ is annual employment income and $H = 2{,}080$ hours.

## Preference parameters

### Speeding utility weight ($\alpha$)

The parameter $\alpha$ governs the private benefit agents derive from speeding. We set $\alpha \sim \mathcal{N}(0.5, 0.15)$, calibrated to match observed US speeding rates. Higher values of $\alpha$ generate more speeding in equilibrium and make deterrence more valuable, tilting the comparison toward income-based fines. We choose the prior mean so that equilibrium speeding intensity is in the range 0.05--0.15, consistent with NHTSA data indicating that speeding is a factor in approximately 29% of traffic fatalities {cite}`nhtsa_fars2024`.

### Labor disutility ($\beta$)

The parameter $\beta$ controls the curvature of the labor disutility function $\beta(h/H)^2/2$. We set $\beta \sim \mathcal{N}(1.0, 0.3)$, calibrated to generate Frisch elasticities in the range 0.1--0.3. At median US wages (~\$27/hour), typical hours (~1,800/year), and a median effective tax rate of ~28%, $\beta = 1.0$ yields $\varepsilon^F \approx 0.25$, consistent with the meta-analytic consensus from {cite}`chetty2012` and survey evidence from {cite}`keane2011`.

### Maximum hours ($H$)

We fix $H = 2{,}080$ hours per year (40 hours/week $\times$ 52 weeks) with no uncertainty. This serves as a normalization; the effective labor supply margin operates through the interior choice of $h$.

## Safety parameters

### Value of statistical life ($V$)

We adopt $V \sim \mathcal{N}(11{,}600{,}000, \; 2{,}900{,}000)$ USD, following the US EPA's central estimate for regulatory impact analyses {cite}`epa_vsl2024`. The 25% coefficient of variation reflects the substantial range in meta-analytic estimates. The VSL enters the model as a scaling factor in the death cost term $p(s) \cdot V / (1+c)$; higher values increase the private cost of speeding and reduce equilibrium speeding intensity under both fine systems.

### Baseline death probability ($p_{\text{base}}$)

The baseline annual traffic fatality probability is $p_{\text{base}} \sim \mathcal{N}(0.00012, 0.00006)$. This is derived from NHTSA FARS data {cite}`nhtsa_fars2024`: 1.37 deaths per 100 million vehicle miles traveled, combined with average annual driving of approximately 13,400 miles per licensed driver, yields an annual fatality probability of approximately $1.2 \times 10^{-4}$.

### Speed-fatality exponent ($n$)

The power model exponent is $n \sim \mathcal{N}(4.0, 0.5)$, following {cite}`nilsson2004`, who estimated $n \approx 4$ for fatalities across international data. {cite}`elvik2019` found somewhat lower values ($n \approx 3.5$) in updated estimates. Our prior encompasses both, with a range from approximately 3 to 5. This parameter is critical: higher exponents make speeding more dangerous and increase the value of deterrence, favoring income-based fines.

## Fine system parameters

### Flat fine

The flat fine baseline is $F = \$130$, approximating the US national average for speeding tickets based on data from the National Center for State Courts.

### Income-based fine

The income-based fine rate is $\phi = 0.002$ per unit speeding intensity. There is no established US income-based fine system to calibrate against directly; we adopt a rate consistent with European day-fine systems {cite}`kantorowicz_faure2021` and the San Francisco pilot {cite}`sf_income_fines2025`. At median US income (~\$56,000), a speeding intensity of $s = 0.1$ yields a fine of $0.002 \times 56{,}000 \times 0.1 = \$11.20$---modest enough to be politically feasible while creating a measurable implicit tax on labor income.

## Monte Carlo procedure

For each of 10,000 draws:

1. Sample $N = 1{,}000$ agents with replacement from CPS microdata (weighted bootstrap), obtaining per-agent wages $w_i$ and marginal tax rates $\text{MTR}_i$.
2. Draw $(\alpha, \beta, V, p_{\text{base}}, n)$ independently from their Normal priors, clipping to valid ranges ($\alpha, \beta > 0.01$; $p_{\text{base}} \in [10^{-8}, 0.1]$; $n \in [0.5, 10]$).
3. Solve mean-field equilibrium under the flat fine ($F = 130$).
4. Solve mean-field equilibrium under the income-based fine ($\phi = 0.002$).
5. Record utilitarian welfare, mean speeding, Gini coefficient, and equilibrium transfers for each system.
6. Compute the welfare difference $\Delta W = W_{\text{flat}} - W_{\text{IB}}$ and its decomposition.

Note that tax rates are **not drawn from priors**---they are empirical, fixed per agent, drawn from the CPS microdata. This is a key methodological improvement over using a single scalar tax rate parameter.

{numref}`tab:priors` summarizes the prior specifications.

```{list-table} Prior specifications
:header-rows: 1
:name: tab:priors

* - Parameter
  - Symbol
  - Mean
  - SD
  - Source
* - Speeding utility weight
  - $\alpha$
  - 0.50
  - 0.15
  - Calibrated to US speeding rates
* - Labor disutility
  - $\beta$
  - 1.00
  - 0.30
  - {cite}`keane2011`, {cite}`chetty2012`
* - Maximum hours
  - $H$
  - 2,080
  - 0
  - Standard full-time year
* - Value of statistical life
  - $V$
  - 11,600,000
  - 2,900,000
  - {cite}`epa_vsl2024`
* - Baseline death probability
  - $p_{\text{base}}$
  - 0.00012
  - 0.00006
  - {cite}`nhtsa_fars2024`
* - Speed-fatality exponent
  - $n$
  - 4.0
  - 0.5
  - {cite}`nilsson2004`, {cite}`elvik2019`
* - Labor supply elasticity
  - $\varepsilon$
  - 0.25
  - 0.10
  - {cite}`chetty2012`
```
