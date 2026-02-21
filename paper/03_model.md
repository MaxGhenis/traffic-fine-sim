---
title: Model
---

# Model

We develop a model of heterogeneous agents who jointly choose labor supply and speeding intensity under alternative fine structures. The environment features a proportional income tax, a fine system (flat or income-based), and a universal transfer funded by tax and fine revenue. We solve for mean-field equilibrium where agents optimize given aggregate outcomes and aggregate outcomes are consistent with individual choices.

## Preferences and technology

Consider an economy with $N$ agents indexed by productivity (wage) $w_i$, drawn from a lognormal distribution. Each agent chooses annual work hours $h_i \in [1, H]$ and speeding intensity $s_i \in [0, 1]$, where $s$ represents the fractional speed above the posted limit and $H$ is the maximum feasible work year.

**Assumption 1.** *Agents maximize:*

$$U_i = \underbrace{\log(1 + c_i)}_{\text{consumption}} + \underbrace{\alpha \log(1 + s_i)}_{\text{speeding benefit}} - \underbrace{\frac{\beta}{2}\left(\frac{h_i}{H}\right)^2}_{\text{labor cost}} - \underbrace{\frac{p(s_i) \cdot V}{1 + c_i}}_{\text{death cost}}$$ (eq:utility)

*where $c_i$ is consumption, $\alpha > 0$ is the weight on speeding utility, $\beta > 0$ governs labor disutility, $V$ is the value of statistical life (VSL), and $p(s_i)$ is the annual death probability.*

Several features merit discussion. Log consumption utility ensures declining marginal utility and positive consumption. The speeding term $\alpha \log(1+s)$ captures time savings and private benefits from higher speeds, with diminishing returns. The quadratic labor cost in normalized hours $h/H$ generates interior solutions and well-behaved comparative statics. The death cost term $p(s) \cdot V / (1+c)$ converts the monetary VSL into utility units by multiplying by the marginal utility of consumption $u'(c) = 1/(1+c)$, ensuring that risk valuation is consistent with the consumption utility function.

**Assumption 2 (Power model).** *The annual death probability follows the {cite}`nilsson2004` power model:*

$$p(s) = p_{\text{base}} \cdot (1 + s)^n, \quad n \approx 4$$ (eq:death-prob)

*where $p_{\text{base}}$ is the baseline death probability and $n$ is the speed-fatality exponent {cite}`nilsson2004`.*

This specification implies that fatality risk is highly convex in speeding intensity. A 10% increase in speed ($s = 0.1$) raises death probability by a factor of $(1.1)^4 \approx 1.46$, while a 50% increase ($s = 0.5$) raises it by $(1.5)^4 \approx 5.06$.

## Budget constraint and fine structures

Agent $i$ earns gross income $y_i = w_i h_i$, pays income tax, pays a fine that depends on the fine system, and receives a uniform transfer $T$. In the budget constraints below, $\tau$ denotes the agent-specific tax rate $\text{MTR}_i$. We use each agent's marginal tax rate from the CPS/PolicyEngine data as a linearization of the progressive tax schedule around the observed income level. This is a standard approximation in the public finance simulation literature {cite}`saez2001`: the marginal rate governs the agent's labor supply response at the margin, which is the relevant object for the welfare comparison between fine systems. Because both fine systems use the same linearized tax treatment, any level bias from this approximation is symmetric and cancels in the welfare *difference* $\Delta W = W_{\text{IB}} - W_{\text{flat}}$, which is our primary object of interest. We discuss the limitations of this approximation in Section 6. We consider two fine structures.

**Flat fine.** Under a flat fine $F$, the penalty is $F \cdot s_i$---proportional to speeding intensity but independent of income:

$$c_i = w_i h_i (1 - \tau) - F s_i + T$$ (eq:budget-flat)

**Income-based fine.** Under an income-based fine with rate $\phi$, the penalty is $\phi \cdot y_i \cdot s_i$---proportional to both income and speeding:

$$c_i = w_i h_i (1 - \tau - \phi s_i) + T$$ (eq:budget-ib)

The crucial difference is visible in {eq}`eq:budget-ib`: the income-based fine enters the budget constraint multiplicatively with income, creating an effective marginal tax rate of $\tau + \phi s_i$ that varies with speeding behavior.

## First-order conditions

### Flat fine system

Taking derivatives of {eq}`eq:utility` subject to {eq}`eq:budget-flat`:

$$\frac{\partial U_i}{\partial h_i} = 0: \quad \frac{w_i(1-\tau)}{1+c_i} + \frac{p(s_i) V w_i(1-\tau)}{(1+c_i)^2} = \frac{\beta h_i}{H^2}$$ (eq:foc-h-flat)

$$\frac{\partial U_i}{\partial s_i} = 0: \quad \frac{\alpha}{1+s_i} = \frac{F}{1+c_i} + \frac{F \cdot p(s_i) V}{(1+c_i)^2} + \frac{p'(s_i) V}{1+c_i}$$ (eq:foc-s-flat)

Under flat fines, the labor supply FOC {eq}`eq:foc-h-flat` depends on speeding only through $p(s_i)$ and $c_i$, and the speeding FOC {eq}`eq:foc-s-flat` depends on labor only through $c_i$. Labor and speeding decisions interact through consumption but the fine itself does not create a direct coupling.

### Income-based fine system

Under the income-based system with budget constraint {eq}`eq:budget-ib`:

$$\frac{\partial U_i}{\partial h_i} = 0: \quad \frac{w_i(1-\tau - \phi s_i)}{1+c_i} + \frac{p(s_i) V w_i(1-\tau - \phi s_i)}{(1+c_i)^2} = \frac{\beta h_i}{H^2}$$ (eq:foc-h-ib)

$$\frac{\partial U_i}{\partial s_i} = 0: \quad \frac{\alpha}{1+s_i} = \frac{\phi w_i h_i}{1+c_i} + \frac{\phi w_i h_i \cdot p(s_i) V}{(1+c_i)^2} + \frac{p'(s_i) V}{1+c_i}$$ (eq:foc-s-ib)

The key difference is in {eq}`eq:foc-h-ib`: the marginal return to labor is reduced from $w_i(1-\tau)$ to $w_i(1-\tau - \phi s_i)$. Agents who speed more face a higher effective tax rate and supply less labor, all else equal. Similarly, {eq}`eq:foc-s-ib` shows that the marginal cost of speeding now depends on income $w_i h_i$, creating the income-based deterrence.

**Proposition 1.** *Under income-based fines, the effective marginal tax rate on labor income is $\tau + \phi s_i$, which is increasing in both the fine rate $\phi$ and the agent's speeding intensity $s_i$.*

**Proposition 2.** *An increase in the fine rate $\phi$ reduces both speeding and labor supply:*

$$\frac{\partial s_i}{\partial \phi} < 0, \quad \frac{\partial h_i}{\partial \phi} < 0$$

*The first effect is the intended deterrence; the second is the unintended labor distortion.*

*Proof sketch.* From {eq}`eq:foc-s-ib`, the marginal cost of speeding includes $\phi w_i h_i / (1+c_i)$, which is increasing in $\phi$, so the equilibrium $s_i$ falls. From {eq}`eq:foc-h-ib`, the marginal return to labor is $w_i(1 - \tau - \phi s_i)/(1+c_i)$, which is decreasing in $\phi$ (holding $s_i$ fixed). While the reduction in $s_i$ partially offsets this by raising the net-of-fine return, the direct effect dominates when $\phi$ is small relative to $1-\tau$, which holds at empirically relevant fine rates. Numerical verification confirms this for all parameter draws in our Monte Carlo analysis.

**Proposition 3.** *The labor supply reduction from income-based fines is increasing in productivity $w_i$, provided that hours $h_i$ are increasing in $w_i$.*

*Proof sketch.* The labor distortion arises from the additional effective tax $\phi s_i$ on labor income $w_i h_i$. From {eq}`eq:foc-h-ib`, the wedge between the marginal return to labor and the marginal disutility is proportional to $\phi s_i w_i / (1+c_i)$. When $w_i$ is higher, the absolute reduction in labor income from any given percentage reduction in hours is larger, and the deadweight loss---which is proportional to $w_i^2$ in a linear approximation---is therefore increasing in $w_i$. This holds when hours are interior and increasing in wages, which is the case in our simulations for all agents.

## Mean-field equilibrium

Fine and tax revenue funds a uniform transfer. The government budget constraint is:

$$T = \frac{1}{N} \left[ \sum_{i=1}^{N} \tau w_i h_i + \sum_{i=1}^{N} f_i(w_i h_i, s_i) \right]$$ (eq:budget-govt)

where $f_i(\cdot)$ is the fine paid by agent $i$.

**Definition 1 (Mean-field equilibrium).** *A mean-field equilibrium is a collection of choices $\{(h_i^*, s_i^*)\}_{i=1}^N$ and a transfer $T^*$ such that:*

1. *Each agent optimizes: $(h_i^*, s_i^*) = \arg\max_{h,s} U_i(h, s; T^*, w_i)$ for all $i$.*
2. *The government budget balances: $T^*$ satisfies {eq}`eq:budget-govt` given $\{(h_i^*, s_i^*)\}$.*

We solve for equilibrium using damped fixed-point iteration:

1. Initialize $T^{(0)} = 0$.
2. Given $T^{(k)}$, each agent solves their optimization problem via L-BFGS-B.
3. Compute the implied transfer $\hat{T}^{(k+1)}$ from {eq}`eq:budget-govt`.
4. Update: $T^{(k+1)} = \lambda \hat{T}^{(k+1)} + (1-\lambda) T^{(k)}$, with damping $\lambda \in (0,1]$.
5. Iterate until $|T^{(k+1)} - T^{(k)}| / \max(|T^{(k)}|, 1) < \varepsilon$.

The damping parameter $\lambda$ (set to 0.5 in our baseline) prevents oscillations that arise because agents' labor supply and speeding responses to the transfer create feedback loops.

## Social welfare

We evaluate outcomes under three social welfare functions:

$$W_{\text{util}} = \sum_{i=1}^N U_i \quad \text{(utilitarian)}$$ (eq:welfare-util)

$$W_{\text{rawls}} = \min_i U_i \quad \text{(Rawlsian)}$$ (eq:welfare-rawls)

$$W_{\text{atk}}(\varepsilon) = N \left[ \frac{1}{N} \sum_{i=1}^N U_i^{1-\varepsilon} \right]^{1/(1-\varepsilon)} \quad \text{(Atkinson, } \varepsilon \geq 0\text{)}$$ (eq:welfare-atk)

The Atkinson family nests the utilitarian ($\varepsilon = 0$) and Rawlsian ($\varepsilon \to \infty$) criteria as special cases, allowing us to trace how social preferences over inequality affect the welfare ranking of fine systems.

## Welfare decomposition

To understand the sources of welfare differences, we decompose $\Delta W = W_{\text{IB}} - W_{\text{flat}}$ into three channels:

$$\Delta W = \underbrace{\Delta W_{\text{deterrence}}}_{\text{safety gain}} + \underbrace{\Delta W_{\text{labor}}}_{\text{distortion loss}} + \underbrace{\Delta W_{\text{revenue}}}_{\text{fiscal effect}}$$ (eq:decomposition)

The deterrence gain captures welfare improvements from more effectively targeted penalties across the income distribution. The labor distortion loss captures the efficiency cost of the implicit tax on earnings. The revenue effect captures differences in equilibrium transfers arising from different revenue levels under the two systems.
