---
title: Introduction
---

# Introduction

How should traffic fines vary with income? Finland has linked speeding penalties to earnings since 1921, producing headlines when executives receive six-figure tickets. In the United States, San Francisco launched the first major income-based traffic fine pilot in 2025, and several other jurisdictions---including New York, which tested day-fines in Staten Island as early as 1988 {cite}`staten_island_pilot1988`---have experimented with similar systems. The motivation is straightforward: a \$200 fine that devastates a minimum-wage worker barely registers for a high earner. Income-based fines appear to solve this problem by scaling penalties with ability to pay {cite}`harris2016,polinsky_shavell1991`.

This paper identifies a countervailing force that complicates this reasoning. When fines depend on earned income, they function as an implicit marginal tax---but one that applies selectively to individuals who speed. This selective taxation distorts labor supply in a way that flat fines do not, compounding pre-existing deadweight losses from the income tax. We develop a model that captures this trade-off, calibrate it to US data using PolicyEngine microsimulation {cite}`policyengine_us2024`, and propagate parameter uncertainty through forward Monte Carlo simulation.

## The double distortion

The central mechanism is what we call the *double distortion*. The first distortion is intentional: fines deter speeding by raising its cost. The second is an unintended byproduct: by conditioning penalties on income, the fine system creates an implicit tax on earning, reducing labor supply among those who speed.

To see why this matters, consider a US worker whose marginal tax rate---combining federal income tax, state income tax, FICA payroll taxes, and benefit phase-outs---is already 35%. Under a flat fine, her labor supply decision is unaffected by her speeding---the fine is a lump sum. Under an income-based fine with rate $\phi$, her effective marginal tax rate becomes $\text{MTR}_i + \phi s$, where $s$ is her speeding intensity. Standard public finance results imply that deadweight loss rises with the *square* of the tax rate {cite}`harberger1964`, so adding even a few percentage points to an already-high marginal rate generates disproportionate efficiency costs.

Crucially, US marginal tax rates are dramatically heterogeneous across the income distribution. Workers on the EITC phase-out face effective marginal rates near 40% {cite}`maag_etal2012`, while some middle-income workers face rates below 25%. This heterogeneity---captured by the per-person marginal tax rates we compute from PolicyEngine's Enhanced CPS microsimulation---means that income-based fines interact very differently with the tax-benefit system at different income levels.

This interaction between fines and labor taxation connects to the *tax-interaction effect* identified in the environmental tax literature. {cite}`bovenberg_demooij1994` showed that Pigouvian taxes on pollution should be set below marginal external damage when they interact with distortionary labor taxes. {cite}`jacobs_demooij2015` qualified this result, showing the interaction vanishes at the second-best optimum when the income tax is set optimally. Our setting differs in a key respect: income-based fines apply only to offenders, creating heterogeneous effective tax rates that cannot be replicated by adjusting the income tax schedule.

## Contributions

This paper makes three contributions to the intersection of public economics and law and economics.

First, we develop a tractable model of joint labor supply and speeding decisions under alternative fine structures. Agents maximize utility over consumption, speeding, and leisure, subject to a budget constraint that embeds the fine structure. Speeding generates private benefits (time savings, utility from speed) but raises mortality risk following the Nilsson power model {cite}`nilsson2004`, where fatality risk scales as $(1+s)^n$ with $n \approx 4$. Under flat fines, labor and speeding decisions separate; under income-based fines, they are coupled through the effective tax rate. We solve for mean-field equilibrium where fine revenue is redistributed as a universal transfer.

Second, we calibrate the model to the United States using real microdata from PolicyEngine's Enhanced CPS {cite}`policyengine_us2024,census_cps2024`. Each simulated agent is drawn from the actual US income distribution and assigned their empirically estimated marginal tax rate---capturing federal and state income taxes, FICA payroll taxes, the EITC, and benefit phase-outs. This approach replaces the stylized single-tax-rate assumption of earlier work with dramatically heterogeneous tax treatment across the income distribution. We specify informative priors for behavioral parameters---drawing on meta-analyses for labor supply elasticities {cite}`chetty2012`, traffic safety parameters {cite}`nilsson2004,elvik2019`, and US regulatory estimates for VSL {cite}`epa_vsl2024`---and propagate uncertainty through 10,000 Monte Carlo draws.

Third, we decompose the welfare difference between fine systems into three components: a *deterrence gain* from more uniform penalties across the income distribution, a *labor distortion loss* from the implicit tax on earnings, and a *revenue effect* from differences in equilibrium fine and tax revenue. The decomposition clarifies when each force dominates and how the welfare ranking depends on key elasticities.

## Preview of results

Our baseline calibration using US CPS data finds that flat fines generate modestly higher utilitarian welfare than income-based fines under a wide range of parameter draws. The labor distortion channel is quantitatively important: income-based fines raise effective marginal tax rates for regular speeders by 2--8 percentage points, on top of already-heterogeneous baseline MTRs that range from near-zero to over 40%. This distortion interacts most severely with the EITC phase-out region, where low-income workers already face steep implicit taxes.

However, the welfare ranking is sensitive to the labor supply elasticity, the existing MTR distribution, and social preferences. When we move from utilitarian to Rawlsian welfare criteria---or when labor supply is sufficiently inelastic---income-based fines can dominate. The Monte Carlo analysis quantifies these sensitivities: the probability that flat fines dominate ranges from roughly 60% to 90% across plausible parameter configurations under utilitarian welfare.

## Roadmap

Section 2 reviews the literatures on optimal taxation, crime deterrence, speed-safety relationships, Pigouvian taxation with labor interactions, day-fine systems, and equity in monetary sanctions. Section 3 presents the model: utility specification, fine structures, first-order conditions, and mean-field equilibrium. Section 4 describes calibration using US CPS microdata and PolicyEngine marginal tax rates. Section 5 reports results, including welfare comparisons, distributional analysis, decomposition, and convergence diagnostics. Section 6 discusses sensitivity, institutional considerations, and policy implications. Section 7 concludes.
