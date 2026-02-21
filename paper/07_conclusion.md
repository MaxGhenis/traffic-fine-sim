---
title: Conclusion
---

# Conclusion

This paper has analyzed the welfare implications of income-based traffic fines through the lens of optimal taxation theory. Our central finding is that, despite the "double distortion" mechanism we identify, income-based fines generate higher welfare than flat fines under realistic US calibration. The deterrence equity gain from income-proportional penalties exceeds the labor distortion cost in the large majority of parameter configurations.

## Summary of findings

We developed a model where heterogeneous agents jointly optimize labor supply and speeding intensity under flat or income-based fine structures, with fine and tax revenue redistributed as a uniform transfer. The model incorporates the Nilsson power model {cite}`nilsson2004` for the speed-fatality relationship and is calibrated to the United States using per-agent marginal tax rates computed from Enhanced Current Population Survey (CPS) microdata via PolicyEngine microsimulation {cite}`policyengine_us2024,census_cps2024`. Behavioral parameters are drawn from informative priors grounded in meta-analytic estimates of labor supply elasticities {cite}`chetty2012`, US regulatory values for the value of statistical life (VSL) {cite}`epa_vsl2024`, and traffic fatality data from the National Highway Traffic Safety Administration (NHTSA) Fatality Analysis Reporting System (FARS) {cite}`nhtsa_fars2024`.

The key results are as follows.

First, income-based fines create an effective marginal tax rate of $\text{MTR}_i + \phi s$ on labor income, where $\text{MTR}_i$ is the agent's pre-existing marginal tax rate from the tax-benefit system, $\phi$ is the fine rate, and $s$ is speeding intensity. This implicit tax is absent under flat fines (Proposition 1). At the welfare-maximizing fine rate ($\phi^* \approx 0.076$, compared with a baseline calibrated rate of $\phi = 0.02$), the additional EMTR is typically 0.2--4 percentage points---quantitatively modest relative to the pre-existing MTR heterogeneity across the US income distribution.

Second, income-based fines generate higher utilitarian welfare than flat fines in 95% of Monte Carlo draws. The mean welfare difference favors income-based fines ($\Delta W = -0.83$, 95% CI: $[-3.22, 0.02]$). This result reflects the distributional gain from income-proportional penalties: low-income agents face lower fines, improving their consumption and welfare through the concavity of log utility. Income-based fines also reduce consumption inequality (Gini 0.325 vs.\ 0.343).

Third, the welfare advantage of income-based fines strengthens under inequality-averse social welfare functions. Under Rawlsian evaluation, income-based fines dominate in virtually all draws.

Fourth, welfare decomposition reveals that the deterrence channel is the dominant component: income-based fines reduce under-deterrence of high-income agents, where the convexity of the fatality-speed relationship makes speeding particularly costly. The labor distortion channel works against income-based fines but is quantitatively smaller.

## Policy implications

Our analysis provides support for income-based fine programs, with several caveats relevant to US jurisdictions moving toward greater experimentation---including San Francisco's 2025 speed camera pilot {cite}`sf_income_fines2025` and building on earlier experiments such as the Staten Island day-fine project {cite}`staten_island_pilot1988`.

The finding that income-based fines dominate under realistic calibration should not be taken as blanket endorsement. The labor distortion we identify is real, even if quantitatively small at current fine rates. Higher fine rates, contemporaneous income assessment, or populations with high labor supply elasticities could tip the balance. Finland's day-fine system partly avoids the double distortion through backward-looking income assessment based on previous-year tax returns {cite}`kaila2024`, which severs the contemporaneous link between work effort and fine liability. US jurisdictions designing income-based fine programs should consider whether backward-looking assessment could further reduce the efficiency costs we identify.

The interaction between income-based fines and the EITC phase-out deserves attention. Workers in the phase-out region already face effective marginal rates near 40% {cite}`maag_etal2012`; adding an income-based fine compounds this distortion. While our results show the net welfare effect is positive---because these workers also benefit from lower fines relative to a flat system---policymakers should monitor labor supply responses in this population.

More broadly, our framework demonstrates that income-based fines can achieve both deterrence and redistributive objectives through a single instrument, contrary to the Tinbergen principle {cite}`tinbergen1952`'s prescription of one instrument per objective. The practical question is whether the efficiency cost of this bundling is large enough to justify maintaining separate instruments---flat fines for deterrence and the tax-transfer system for redistribution {cite}`kaplow_shavell2002`. Our calibration suggests it is not.

## Future work

Several extensions would strengthen the analysis. Natural experiments from fine system reforms---including San Francisco's ongoing pilot---could provide causal estimates of labor supply responses to income-based fines. A multi-period extension would capture the distinction between backward-looking and contemporaneous income assessment, habit formation in speeding, and human capital accumulation. Allowing for heterogeneous risk attitudes and driving needs across agents would refine the welfare calculations. Incorporating external costs of speeding---harm to other road users, congestion, and environmental damage---would strengthen the case for deterrence and likely reinforce the welfare advantage of income-based fines. Finally, extending the model to include the extensive margin of labor supply would capture participation responses that may be important for low-income workers near the EITC phase-out.

## Concluding remarks

The debate over income-based fines exemplifies a recurring tension in public economics: the desire to make individual policy instruments serve multiple objectives. Our analysis identifies the theoretical cost of this approach---the double distortion from coupling fines with labor income---but finds that, with realistic US calibration, the empirical magnitude is small relative to the deterrence equity benefit. Income-based fines appear to be a case where the theoretical concern, while valid, does not override the practical advantages. As the United States considers expanding income-based fine programs, our analysis provides a principled basis for evaluating the trade-off---and suggests that, for most plausible parameter configurations, the trade-off favors income-based fines.
