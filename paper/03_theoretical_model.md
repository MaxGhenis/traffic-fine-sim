# Theoretical Model

We develop a model where heterogeneous agents make joint decisions about labor supply and speeding behavior, facing different fine structures and tax systems. The model captures the key trade-off between deterrence benefits and labor supply distortions.

## Agent Optimization Problem

Consider an economy with a continuum of agents indexed by their productivity $w_i$. Each agent chooses labor supply $l_i \in [0,1]$ and speeding intensity $s_i \in [0,1]$ to maximize utility:

$$U_i = u(c_i) + v(s_i) - h(l_i) - p(s_i) \cdot VSL$$

where:
- $c_i$ is consumption (equal to after-tax, after-fine income)
- $u(\cdot)$ is utility from consumption, with $u' > 0$, $u'' < 0$
- $v(\cdot)$ is utility from speeding (time savings, thrill), with $v' > 0$, $v'' < 0$
- $h(\cdot)$ is disutility from labor, with $h' > 0$, $h'' > 0$
- $p(s_i)$ is the probability of death given speeding intensity
- $VSL$ is the value of statistical life

The budget constraint depends on the fine structure. Under a flat fine system:

$$c_i = w_i l_i (1 - \tau) - F \cdot s_i + T$$

Under an income-based fine system:

$$c_i = w_i l_i (1 - \tau - \phi s_i) + T$$

where $\tau$ is the income tax rate, $F$ is the flat fine amount, $\phi$ is the income-based fine rate, and $T$ is a lump-sum transfer.

## First-Order Conditions

### Flat Fine System

The first-order conditions for the flat fine system are:

$$\frac{\partial U_i}{\partial l_i}: u'(c_i) w_i (1 - \tau) = h'(l_i)$$

$$\frac{\partial U_i}{\partial s_i}: v'(s_i) = u'(c_i) F + p'(s_i) \cdot VSL$$

The labor supply decision is independent of speeding behavior, creating a recursive structure that simplifies analysis.

### Income-Based Fine System

Under income-based fines, the first-order conditions become:

$$\frac{\partial U_i}{\partial l_i}: u'(c_i) w_i (1 - \tau - \phi s_i) = h'(l_i)$$

$$\frac{\partial U_i}{\partial s_i}: v'(s_i) = u'(c_i) \phi w_i l_i + p'(s_i) \cdot VSL$$

Crucially, labor supply now depends on speeding choices through the effective tax rate $(1 - \tau - \phi s_i)$, creating the central distortion we analyze.

## Comparative Statics

Taking the total differential of the first-order conditions and applying the implicit function theorem, we can derive the key comparative static results:

**Proposition 1**: Under income-based fines, an increase in the fine rate $\phi$ reduces both speeding and labor supply:

$$\frac{\partial l_i}{\partial \phi} < 0, \quad \frac{\partial s_i}{\partial \phi} < 0$$

**Proposition 2**: The labor supply reduction is larger for high-income individuals:

$$\left|\frac{\partial l_i}{\partial \phi}\right| \text{ increasing in } w_i$$

## Social Welfare

The social planner maximizes a utilitarian social welfare function:

$$W = \int_i U_i \, di$$

subject to the government budget constraint:

$$\int_i \tau w_i l_i \, di + \text{Fine Revenue} = \int_i T \, di$$

## Optimal Fine Design

The optimal fine structure solves:

$$\max_{\{F\} \text{ or } \{\phi\}} W$$

The first-order condition for the flat fine is:

$$\frac{dW}{dF} = \int_i \left[ \frac{\partial U_i}{\partial s_i} \frac{\partial s_i}{\partial F} + \lambda \cdot s_i \right] di = 0$$

where $\lambda$ is the marginal value of public funds.

For income-based fines:

$$\frac{dW}{d\phi} = \int_i \left[ \frac{\partial U_i}{\partial s_i} \frac{\partial s_i}{\partial \phi} + \frac{\partial U_i}{\partial l_i} \frac{\partial l_i}{\partial \phi} + \lambda \cdot (w_i l_i s_i + \phi w_i s_i \frac{\partial l_i}{\partial \phi}) \right] di = 0$$

The additional terms in the income-based case capture the labor supply distortion, which is absent under flat fines.

## Welfare Comparison

The welfare difference between income-based and flat fine systems can be decomposed into three components:

$$\Delta W = \underbrace{\text{Deterrence Gain}}_{\text{Better targeting}} + \underbrace{\text{Labor Supply Loss}}_{\text{Distortion}} + \underbrace{\text{Revenue Effect}}_{\text{Redistribution}}$$

The relative magnitude of these effects depends on:
1. The elasticity of labor supply with respect to the tax rate
2. The distribution of speeding propensity across income levels
3. The social value of redistribution

## Functional Forms for Simulation

For our numerical analysis, we adopt the following functional forms:

- Utility from consumption: $u(c) = \log(1 + c)$
- Utility from speeding: $v(s) = \alpha \log(1 + s)$
- Labor disutility: $h(l) = \beta \frac{l^2}{2}$
- Death probability: $p(s) = \delta \bar{s}$, where $\bar{s}$ is average speeding

These specifications ensure interior solutions while maintaining analytical tractability.