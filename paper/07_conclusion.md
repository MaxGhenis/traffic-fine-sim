---
title: Conclusion
---

# Conclusion

This paper has analyzed the welfare implications of income-based traffic fines through the lens of optimal taxation theory. Our central finding is that income-based fines, while appealing on equity grounds, function as implicit marginal taxes that distort labor supply. The resulting efficiency costs---what we term the "double distortion"---must be weighed against the deterrence equity benefits of scaling penalties with income.

## Summary of findings

We developed a model where heterogeneous agents jointly optimize labor supply and speeding intensity under flat or income-based fine structures, with fine and tax revenue redistributed as a uniform transfer. The model incorporates the Nilsson power model {cite}`nilsson2004` for the speed-fatality relationship and is calibrated to the United States using per-agent marginal tax rates computed from Enhanced Current Population Survey (CPS) microdata via PolicyEngine microsimulation {cite}`policyengine_us2024,census_cps2024`. Behavioral parameters are drawn from informative priors grounded in meta-analytic estimates of labor supply elasticities {cite}`chetty2012`, US regulatory values for the value of statistical life (VSL) {cite}`epa_vsl2024`, and traffic fatality data from the National Highway Traffic Safety Administration (NHTSA) Fatality Analysis Reporting System (FARS) {cite}`nhtsa_fars2024`.

The key results are as follows.

First, income-based fines create an effective marginal tax rate of $\text{MTR}_i + \phi s$ on labor income, where $\text{MTR}_i$ is the agent's pre-existing marginal tax rate from the tax-benefit system, $\phi$ is the fine rate, and $s$ is speeding intensity. This implicit tax is absent under flat fines, where the labor supply decision is independent of fine structure (Proposition 1). Because US marginal tax rates are heterogeneous---ranging from near-zero for some workers to over 40\% for those on the Earned Income Tax Credit (EITC) phase-out {cite}`maag_etal2012`---the efficiency cost of adding to already-high rates varies dramatically across the income distribution.

Second, the welfare comparison between the two systems depends critically on the labor supply elasticity. Under utilitarian preferences and central parameter estimates, flat fines generate higher welfare in a majority of Monte Carlo draws. However, the ranking is uncertain: income-based fines dominate in a non-trivial share of parameter configurations, particularly when labor supply is inelastic.

Third, the welfare ranking reverses under sufficiently inequality-averse social preferences. Rawlsian evaluation consistently favors income-based fines because they reduce the penalty burden on the poorest agents. The Atkinson family of welfare functions traces the crossover between these conclusions as a function of inequality aversion.

Fourth, welfare decomposition reveals that the labor distortion channel is the primary source of welfare loss from income-based fines, typically exceeding the deterrence equity gain. The revenue effect---differences in equilibrium transfers---is a smaller component.

## Policy implications

Our analysis suggests several principles for the design of income-based fine systems, particularly as US jurisdictions move toward greater experimentation---following San Francisco's 2025 speed camera pilot {cite}`sf_income_fines2025` and building on earlier experiments such as the Staten Island day-fine project {cite}`staten_island_pilot1988`.

The labor distortion identified in this paper is strongest when fines are based on contemporaneous income, the labor supply elasticity is moderate to high, and pre-existing marginal tax rates are already elevated. Finland's day-fine system partly avoids the double distortion through backward-looking income assessment based on previous-year tax returns {cite}`kaila2024`, which severs the contemporaneous link between work effort and fine liability. US jurisdictions designing income-based fine programs should consider whether backward-looking assessment could attenuate the efficiency costs we identify, while recognizing that forward-looking agents may still internalize future fine liability.

The efficiency costs of income-linking may be avoided by maintaining flat fines for deterrence and addressing distributional concerns through the tax-transfer system---income-contingent payment plans, fine forgiveness for demonstrated hardship, or enhanced transfers to low-income households {cite}`kaplow_shavell2002`. This approach follows the Tinbergen principle of assigning each policy instrument to its comparative advantage: fines for deterrence, transfers for redistribution. The interaction between income-based fines and the EITC phase-out is particularly concerning, as it compounds an already-steep implicit tax on the working poor---the very population that income-based fines are intended to help.

More broadly, proposals for income-based fines should be evaluated not only for their direct effects on deterrence and equity but also for their interaction with the existing tax-benefit system. Our framework provides a quantitative method for this evaluation, incorporating parameter uncertainty and alternative social welfare functions.

## Future work

Several extensions would strengthen the analysis. Natural experiments from fine system reforms---including San Francisco's ongoing pilot---could provide causal estimates of labor supply responses to income-based fines. A multi-period extension would capture the distinction between backward-looking and contemporaneous income assessment, habit formation in speeding, and human capital accumulation. Allowing for heterogeneous risk attitudes and driving needs across agents would refine the welfare calculations. Incorporating external costs of speeding---harm to other road users, congestion, and environmental damage---would strengthen the case for deterrence and potentially shift the optimal fine structure. Finally, extending the model to include the extensive margin of labor supply would capture participation responses that may be first-order for low-income workers near the EITC phase-out.

## Concluding remarks

The debate over income-based fines exemplifies a recurring tension in public economics: the desire to make individual policy instruments serve multiple objectives. Income-based fines simultaneously pursue deterrence and redistribution, but the mechanisms through which they achieve these goals interact with each other and with the existing tax-benefit system in ways that create unintended costs. As the United States considers expanding income-based fine programs, our analysis provides a principled basis for evaluating the trade-off between deterrence equity and labor supply efficiency---a trade-off that should be made explicitly rather than assumed away. The key empirical inputs---the distribution of marginal tax rates across the income distribution, labor supply elasticities, and speeding behavior---are all measurable, making this welfare comparison empirically grounded rather than purely theoretical.
