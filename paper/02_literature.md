---
title: Literature review
---

# Literature review

This paper sits at the intersection of several literatures: optimal income taxation, the economics of crime and deterrence, the speed-safety relationship, Pigouvian taxation with pre-existing distortions, the Finnish day-fine system, and equity in monetary sanctions. We review each in turn, emphasizing the gap our model fills.

## Optimal taxation and behavioral responses

The modern theory of optimal taxation, initiated by {cite}`mirrlees1971` and extended by {cite}`diamond_mirrlees1971`, derives tax schedules that balance redistribution against efficiency costs arising from behavioral responses. {cite}`saez2001` showed that optimal marginal tax rates can be expressed in terms of sufficient statistics---principally the elasticity of taxable income (ETI)---without specifying the full structure of preferences. {cite}`feldstein1999` emphasized that the ETI captures all behavioral margins, including labor supply, tax avoidance, and evasion.

The empirical literature on the ETI, surveyed by {cite}`saez2012`, places central estimates around 0.25 for broad income, with a range of 0.12 to 0.40. {cite}`chetty2012` reconciles micro and macro labor supply estimates by accounting for optimization frictions, arriving at a Hicksian elasticity of approximately 0.25. {cite}`keane2011` provides a comprehensive survey, noting that intensive-margin elasticities for prime-age men are typically 0.1--0.3, while estimates for women and secondary earners are larger.

Our contribution extends this literature by identifying a novel source of effective marginal taxation: income-linked regulatory penalties. {cite}`maag_etal2012` document how benefit phase-outs create implicit marginal tax rates exceeding 80% for low-income families. We show that income-based fines create analogous distortions that vary with violation behavior, a channel not previously analyzed.

## Crime, deterrence, and fine design

{cite}`becker1968` established the framework for analyzing crime as a rational choice, where individuals weigh expected penalties against the benefits of offending. {cite}`polinsky_shavell1979` extended this to optimal fine design, showing that maximal fines with low detection probabilities minimize enforcement costs under risk neutrality. When offenders vary in wealth, {cite}`polinsky_shavell1991` showed that optimal fines should be wealth-dependent: flat fines over-deter the poor and under-deter the wealthy. {cite}`garoupa1997` and {cite}`polinsky_shavell2007` provide comprehensive surveys.

Empirically, {cite}`chalfin_mccrary2017` review the deterrence literature and find that both police presence and sanction severity reduce crime, with elasticities of crime to police around $-0.3$ to $-0.5$. {cite}`hansen2015` exploits sharp punishment thresholds for drunk driving in Washington State, finding that crossing a blood alcohol content cutoff that triggers harsher sanctions reduces recidivism. {cite}`deangelo_hansen2014` show that reduced police enforcement during budget crises increases traffic fatalities in Oregon. These studies confirm that traffic penalties have real deterrent effects.

The behavioral dimension complicates standard deterrence theory. {cite}`gneezy_rustichini2000` demonstrated in a daycare experiment that introducing small fines for late pickup *increased* lateness, suggesting fines can crowd out intrinsic motivation when set too low. {cite}`chetty_looney_kroft2009` showed that less salient taxes generate smaller behavioral responses, raising the question of whether the deterrent effect of income-based fines depends partly on their psychological salience.

Our model takes the deterrence motive seriously: income-based fines achieve more uniform expected disutility across the income distribution. The question is whether this benefit survives once labor supply distortions are accounted for.

## Speed-safety relationship

The relationship between vehicle speed and crash severity is central to our calibration. {cite}`nilsson2004` proposed the *power model*, in which fatal crashes are proportional to $(v_1/v_0)^n$ where $v_1$ and $v_0$ are the after and before speeds and $n \approx 4$ for fatalities, 3 for serious injuries, and 2 for all injury crashes. This nonlinear relationship implies that speeding carries sharply increasing marginal risk: a 10% speed increase roughly doubles fatality risk.

{cite}`elvik2019` re-estimated the power model across a broader set of studies, finding somewhat lower exponents (around 3.5 for fatalities) with variation by road type. We adopt the Nilsson parameterization with $n \sim \mathcal{N}(4.0, 0.5)$ as our prior, encompassing both estimates.

The power model is attractive for our purposes because it provides a micro-founded relationship between individual speeding intensity and mortality risk, avoiding the need to model crash mechanics directly. We express death probability as $p(s) = p_{\text{base}} \cdot (1+s)^n$, where $s \in [0,1]$ is fractional speed above the limit and $p_{\text{base}}$ is the baseline annual traffic fatality probability.

## Pigouvian taxation and labor market interaction

Our analysis closely parallels the literature on environmental taxes in the presence of pre-existing distortions. {cite}`bovenberg_demooij1994` showed that the optimal pollution tax falls *below* the Pigouvian level (marginal external damage) when it interacts with a distortionary labor tax. The intuition is that the environmental tax raises the cost of consumption, reducing the real wage and amplifying labor supply distortions---the *tax-interaction effect*. {cite}`bovenberg_goulder1996` showed that recycling environmental tax revenue through labor tax cuts (the *revenue-recycling effect*) partially but not fully offsets this interaction.

{cite}`jacobs_demooij2015` proved a striking irrelevance result: when the income tax is set optimally, the optimal Pigouvian tax equals marginal external damage regardless of pre-existing distortions. The tax-interaction and revenue-recycling effects exactly cancel at the second-best optimum.

Our setting differs from the standard Pigouvian framework in a crucial respect. Environmental taxes apply uniformly to all consumers of a polluting good, whereas income-based fines apply only to offenders. This creates *heterogeneous* effective tax rates: agents who speed more face higher marginal taxation on labor income. The resulting distortion cannot be offset by adjusting the uniform income tax schedule, because the planner cannot condition taxes on speeding behavior (which is the rationale for fines in the first place). This heterogeneity is why the Jacobs--de Mooij irrelevance result does not carry over to our setting.

## Finnish day-fines

Finland introduced the day-fine (*p\"aiv\"asakko*) system in 1921, making it the longest-running income-based penalty system. The formula sets the daily fine amount to roughly $(\text{monthly net income} - 255) / 60$, multiplied by a number of day-fine units determined by offense severity {cite}`kantorowicz_faure2021`. For speeding violations exceeding 20 km/h above the limit, fines become income-based; below this threshold, fixed petty fines (*rikesakko*) of around \euro200 apply.

{cite}`kaila2024` provides the most rigorous empirical analysis, exploiting discontinuities in the Finnish system. Key findings include: (i) income-based fines reduce reoffending, though effects attenuate after six months; (ii) there is limited evidence of labor supply responses, potentially because day-fines are calculated from *previous-year* tax returns rather than current income; and (iii) there is no bunching in the income distribution near fine thresholds. The backward-looking income assessment is an important institutional feature: it severs the contemporaneous link between current work effort and fine liability that drives the labor distortion in our model. We discuss this distinction in Section 6.

Several other countries use related systems. Switzerland and several German states employ day-fine variants for criminal offenses, though not for traffic violations. {cite}`kantorowicz_faure2021` provide a comparative analysis, finding broad support for the deterrence equity rationale but limited formal welfare analysis.

## Equity and monetary sanctions

A growing literature documents the regressive impact of flat monetary sanctions. {cite}`harris2016` shows that fines, fees, and court costs disproportionately burden low-income individuals, creating cycles of debt, license suspension, and incarceration. {cite}`lerman_weaver2014` demonstrate that contact with the criminal justice system---including monetary sanctions---erodes civic participation and trust in government, with downstream consequences for democratic engagement.

These findings motivate the equity case for income-based fines: if flat penalties trap the poor in punitive cycles while failing to deter the wealthy, calibrating fines to ability to pay seems both fair and efficient. {cite}`saez_stantcheva2016` provide a framework for incorporating such concerns through generalized social marginal welfare weights that can reflect a society's equity preferences.

However, the public economics literature counsels caution about using individual policy instruments for redistribution. {cite}`kaplow_shavell2002` argue on both theoretical and practical grounds that distributional concerns are better addressed through the tax-and-transfer system than through the design of specific regulatory policies. Our analysis provides a quantitative test of this principle: we compare the welfare effects of addressing fine regressivity through income-linking (which creates labor distortions) versus maintaining flat fines and relying on the existing fiscal system for redistribution.

## Synthesis

No previous work has formally modeled the interaction between income-based fines and labor supply decisions in a setting with heterogeneous agents, endogenous speeding, and mean-field equilibrium. The closest contributions are the environmental tax literature---which analyzes Pigouvian taxes with labor interactions but not heterogeneous exposure---and the law and economics literature on wealth-dependent sanctions---which considers optimal deterrence but not labor supply responses. Our model fills this gap by combining elements from both traditions in a calibrated simulation framework.
