---
title: Calibration
---

# Calibration

We calibrate the model to the United States, using real microdata from the Enhanced Current Population Survey (CPS) via PolicyEngine {cite}`policyengine_us2024`. Rather than fixing parameters at point estimates, we specify informative priors for behavioral parameters and propagate uncertainty through forward Monte Carlo simulation. The key innovation is using empirically estimated per-agent marginal tax rates that capture the full complexity of the US tax-benefit system.

## Income distribution and marginal tax rates

### CPS microdata

Agent wages and tax rates are drawn from the Enhanced CPS microdata, processed through PolicyEngine's US microsimulation model {cite}`policyengine_us2024,census_cps2024`. We restrict the sample to working-age adults (18–64) with positive employment income, yielding approximately 19,400 observations representing the US working population.

For each observation, PolicyEngine computes the marginal tax rate accounting for federal income tax (including bracket structure and standard deduction), state income taxes (varying across all 50 states plus DC), Federal Insurance Contributions Act (FICA) payroll taxes (Social Security 6.2% plus Medicare 1.45%, with the Social Security wage cap), Earned Income Tax Credit (EITC) phase-in and phase-out, and benefit phase-outs including the Supplemental Nutrition Assistance Program (SNAP), Medicaid, and housing assistance.

The resulting MTR distribution is dramatically heterogeneous. Workers in the EITC phase-out region face effective marginal rates near 40% {cite}`maag_etal2012`, while some middle-income workers above the EITC range but below higher tax brackets face rates around 22–25%. High earners face combined federal-state rates of 40–50%. This heterogeneity is a key empirical contribution: it means income-based fines interact very differently with the tax-benefit system at different income levels, amplifying the double distortion for workers already facing high marginal rates.

We clip marginal tax rates to the range $[0, 0.95]$ to handle occasional values exceeding 100% that arise from benefit cliffs (discrete jumps in program eligibility).

### Sampling procedure

Each Monte Carlo draw samples $N = 50$ agents with replacement from the CPS microdata, using calibrated household weights as sampling probabilities. This weighted bootstrap preserves the representative structure of the CPS while allowing independent draws across simulations. Each sampled agent carries their empirical wage (employment income / 2,080 hours) and marginal tax rate.

Hourly wages are derived as $w_i = y_i / H$ where $y_i$ is annual employment income and $H = 2{,}080$ hours.

## Preference parameters

### Speeding utility weight ($\alpha$)

The parameter $\alpha$ governs the private benefit agents derive from speeding. We set $\alpha \sim \mathcal{N}(0.5, 0.15)$. Higher values of $\alpha$ generate more speeding in equilibrium and make deterrence more valuable, tilting the comparison toward income-based fines. In our baseline calibration, equilibrium mean speeding intensity is approximately 0.37, higher than typical observed behavior (most speeders exceed limits by 5–15 mph, corresponding to $s \approx 0.08$–$0.23$). This elevated speeding arises because our model does not include detection probability or non-monetary penalties (points, license suspension), which in practice constrain speeding. The continuous fine formulation $F \cdot s$ or $\phi \cdot y \cdot s$ can be interpreted as the expected fine conditional on the full enforcement technology {cite}`becker1968`, and the implied detection probability would then scale down the equilibrium speeding intensity. We discuss the implications of this calibration in Section 6.

### Labor disutility ($\beta$)

The parameter $\beta$ scales the labor disutility function $\beta(h/H)^2/2$. We set $\beta \sim \mathcal{N}(1.0, 0.3)$, which governs equilibrium hours and the level of labor disutility.

The quadratic specification implies a Frisch elasticity of labor supply that is identically 1.0, regardless of $\beta$. To see this, note that the Frisch elasticity is $\varepsilon^F = v'(h) / [h \cdot v''(h)]$. For $v(h) = \frac{\beta}{2}(h/H)^2$, we have $v'(h) = \beta h / H^2$ and $v''(h) = \beta / H^2$, so $\varepsilon^F = (\beta h / H^2) / (h \cdot \beta / H^2) = 1$. The parameter $\beta$ affects equilibrium hours but not the curvature ratio that determines the elasticity.

This implied Frisch elasticity of 1.0 is higher than the meta-analytic consensus of approximately 0.25 from {cite}`chetty2012` and {cite}`keane2011`. Targeting $\varepsilon^F = 0.25$ would require a higher-power specification such as $v(h) \propto (h/H)^{1+1/\varepsilon} = (h/H)^5$. We retain the quadratic form for analytical tractability and because the higher elasticity makes our results *more conservative*: since the labor distortion from income-based fines is increasing in the elasticity, the welfare advantage of income-based fines would be even larger at the empirically estimated elasticity of 0.25 than at our model's value of 1.0. The finding that income-based fines dominate in 95% of draws despite an elasticity four times the consensus estimate strengthens the qualitative conclusion.

### Maximum hours ($H$)

We fix $H = 2{,}080$ hours per year (40 hours/week $\times$ 52 weeks) with no uncertainty. This serves as a normalization; the effective labor supply margin operates through the interior choice of $h$.

## Safety parameters

### Value of statistical life ($V$)

We adopt $V \sim \mathcal{N}(11{,}600{,}000, \; 2{,}900{,}000)$ USD, following the US EPA's central estimate for regulatory impact analyses {cite}`epa_vsl2024`. The 25% coefficient of variation reflects the range in meta-analytic estimates. The VSL enters the model as a scaling factor in the death cost term $p(s) \cdot V / (1+c)$; higher values increase the private cost of speeding and reduce equilibrium speeding intensity under both fine systems.

### Baseline death probability ($p_{\text{base}}$)

The baseline annual traffic fatality probability is $p_{\text{base}} \sim \mathcal{N}(0.00012, 0.00006)$. This is derived from NHTSA FARS data {cite}`nhtsa_fars2024`: 1.37 deaths per 100 million vehicle miles traveled, combined with average annual driving of approximately 13,400 miles per licensed driver, yields an annual fatality probability of approximately $1.2 \times 10^{-4}$.

### Speed-fatality exponent ($n$)

The power model exponent is $n \sim \mathcal{N}(4.0, 0.5)$, following {cite}`nilsson2004`, who estimated $n \approx 4$ for fatalities across international data. {cite}`elvik2019` found somewhat lower values ($n \approx 3.5$) in updated estimates. Our prior encompasses both, with a range from approximately 3 to 5. This parameter is critical: higher exponents make speeding more dangerous and increase the value of deterrence, favoring income-based fines.

## Fine system parameters

### Flat fine

The flat fine baseline is $F = \$130$, approximating the US national average for speeding tickets based on data from the National Center for State Courts.

### Income-based fine

The income-based fine rate is $\phi = 0.02$ per unit speeding intensity. There is no established US income-based fine system to calibrate against directly; we adopt a rate consistent with European day-fine systems {cite}`kantorowicz_faure2021` and the San Francisco pilot {cite}`sf_income_fines2025`. At median US income (~\$56,000), a speeding intensity of $s = 0.1$ yields a fine of $0.02 \times 56{,}000 \times 0.1 = \$112$—comparable to the flat fine at median income, providing a revenue-neutral comparison while creating a measurable implicit tax on labor income.

## Monte Carlo procedure

For each Monte Carlo draw, the procedure is as follows. Sample $N$ agents with replacement from CPS microdata using calibrated household weights as sampling probabilities, obtaining per-agent wages $w_i$ and marginal tax rates $\text{MTR}_i$. Draw $(\alpha, \beta, V, p_{\text{base}}, n)$ independently from their Normal priors, clipping to valid ranges ($\alpha, \beta > 0.01$; $p_{\text{base}} \in [10^{-8}, 0.1]$; $n \in [0.5, 10]$). Find the welfare-maximizing flat fine $F^*$ and income-based rate $\phi^*$ by grid search. Solve mean-field equilibrium under each optimal fine system. Record utilitarian welfare, mean speeding, Gini coefficient, and equilibrium transfers for each system. Compute the welfare difference $\Delta W = W_{\text{IB}} - W_{\text{flat}}$ and its decomposition.

The baseline specification uses 100 Monte Carlo draws with 50 agents per draw. The moderate sample sizes reflect the computational cost of solving mean-field equilibrium with per-agent L-BFGS-B optimization inside a damped fixed-point iteration loop; each draw requires solving two equilibria (flat and income-based), each involving repeated optimization of all agents until convergence. The standard error of the estimated probability $\Pr(\Delta W > 0)$ at $\hat{p} = 0.95$ is approximately $\sqrt{0.95 \times 0.05 / 100} \approx 0.022$, adequate to establish the direction of the welfare comparison.

Tax rates are **not drawn from priors**—they are empirical, fixed per agent, drawn from the CPS microdata. This is a key methodological improvement over using a single scalar tax rate parameter.

The following table summarizes the prior specifications.

| Parameter | Symbol | Mean | SD | Source |
|---|---|---|---|---|
| Speeding utility weight | $\alpha$ | 0.50 | 0.15 | Calibrated to US speeding rates |
| Labor disutility | $\beta$ | 1.00 | 0.30 | {cite}`keane2011`, {cite}`chetty2012` |
| Maximum hours | $H$ | 2,080 | 0 | Standard full-time year |
| Value of statistical life | $V$ | 11,600,000 | 2,900,000 | {cite}`epa_vsl2024` |
| Baseline death probability | $p_{\text{base}}$ | 0.00012 | 0.00006 | {cite}`nhtsa_fars2024` |
| Speed-fatality exponent | $n$ | 4.0 | 0.5 | {cite}`nilsson2004`, {cite}`elvik2019` |
| Frisch elasticity (implied by quadratic $v$) | $\varepsilon^F$ | 1.0 | --- | Implied by $v(h) = \frac{\beta}{2}(h/H)^2$; see text |
