---
title: Discussion
---

# Discussion

Our analysis reveals a fundamental tension between the equity objectives of income-based fines and their efficiency costs through labor market distortions. This section discusses the sensitivity of our results to modeling choices, the role of institutional context, and implications for policy design.

## Backward-looking income assessment

The most important institutional qualification concerns the timing of income measurement. Finland's day-fine system calculates penalties from *previous-year* tax returns, not current income {cite}`kaila2024`. This backward-looking assessment severs the contemporaneous link between current labor effort and fine liability that drives the labor distortion in our model. When today's work hours do not affect today's fine, the effective marginal tax rate on current labor is $\tau$ regardless of speeding behavior.

This design feature substantially weakens the double distortion mechanism. However, it does not eliminate it entirely. Forward-looking agents who anticipate future fines will internalize that higher *future* income implies higher *future* fines, generating a dynamic version of the labor supply distortion. The strength of this channel depends on the persistence of income shocks, the frequency of violations, and discount rates. {cite}`kaila2024` finds limited evidence of labor supply responses in the Finnish system, consistent with the attenuation we would expect from backward-looking assessment.

A contemporaneous system---where fines are linked to current-year income, as would be feasible with real-time income verification---would exhibit the full force of the double distortion. Several proposed income-based fine systems in the United States contemplate using current income data, making our analysis directly relevant to their design.

## Sensitivity to the labor supply elasticity

Our results are most sensitive to the compensated labor supply elasticity, which governs the responsiveness of work effort to the effective marginal tax rate. The meta-analytic consensus from {cite}`chetty2012` and {cite}`saez2012` places the elasticity around 0.25 for broad income, but estimates vary by population and margin.

At the intensive margin, elasticities for prime-age men are typically 0.1--0.3 {cite}`keane2011`. At the extensive margin (participation), elasticities can be substantially larger, particularly for secondary earners and low-income workers. If income-based fines push some agents below their participation threshold---inducing them to exit the labor force entirely---the efficiency cost could be larger than our continuous model suggests.

The elasticity also varies over the business cycle and across institutional settings. Countries with generous social insurance may exhibit lower labor supply elasticities because the marginal value of additional earnings is reduced. Finland's comprehensive welfare state may therefore attenuate the double distortion relative to countries with weaker safety nets.

## Inequality and social preferences

The welfare ranking of fine systems depends critically on how society values equality. Under utilitarian preferences, the efficiency costs of income-based fines typically dominate. Under sufficiently inequality-averse social welfare functions, the distributional benefits of scaling fines with ability to pay can reverse this ranking.

{cite}`saez_stantcheva2016` provide a framework for incorporating diverse social preferences through generalized social marginal welfare weights. In their framework, the optimal degree of income-basedness depends on the weight society places on equity versus efficiency---a normative choice that our model can inform but not resolve. Our contribution is to quantify the efficiency cost so that policymakers can make this trade-off explicitly rather than assuming income-based fines are costless.

The Atkinson parameter $\varepsilon$ at which society is indifferent between the two systems is an informative summary statistic. A low crossover $\varepsilon$ means that even moderate inequality aversion justifies income-based fines despite their efficiency costs; a high crossover $\varepsilon$ means that only extreme prioritarianism favors the income-based system.

## The value of targeted deterrence

Income-based fines are motivated by the observation that flat fines under-deter the wealthy and over-deter the poor. Our model captures this asymmetry: under flat fines, high-income agents speed more because the fine represents a smaller fraction of their consumption. Income-based fines equalize the deterrence margin across the income distribution.

The welfare value of this equalization depends on the curvature of the death probability function. Under the power model with $n = 4$, speeding carries sharply increasing risk, and under-deterrence of high-income agents imposes significant external costs (through higher aggregate speeding and death probability). If speeding primarily harms the speeder, the external cost argument is weaker; our model focuses on private mortality risk but does not separately model external harm to other road users.

## Alternative policy instruments

If income-based fines are too blunt to navigate the equity-efficiency trade-off, several alternatives merit consideration.

**Payment flexibility.** Flat fines combined with income-contingent payment plans can address the regressivity concern without creating labor supply distortions. The fine amount remains flat, preserving the labor supply incentives, while the payment schedule accommodates liquidity constraints. Several U.S. jurisdictions have adopted such systems.

**Non-monetary sanctions.** Point-based systems, license suspensions, and community service requirements create penalties that are less directly tied to income. {cite}`bourgeon_picard2007` analyze point-record systems and show they can achieve effective deterrence through non-monetary channels. However, non-monetary sanctions may have their own distributional consequences if time costs or license dependency vary with income.

**Optimized transfers.** Rather than linking fines to income, flat fines can be paired with enhanced transfers to low-income households. {cite}`kaplow_shavell2002` advocate separating the pricing function (deterrence through fines) from the redistributive function (transfers through the tax system). This approach avoids the implicit tax on labor while achieving distributional goals through a more efficient instrument.

## Limitations

Our analysis rests on several simplifying assumptions that merit acknowledgment.

**Static model.** We analyze a single-period decision, abstracting from reputation effects, learning, and habit formation. Speeding behavior is likely persistent, and fines may have dynamic deterrent effects that our static model misses. The backward-looking income assessment in Finland's system introduces explicitly dynamic considerations that would require a multi-period model to analyze fully.

**Homogeneous preferences.** Within each income level, agents have identical preferences. Heterogeneity in risk attitudes, time preferences, or driving needs could affect optimal fine design. Agents who must drive for work, for example, face different trade-offs than recreational drivers.

**No enforcement heterogeneity.** We assume uniform detection probability across income levels. If wealthy individuals can better avoid detection---through legal representation, choice of routes, or vehicle technology---the effective deterrence of income-based fines may differ from what our model predicts.

**Proportional income tax.** We model a flat tax rate rather than the progressive schedule that actually applies in Finland. A progressive tax amplifies the double distortion for high earners (who already face high marginal rates) while attenuating it for low earners. The qualitative mechanism persists, but the quantitative welfare comparison could shift.

**No extensive margin.** Our model treats labor supply as a continuous intensive-margin choice. If income-based fines push some agents below their participation threshold, the efficiency costs would be larger than we estimate.

## Broader implications

The double distortion mechanism applies whenever penalties are linked to economic productivity. Criminal day-fines, income-contingent environmental penalties, and means-tested regulatory sanctions all create the same implicit tax on earnings that we identify for traffic fines. The general principle is that linking any cost to income adds to the effective marginal tax rate, with efficiency consequences that should be weighed against equity or deterrence benefits.

This connects to a broader theme in public economics: the Tinbergen principle, which holds that achieving $k$ policy objectives requires at least $k$ independent instruments. Income-based fines attempt to serve two objectives---deterrence and redistribution---with a single instrument. Our analysis suggests that separating these functions---using flat fines for deterrence and the tax-transfer system for redistribution---may achieve both objectives more efficiently.
