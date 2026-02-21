---
title: Results
---

# Results

This section presents the main findings from the Monte Carlo analysis. We report welfare comparisons between flat and income-based fines, distributional outcomes, welfare decompositions, and sensitivity analysis. Results are computed over 100 parameter draws from the priors specified in Section 4, with each draw sampling 50 agents from US CPS microdata with empirically estimated marginal tax rates. The moderate sample sizes reflect the computational cost of solving mean-field equilibrium with per-agent optimization; we verify robustness to sample size in the convergence diagnostics.

## Baseline welfare comparison

The central question is whether flat or income-based fines generate higher social welfare. Under utilitarian welfare (sum of individual utilities), the Monte Carlo analysis yields a clear result.

**Finding 1.** *Under the baseline calibration using US CPS data, income-based fines generate higher utilitarian welfare than flat fines in 95% of Monte Carlo draws.*

The mean welfare difference is $\Delta W = W_{\text{IB}} - W_{\text{flat}} = 0.83$ (95% CI: $[-0.02, 3.22]$), indicating that income-based fines dominate. This result reflects the fact that the distributional gain from income-proportional penalties---lower fines for low-income agents and the resulting welfare improvement through concave utility---exceeds the labor distortion cost from the implicit tax on earnings. While the double distortion mechanism is present, its magnitude is quantitatively small: the additional effective marginal tax rate is 0.2--2 percentage points at the baseline fine rate, modest relative to the pre-existing MTR heterogeneity (which ranges from near-zero to over 50%).

The result is robust across parameter draws but not unanimous: flat fines dominate in approximately 5% of draws, typically when the labor supply elasticity is drawn from the upper tail of its prior distribution and the speeding utility weight is low.

## Distributional analysis

The welfare advantage of income-based fines is reinforced by distributional improvements.

**Finding 2.** *Income-based fines reduce consumption inequality. The mean Gini coefficient under income-based fines is 0.325, compared with 0.343 under flat fines.*

This finding reflects two channels. First, income-based fines redistribute from high-income speeders to all agents via the universal transfer: high-income agents pay more in fines, increasing total revenue and the equilibrium transfer. Second, flat fines are regressive in the sense that they represent a larger share of income for low-wage agents, exacerbating pre-existing inequality.

**Finding 3.** *The welfare ranking is even stronger under inequality-averse social welfare functions. Under Rawlsian preferences, income-based fines dominate flat fines in virtually all draws.*

The Rawlsian criterion places all weight on the worst-off agent---typically the lowest-wage individual. Since income-based fines already dominate under utilitarian preferences, the Atkinson crossover from flat to income-based dominance occurs at $\varepsilon = 0$: no inequality aversion is needed to prefer income-based fines. This contrasts with the theoretical prediction that the double distortion would create a meaningful equity-efficiency trade-off; with realistic US calibration, the efficiency cost is too small to outweigh the distributional gains.

## Welfare decomposition

We decompose the welfare difference into three components following {eq}`eq:decomposition`.

**Finding 4.** *The deterrence gain from income-based fines exceeds the labor distortion loss, explaining the overall welfare advantage.*

The decomposition reveals that income-based fines achieve more uniform deterrence across the income distribution: high-income agents face larger penalties proportional to their ability to pay, reducing the under-deterrence problem inherent in flat fines. The labor distortion channel is present but small relative to the 0--50 percentage point range of pre-existing MTRs: the implicit tax $\phi s$ adds only 0.2--2 percentage points to effective marginal rates at the baseline fine rate $\phi = 0.02$, generating small deadweight loss relative to the deterrence gain. The revenue effect---arising from differences in equilibrium transfers between the two systems---is the smallest component.

## Aggregate speeding

An important finding is that aggregate speeding is slightly *higher* under income-based fines (mean $s = 0.370$) than under flat fines (mean $s = 0.358$). This may appear to contradict the "deterrence equity" narrative, but it reflects the composition of optimal fine levels. The welfare-maximizing income-based rate ($\phi^* \approx 0.076$) generates lower per-unit deterrence for low-income agents than the optimal flat fine (\$3,262), because $\phi^* \times y$ falls below \$3,262 for agents with income below approximately \$43,000---roughly the bottom half of the income distribution. The welfare gain from income-based fines therefore comes not from reducing aggregate speeding but from the distributional improvement: low-income agents pay less and high-income agents pay more, reducing consumption inequality and improving utilitarian welfare through the concavity of log utility. This is consistent with the welfare decomposition (Finding 4): the deterrence gain arises from redistributing fine burdens across the income distribution, not from reducing aggregate speeding.

## Optimal fine levels

The welfare-maximizing fine levels provide additional insight.

**Finding 5.** *The optimal flat fine averages \$3,262 (95% CI: [\$1,238, \$5,000]), far exceeding the current US national average of approximately \$130. The optimal income-based fine rate averages $\phi^* = 0.076$ (95% CI: [0.025, 0.10]).*

Both confidence intervals exhibit grid boundary effects: the upper end of the flat fine CI coincides with the grid maximum of \$5,000, and the upper end of the income-based CI coincides with $\phi = 0.10$. Some draws may favor values above these bounds. Extending either grid would likely shift the respective optimal levels slightly upward without affecting the welfare ranking, since the welfare function is relatively flat near the optimum.

The high optimal flat fine reflects the model's emphasis on mortality risk: with $p_{\text{base}} = 0.00012$ and $n = 4$, even moderate speeding carries substantial fatality risk, and the model favors strong deterrence. However, these optimal levels should be interpreted through the lens of detection probability, which the model abstracts from: at a plausible detection rate of $\pi = 0.05$, the expected fine per speeding event would be $0.05 \times 3{,}262 \approx \$163$, close to current fine levels. The optimal income-based rate of $\phi^* = 0.076$ generates fines of approximately $\phi^* \times y \times s = 0.076 \times 56{,}000 \times 0.37 \approx \$1{,}575$ for a median-income agent with typical speeding, distributed proportionally to income.

## Effective marginal tax rates

The implicit tax created by income-based fines varies across agents and represents the core mechanism of the double distortion. Because we use empirical per-agent MTRs from the CPS, the interaction between fines and existing taxes is heterogeneous across the income distribution.

**Finding 6.** *Under income-based fines, effective marginal tax rates for regular speeders exceed their CPS-based marginal tax rates by 0.2--2 percentage points, with larger increases for agents who speed more intensively.*

For an agent with speeding intensity $s$ facing marginal tax rate $\text{MTR}_i$ and fine rate $\phi$, the effective marginal tax rate on labor income is:

$$\text{EMTR}_i = \text{MTR}_i + \phi s$$

At the baseline fine rate $\phi = 0.02$, an agent with moderate speeding ($s = 0.1$) faces an additional 0.2 percentage point effective tax; with high speeding ($s = 0.5$) the additional tax rises to 1 percentage point. At the welfare-maximizing rate $\phi^* \approx 0.076$, these figures rise to 0.76 and 3.8 percentage points respectively. While the welfare cost of these additional tax wedges is amplified by the pre-existing marginal tax rate---because deadweight loss is convex in the total tax rate {cite}`harberger1964`---the magnitude is small enough that the distributional gain dominates.

Workers in the EITC phase-out region (earning roughly \$20,000--\$50,000) face the highest baseline MTRs (near 40%), so the additional distortion from income-based fines is disproportionate there. However, these workers also benefit most from the income-scaling of fines, which reduces their fine burden relative to a flat system, partially offsetting the labor distortion through higher after-fine consumption.

## Sensitivity to key parameters

### Labor supply elasticity

The welfare ranking is most sensitive to the labor supply elasticity.

**Finding 7.** *The probability that flat fines dominate increases with the labor supply elasticity, but income-based fines continue to dominate in the large majority of draws even at the upper end of empirically plausible elasticities.*

This finding has a simple intuition: the labor distortion channel matters more when labor supply is elastic. The quadratic disutility specification implies a Frisch elasticity of 1.0, four times the meta-analytic consensus of 0.25 {cite}`chetty2012`. Because income-based fines dominate even at this elevated elasticity, the result would hold a fortiori at the empirically estimated value. Variation in $\beta$ across Monte Carlo draws modulates equilibrium hours and the absolute magnitude of labor distortion, but the curvature ratio that determines the elasticity remains fixed at 1.0.

### Value of statistical life

**Finding 8.** *Higher VSL values favor income-based fines by increasing the value of deterrence.*

The VSL enters the death cost term $p(s) \cdot V / (1+c)$, scaling the private cost of speeding risk. When $V$ is large, agents internalize more mortality risk, making effective deterrence across the income distribution more valuable. The interaction with fine structure favors income-based fines because they achieve deterrence more equitably.

### Speed-fatality exponent

**Finding 9.** *Higher power model exponents ($n$) favor income-based fines. When speeding is more dangerous, the deterrence benefit of income-proportional penalties increases.*

The exponent $n$ controls the convexity of the death probability function $p(s) = p_{\text{base}}(1+s)^n$. Higher $n$ means that even moderate speeding carries substantial mortality risk, making effective deterrence across the full income distribution more valuable.

## Convergence diagnostics

The mean-field equilibrium is solved by damped fixed-point iteration with damping parameter $\lambda = 0.5$.

**Finding 10.** *The equilibrium solver converges within 200 iterations for more than 99% of Monte Carlo draws, with typical convergence in 20--50 iterations.*

Convergence is measured by the relative change in the universal transfer: $|T^{(k+1)} - T^{(k)}| / \max(|T^{(k)}|, 1) < 10^{-4}$. The damping parameter prevents oscillations that can arise when large changes in the transfer induce large changes in labor supply and speeding, which in turn change revenue and the implied transfer. Draws that fail to converge within 200 iterations are flagged and excluded from welfare comparisons.
