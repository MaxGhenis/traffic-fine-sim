---
title: Calibration
---

# Calibration

We calibrate the model to Finland, which operates the world's longest-running income-based fine system and provides the best available data for this analysis. Rather than fixing parameters at point estimates, we specify informative priors for each parameter and propagate uncertainty through forward Monte Carlo simulation with 10,000 draws. This section traces each parameter to its empirical source.

## Preference parameters

### Speeding utility weight ($\alpha$)

The parameter $\alpha$ governs the private benefit agents derive from speeding. We set $\alpha \sim \mathcal{N}(0.5, 0.15)$, calibrated to match observed Finnish speeding rates under the day-fine system. Higher values of $\alpha$ generate more speeding in equilibrium and make deterrence more valuable, tilting the comparison toward income-based fines. There is no direct empirical estimate of this parameter; instead, we choose the prior mean so that equilibrium speeding intensity is in the range 0.05--0.15, consistent with Finnish enforcement data indicating that most detected violations are 5--15 km/h above posted limits.

### Labor disutility ($\beta$)

The parameter $\beta$ controls the curvature of the labor disutility function $\beta(h/H)^2/2$. We set $\beta \sim \mathcal{N}(1.0, 0.3)$, calibrated to generate Frisch elasticities in the range 0.1--0.3. With our utility specification, the Frisch elasticity at an interior optimum is approximately:

$$\varepsilon^F \approx \frac{w(1-\tau)}{\beta \cdot (h/H) \cdot (1+c)}$$

At median Finnish wages (~\euro22/hour), typical hours (~1,500/year), and a 30% tax rate, $\beta = 1.0$ yields $\varepsilon^F \approx 0.25$, consistent with the meta-analytic consensus from {cite}`chetty2012` and survey evidence from {cite}`keane2011`. The standard deviation of 0.3 spans the range from 0.1 (low elasticity, as typical for prime-age men) to 0.4 (higher elasticity, as found for some subgroups).

### Maximum hours ($H$)

We fix $H = 2{,}080$ hours per year (40 hours/week $\times$ 52 weeks) with no uncertainty. This serves as a normalization; the effective labor supply margin operates through the interior choice of $h$.

## Safety parameters

### Value of statistical life ($V$)

We adopt $V \sim \mathcal{N}(3{,}600{,}000, \; 900{,}000)$ EUR, following the European Commission's recommended VSL for transport safety analysis {cite}`eu_vsl2014`. The 25% coefficient of variation reflects the substantial range in meta-analytic estimates, which vary with methodology, population, and income level. The VSL enters the model as a scaling factor in the death cost term $p(s) \cdot V / (1+c)$; higher values increase the private cost of speeding and reduce equilibrium speeding intensity under both fine systems.

### Baseline death probability ($p_{\text{base}}$)

The baseline annual traffic fatality probability is $p_{\text{base}} \sim \mathcal{N}(0.001, 0.0005)$. This is calibrated from Finnish road safety statistics: approximately 220 annual traffic fatalities among 3.5 million licensed drivers, yielding a raw rate of $6.3 \times 10^{-5}$. We scale this up to $10^{-3}$ to reflect the *conditional* risk for active drivers with significant speeding exposure, calibrated to produce interior solutions where agents choose positive but moderate speeding. The standard deviation spans an order of magnitude, from the raw statistical rate to more aggressive risk assumptions.

### Speed-fatality exponent ($n$)

The power model exponent is $n \sim \mathcal{N}(4.0, 0.5)$, following {cite}`nilsson2004`, who estimated $n \approx 4$ for fatalities across international data. {cite}`elvik2019` found somewhat lower values ($n \approx 3.5$) in updated estimates. Our prior encompasses both, with a range from approximately 3 to 5. This parameter is critical: higher exponents make speeding more dangerous and increase the value of deterrence, favoring income-based fines.

## Fiscal parameters

### Tax rate ($\tau$)

We set $\tau \sim \mathcal{N}(0.30, 0.05)$, representing the average effective tax rate in Finland. Finland's tax system is progressive, with combined municipal and state income tax rates ranging from 0% to approximately 55%. The mean of 0.30 represents the effective rate for middle-income earners who constitute the bulk of driving violations. The tax rate is a key parameter for the double distortion: higher baseline tax rates amplify the deadweight loss from the additional implicit tax created by income-based fines {cite}`harberger1964`.

## Income distribution

Agent wages are drawn from a lognormal distribution calibrated to Finnish income data {cite}`statistics_finland2023`:

$$\log(y) \sim \mathcal{N}(\mu_{\log}, \sigma_{\log})$$

with mean annual income \euro45,000 and standard deviation \euro25,000. These moments imply $\mu_{\log} \approx 10.49$ and $\sigma_{\log} \approx 0.53$. The lognormal specification generates right-skewed income distributions with a median below the mean, consistent with observed Finnish income data (median ~\euro35,000, mean ~\euro45,000). We simulate $N = 1{,}000$ agents per equilibrium computation; convergence tests at $N \in \{500, 1000, 2000\}$ confirm that results are stable.

Hourly wages are derived by dividing annual incomes by maximum hours: $w_i = y_i / H$.

## Fine system parameters

### Flat fine

The flat fine baseline is $F = \text{\euro}200$, matching the standard Finnish petty fine (*rikesakko*) for speeding violations under 20 km/h above the limit.

### Income-based fine

The income-based fine rate is $\phi = 0.002$ per unit speeding intensity, calibrated to approximate the Finnish day-fine formula. In Finland, the day-fine amount is approximately $(\text{monthly net income} - 255) / 60 \approx 0.017 \times \text{monthly net income}$ per day-fine unit {cite}`kantorowicz_faure2021`. With a typical severity of 12 day-fine units, the total fine is roughly $0.017 \times 12 = 0.2$ times monthly net income, or about 0.017 times annual income per unit of speeding. Our rate of 0.002 per unit speeding intensity reflects the continuous approximation and the fact that most violations involve modest speeding ($s \approx 0.1$).

## Monte Carlo procedure

For each of 10,000 draws:

1. Draw $(\alpha, \beta, V, p_{\text{base}}, n, \tau)$ independently from their Normal priors, clipping to valid ranges ($\alpha, \beta > 0.01$; $p_{\text{base}} \in [10^{-8}, 0.1]$; $n \in [0.5, 10]$; $\tau \in [0.01, 0.99]$).
2. Draw $N = 1{,}000$ agent wages from the lognormal income distribution.
3. Solve mean-field equilibrium under the flat fine ($F = 200$).
4. Solve mean-field equilibrium under the income-based fine ($\phi = 0.002$).
5. Record utilitarian welfare, mean speeding, Gini coefficient, and equilibrium transfers for each system.
6. Compute the welfare difference $\Delta W = W_{\text{flat}} - W_{\text{IB}}$ and its decomposition.

This procedure generates a joint distribution of outcomes over parameter uncertainty, allowing us to report credible intervals and welfare dominance probabilities rather than point estimates. {numref}`tab:priors` summarizes the prior specifications.

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
  - Calibrated to Finnish speeding rates
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
  - 3,600,000
  - 900,000
  - {cite}`eu_vsl2014`
* - Baseline death probability
  - $p_{\text{base}}$
  - 0.001
  - 0.0005
  - Finnish road safety statistics
* - Speed-fatality exponent
  - $n$
  - 4.0
  - 0.5
  - {cite}`nilsson2004`, {cite}`elvik2019`
* - Tax rate
  - $\tau$
  - 0.30
  - 0.05
  - {cite}`statistics_finland2023`
* - Labor supply elasticity
  - $\varepsilon$
  - 0.25
  - 0.10
  - {cite}`chetty2012`
```
