---
title: Conclusion
---

# Conclusion

This paper has analyzed the welfare implications of income-based traffic fines through the lens of optimal taxation theory. Our central finding is that, despite the "double distortion" mechanism we identify, income-based fines generate higher welfare than flat fines under realistic US calibration. The deterrence equity gain from income-proportional penalties exceeds the labor distortion cost in the large majority of parameter configurations.

## Summary of findings

We developed a model where heterogeneous agents jointly optimize labor supply and speeding intensity under flat or income-based fine structures, with fine and tax revenue redistributed as a uniform transfer. The model incorporates the Nilsson power model {cite}`nilsson2004` for the speed-fatality relationship and is calibrated to the United States using per-agent marginal tax rates computed from Enhanced Current Population Survey (CPS) microdata via PolicyEngine microsimulation {cite}`policyengine_us2024,census_cps2024`. Behavioral parameters are drawn from informative priors grounded in meta-analytic estimates of labor supply elasticities {cite}`chetty2012`, US regulatory values for the value of statistical life (VSL) {cite}`epa_vsl2024`, and traffic fatality data from the National Highway Traffic Safety Administration (NHTSA) Fatality Analysis Reporting System (FARS) {cite}`nhtsa_fars2024`.

The key results are as follows.

First, income-based fines create an effective marginal tax rate of $\text{MTR}_i + \phi s$ on labor income, where $\text{MTR}_i$ is the agent's pre-existing marginal tax rate from the tax-benefit system, $\phi$ is the fine rate, and $s$ is speeding intensity. This implicit tax is absent under flat fines (Proposition 1). At the baseline calibrated rate ($\phi = 0.02$), the additional EMTR is 0.2--2 percentage points; at the welfare-maximizing rate ($\phi^* \approx 0.076$), it rises to 0.8--4 percentage points---still small relative to the 0--50 percentage point range of pre-existing MTRs across the US income distribution.

Second, income-based fines generate higher utilitarian welfare than flat fines in 95% of Monte Carlo draws. The mean welfare difference favors income-based fines ($\Delta W = 0.83$, 95% CI: $[-0.02, 3.22]$). This result reflects the distributional gain from income-proportional penalties: low-income agents face lower fines, improving their consumption and welfare through the concavity of log utility. Income-based fines also reduce consumption inequality (Gini 0.325 vs.\ 0.343).

Third, the welfare advantage of income-based fines strengthens under inequality-averse social welfare functions. Under Rawlsian evaluation, income-based fines dominate in virtually all draws.

Fourth, welfare decomposition reveals that the deterrence channel is the dominant component: income-based fines reduce under-deterrence of high-income agents, where the convexity of the fatality-speed relationship makes speeding particularly costly. The labor distortion channel works against income-based fines but is quantitatively smaller.

## Policy implications

Under our calibration, income-based fines generate higher welfare than flat fines, with several caveats relevant to US jurisdictions moving toward greater experimentation---including San Francisco's 2025 speed camera pilot {cite}`sf_income_fines2025` and building on earlier experiments such as the Staten Island day-fine project {cite}`staten_island_pilot1988`.

The finding that income-based fines dominate under realistic calibration should not be taken as blanket endorsement. The labor distortion we identify is real, and our model's quadratic disutility specification implies a Frisch elasticity of 1.0---four times the empirical consensus---meaning the labor distortion in our simulations is larger than it would be at realistic elasticities. Even so, higher fine rates, contemporaneous income assessment, or specific subpopulations with high participation elasticities could tip the balance. Backward-looking income assessment, as in Finland's day-fine system {cite}`kaila2024`, would attenuate the labor distortion channel by severing the contemporaneous link between work effort and fine liability.

The interaction between income-based fines and the EITC phase-out deserves attention. Workers in the phase-out region already face effective marginal rates near 40% {cite}`maag_etal2012`; adding an income-based fine compounds this distortion. While our results show the net welfare effect is positive---because these workers also benefit from lower fines relative to a flat system---the labor supply response in this population remains a key empirical unknown for evaluating income-based fines.

More broadly, our framework demonstrates that income-based fines can achieve both deterrence and redistributive objectives through a single instrument, contrary to the Tinbergen principle {cite}`tinbergen1952`'s prescription of one instrument per objective. The practical question is whether the efficiency cost of this bundling is large enough to justify maintaining separate instruments---flat fines for deterrence and the tax-transfer system for redistribution {cite}`kaplow_shavell2002`. Our calibration suggests it is not.

## Future work

Several extensions would strengthen the analysis. Natural experiments from fine system reforms---including San Francisco's ongoing pilot---could provide causal estimates of labor supply responses to income-based fines. A multi-period extension would capture the distinction between backward-looking and contemporaneous income assessment, habit formation in speeding, and human capital accumulation. Allowing for heterogeneous risk attitudes and driving needs across agents would refine the welfare calculations. Incorporating external costs of speeding---harm to other road users, congestion, and environmental damage---would strengthen the case for deterrence and likely reinforce the welfare advantage of income-based fines. Finally, extending the model to include the extensive margin of labor supply would capture participation responses that may be important for low-income workers near the EITC phase-out.

## Concluding remarks

As the United States considers expanding income-based fine programs, the framework developed here provides a principled basis for evaluating the equity-efficiency trade-off. Under our calibration, the labor distortion cost is an order of magnitude smaller than the deterrence equity gain for most plausible parameter configurations, even with a Frisch elasticity four times the empirical consensus.
