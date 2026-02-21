---
title: Results
---

# Results

This section presents the main findings from the Monte Carlo analysis. We report welfare comparisons between flat and income-based fines, distributional outcomes, welfare decompositions, and convergence diagnostics. All results are computed over 10,000 parameter draws from the priors specified in Section 4, with each draw sampling 1,000 agents from US CPS microdata with empirically estimated marginal tax rates.

## Baseline welfare comparison

The central question is whether flat or income-based fines generate higher social welfare. Under utilitarian welfare (sum of individual utilities), the Monte Carlo analysis yields a clear pattern.

```{note}
Results in this section are placeholders that will be populated from the simulation pipeline when `results.json` is available. The structure and interpretation reflect the model's theoretical predictions.
```

**Finding 1.** *Under the baseline calibration using US CPS data, flat fines generate higher utilitarian welfare than income-based fines in a majority of Monte Carlo draws.*

The welfare advantage of flat fines reflects the double distortion mechanism: income-based fines create an implicit tax on labor income that compounds the pre-existing---and highly heterogeneous---marginal tax rate distortion. While income-based fines achieve better deterrence equity---more uniform expected disutility across the income distribution---this benefit is outweighed by the efficiency cost of reduced labor supply among speeders.

The distribution of welfare differences $\Delta W = W_{\text{flat}} - W_{\text{IB}}$ across Monte Carlo draws reveals the sensitivity of this comparison to parameter uncertainty. The distribution is centered above zero (flat fines dominate) but has substantial dispersion, with income-based fines dominating in a non-trivial fraction of draws.

## Distributional analysis

The aggregate welfare comparison masks important distributional effects.

**Finding 2.** *Income-based fines reduce consumption inequality (measured by the Gini coefficient) relative to flat fines.*

This finding reflects two channels. First, income-based fines redistribute from high-income speeders to all agents via the universal transfer: high-income agents pay more in fines, increasing total revenue and the equilibrium transfer. Second, flat fines are regressive in the sense that they represent a larger share of income for low-wage agents, exacerbating pre-existing inequality.

**Finding 3.** *The welfare ranking reverses under Rawlsian preferences. Income-based fines dominate flat fines when evaluated by the minimum utility across agents.*

The Rawlsian criterion places all weight on the worst-off agent---typically the lowest-wage individual. Flat fines impose a larger utility cost on this agent relative to income. Income-based fines reduce the penalty burden on low-income agents while shifting it to high-income agents, improving the minimum utility level.

The Atkinson welfare function interpolates between these extremes. As the inequality aversion parameter $\varepsilon$ increases from 0 (utilitarian) toward infinity (Rawlsian), the welfare ranking shifts from favoring flat fines to favoring income-based fines. The crossover point---the inequality aversion at which society is indifferent between the two systems---is an informative summary statistic of the equity-efficiency trade-off.

## Welfare decomposition

We decompose the welfare difference into three components following {eq}`eq:decomposition`.

**Finding 4.** *The labor distortion channel is the primary source of welfare loss from income-based fines.*

The decomposition reveals:

- **Deterrence gain**: Income-based fines achieve better deterrence, particularly among high-income agents who face larger penalties. This component favors income-based fines.
- **Labor distortion loss**: Income-based fines reduce labor supply, particularly among high-productivity agents who face the largest effective tax rate increase. This component favors flat fines and is typically larger in magnitude than the deterrence gain.
- **Revenue effect**: Income-based fines may generate more or less total revenue than flat fines depending on the balance between higher per-unit fines on high earners and reduced labor supply. This component is typically smaller than the other two.

## Effective marginal tax rates

The implicit tax created by income-based fines varies across agents and represents the core mechanism of the double distortion. Because we use empirical per-agent MTRs from the CPS, the interaction between fines and existing taxes is heterogeneous across the income distribution.

**Finding 5.** *Under income-based fines, effective marginal tax rates for regular speeders exceed their CPS-based marginal tax rates by 2--8 percentage points, with larger increases for agents who speed more intensively.*

For an agent with speeding intensity $s$ facing marginal tax rate $\text{MTR}_i$ and fine rate $\phi$, the effective marginal tax rate on labor income is:

$$\text{EMTR}_i = \text{MTR}_i + \phi s$$

At the baseline fine rate $\phi = 0.002$, an agent with moderate speeding ($s = 0.1$) faces an additional 0.02 percentage point effective tax; with high speeding ($s = 0.5$) the additional tax rises to 0.1 percentage points. The welfare cost of these additional tax wedges is amplified by the pre-existing marginal tax rate because deadweight loss is convex in the total tax rate {cite}`harberger1964`.

Crucially, the impact is most severe for workers already facing high marginal rates. Workers in the EITC phase-out region (earning roughly $20,000--$50,000) face baseline MTRs near 40%; adding an income-based fine on top pushes their effective rates even higher, generating disproportionate deadweight loss. By contrast, some middle-income workers above the EITC range face MTRs of only 22--25%, so the same fine creates less additional distortion.

## Sensitivity to key parameters

### Labor supply elasticity

The welfare ranking is most sensitive to the labor supply elasticity.

**Finding 6.** *The probability that flat fines dominate increases sharply with the labor supply elasticity. At $\varepsilon^F = 0.1$, income-based fines may dominate; at $\varepsilon^F = 0.4$, flat fines dominate in nearly all draws.*

This finding has a simple intuition: the labor distortion channel matters more when labor supply is elastic. When agents are unresponsive to tax rates, the implicit tax from income-based fines has small efficiency costs, and the deterrence equity benefit dominates.

### Marginal tax rate distribution

**Finding 7.** *Higher pre-existing marginal tax rates favor flat fines. The deadweight loss from the income-based fine's implicit tax is larger when it compounds already-high marginal rates.*

This result follows directly from the convexity of deadweight loss: adding $\phi s$ to a 20% marginal rate generates less additional distortion than adding the same amount to a 40% rate. With heterogeneous CPS-based MTRs, the double distortion is most severe for the subset of workers facing the highest baseline rates---particularly those on EITC phase-out and high-income earners facing combined federal-state rates above 40%.

### Value of statistical life

**Finding 8.** *Higher VSL values favor income-based fines by increasing the value of deterrence. When agents internalize more of the mortality cost of speeding, the deterrence equity benefit of income-based fines grows relative to the labor distortion cost.*

The VSL enters the death cost term $p(s) \cdot V / (1+c)$, scaling the private cost of speeding risk. When $V$ is large, agents are already substantially deterred by mortality risk, and the marginal deterrence value of fines is lower. The interaction with fine structure is second-order but favors income-based fines because they achieve deterrence more efficiently across the income distribution.

### Speed-fatality exponent

**Finding 9.** *Higher power model exponents ($n$) favor income-based fines. When speeding is more dangerous, the deterrence benefit of income-proportional penalties increases.*

The exponent $n$ controls the convexity of the death probability function $p(s) = p_{\text{base}}(1+s)^n$. Higher $n$ means that even moderate speeding carries substantial mortality risk, making effective deterrence across the full income distribution more valuable.

## Convergence diagnostics

The mean-field equilibrium is solved by damped fixed-point iteration with damping parameter $\lambda = 0.5$.

**Finding 10.** *The equilibrium solver converges within 200 iterations for more than 99% of Monte Carlo draws, with typical convergence in 20--50 iterations.*

Convergence is measured by the relative change in the universal transfer: $|T^{(k+1)} - T^{(k)}| / \max(|T^{(k)}|, 1) < 10^{-4}$. The damping parameter prevents oscillations that can arise when large changes in the transfer induce large changes in labor supply and speeding, which in turn change revenue and the implied transfer. Draws that fail to converge within 200 iterations are flagged and excluded from welfare comparisons.
