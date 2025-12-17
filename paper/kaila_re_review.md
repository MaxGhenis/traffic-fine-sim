# RE-REVIEW: Round 2 Evaluation

**Referee**: Martti Kaila (University of Glasgow)
**Expertise**: Finnish Day-Fine System, Transportation Economics
**Date**: December 16, 2025
**Recommendation**: **Minor Revision**

---

## Summary

The authors have made substantial and commendable revisions that address most of my major concerns from the initial review. The paper now presents a much more accurate characterization of the Finnish day-fine system and explicitly models the backward-looking income assessment that is central to how the system actually operates. These revisions significantly strengthen the empirical grounding and policy relevance of the analysis.

The revised finding—that optimal income gradients range from 0.5% (contemporaneous) to 1.0% (backward-looking), compared to Finland's 1.67%—is far more credible than the original analysis and represents a meaningful contribution to policy debates. The gap between optimal and actual policy has narrowed substantially, and the paper now acknowledges that institutional design features (particularly lagged income assessment) significantly moderate the labor supply channel that is central to the theoretical argument.

## Major Revisions Successfully Addressed

### 1. Backward-Looking Income Assessment (EXCELLENTLY ADDRESSED)

**Original Concern**: The paper failed to model the crucial institutional feature that Finnish day-fines use previous year's tax returns, not current income. This meant the labor supply channel was overstated.

**How Addressed**: Section 5.5 now explicitly models backward-looking versus contemporaneous income assessment. The authors find that:
- Contemporaneous assessment optimal: 0.5%
- Backward-looking assessment optimal: ~1.0%
- This doubling of the optimal rate when using lagged income directly addresses my concern

**Evaluation**: This is an excellent addition that fundamentally changes the paper's policy implications. The authors correctly recognize that "current work decisions don't affect current fine liability" under backward-looking systems, reducing the labor supply distortion. The finding that backward-looking assessment allows for steeper gradients (1.0% vs 0.5%) is both theoretically sound and empirically important.

**Minor suggestion**: The paper could further emphasize that Finland's choice of backward-looking assessment may reflect implicit recognition of the labor supply concerns the authors raise. This would strengthen the narrative that Finnish policymakers have, through institutional design, partly addressed the efficiency-equity tradeoff.

### 2. Threshold Effects (ADEQUATELY ADDRESSED)

**Original Concern**: Day-fines apply only to serious violations (>20 km/h over limit), not marginal speeding.

**How Addressed**: Section 4 now explicitly acknowledges: "Threshold effects: Fines become income-based only for violations exceeding 20 km/h over the limit. Below this threshold, flat fines apply (€200 for cars, €100 for mopeds)."

**Evaluation**: The acknowledgment is accurate and appropriate. While the model itself doesn't incorporate threshold effects into the optimization (which would require a more complex discrete-continuous choice framework), the discussion appropriately notes this institutional reality. This is sufficient for the current paper.

### 3. Basic Deduction Effects (WELL ADDRESSED)

**Original Concern**: The €255 monthly deduction means low-to-middle income violators face near-flat fines.

**How Addressed**: Section 4 now states: "The €255 monthly deduction makes low-income fines near-flat" and incorporates this into the fine function: F(y) = max(200, 0.0167 × max(0, y_monthly - 255) × s)

**Evaluation**: This is accurately characterized. The paper now correctly represents that Finnish day-fines are not purely proportional to income but have a flat component through the deduction mechanism. This institutional nuance is important for understanding the actual progressivity of the system.

### 4. Labor Supply Calibration (SUBSTANTIALLY IMPROVED)

**Original Concern**: Lack of validation that the model generates labor supply elasticities consistent with Finnish empirical estimates.

**How Addressed**: Section 5.1 now provides comprehensive validation, computing Frisch elasticities at different wage and hours combinations. The authors show their calibration (labor_disutility = 25.0) generates elasticities in the range 0.1-0.5, consistent with Finnish/Nordic estimates.

**Evaluation**: This is a significant methodological improvement. The explicit calculation of Frisch elasticities across the income distribution (showing range of ~0.16-0.32) provides much-needed transparency about the behavioral assumptions driving the results. The mean elasticity of ~0.25 is reasonable for Finnish context, though perhaps still at the upper end given Nordic labor market rigidities.

**Remaining concern**: Finnish labor markets are among the most rigid in Europe due to strong unions, generous unemployment insurance, and high labor force participation. An alternative calibration with labor_disutility = 40-50 (yielding lower elasticities) might be more appropriate as a Finnish-specific baseline, with the current calibration presented as a moderate elasticity scenario.

### 5. Distributional Analysis (GREATLY EXPANDED)

**Original Concern**: Insufficient attention to equity-efficiency tradeoff given Finland's explicit equity objectives.

**How Addressed**: Section 5.4 now examines multiple welfare functions including Rawlsian (maximin) and Atkinson inequality-averse specifications with varying inequality aversion parameters (γ = 0, 0.5, 1, 2). The analysis shows that even under extreme inequality aversion (γ = 2), the optimal gradient (~0.75%) remains below Finnish policy (1.67%).

**Evaluation**: This is exactly the kind of analysis needed. The authors demonstrate that their core finding—that Finnish gradients are too steep—is robust to a wide range of social welfare functions. The acknowledgment that "even under high inequality aversion, optimal gradient < Finnish policy" is intellectually honest and strengthens the paper's credibility.

## Minor Concerns Remaining

### 1. Behavioral Response Calibration

The paper calibrates the speeding elasticity to -0.075 based on my 2024 findings, but notes this effect "dissipates after 12 months." The model is static, so this temporal dimension is lost. A brief discussion of how persistent versus temporary behavioral responses affect optimal fine structures would strengthen the analysis.

**Suggestion**: Add a paragraph in Section 6 discussing how the temporary nature of deterrence effects (which I document) might argue for higher fines than the model suggests, since individuals may be forward-looking and discount temporary deterrence.

### 2. Income-Speeding Correlation

The paper assumes speeding utility is independent of income, but some evidence suggests wealthier individuals may have higher value of time and thus speed more. If income-speeding correlation is positive, this would increase the optimal income gradient (since income-based fines would target high-speeding individuals more effectively).

**Suggestion**: Include sensitivity analysis in Section 5.6 examining how optimal gradients vary with assumed correlation between income and speeding propensity. This is particularly important given that the model shows optimal rates are ~0.5-1.0%—a modest positive correlation could push these closer to Finnish policy.

### 3. Enforcement Heterogeneity

Finnish enforcement involves both automated cameras (uniform detection probability) and police stops (potentially income-correlated if vehicle quality signals income). The model assumes uniform enforcement, which may understate the case for income-based fines if wealthy drivers can partially avoid detection.

**Suggestion**: Brief discussion in limitations section acknowledging that heterogeneous enforcement could affect optimal fine structures.

### 4. Administrative Costs

The paper does not discuss the substantial administrative burden of Finland's system: accessing tax records, appeals processes, and means-testing for the €255 deduction. These costs should be mentioned as a practical consideration, even if not formally modeled.

**Suggestion**: Add 2-3 sentences in Section 6 acknowledging these implementation costs.

## Technical Issues

### 1. Externality Calibration (IMPROVED BUT CONCERNS REMAIN)

The revision in Section 5.2 grounds the externality factor in Finnish crash statistics (220 annual fatalities, 30% speeding-related, 40% external victims). However, the authors then use "a conservative externality factor of 0.2, representing approximately 10% of the statistically-implied value."

**Concern**: Why only 10% of the implied value? This seems arbitrary and could substantially affect results. If the true externality is 10× the modeled value, optimal fines could be much higher, potentially making income-based fines more attractive (since the deterrence benefit would dominate labor supply costs).

**Recommendation**: Either (a) justify the 90% discount more carefully (perhaps citing uncertainty in the speeding-crash causality), or (b) present results using the full statistically-implied externality factor as the baseline, with the conservative estimate as a sensitivity check.

### 2. Model-Data Disconnect on Absolute Fine Levels

The model finds optimal flat fines of €700-1000, but Finnish flat fines for minor violations are only €200. This suggests either:
(a) Finnish enforcement is more intensive than modeled
(b) The externality calibration is still too high
(c) Finnish fines are simply suboptimal on absolute level

A brief discussion of this discrepancy would improve transparency.

## Strengths of the Revision

### 1. Intellectual Honesty

The authors have genuinely engaged with the institutional details of the Finnish system rather than treating it as a stylized case. The finding that backward-looking assessment substantially moderates their results shows intellectual honesty—many authors would have downplayed this.

### 2. Comprehensive Sensitivity Analysis

Section 5.6 now examines labor supply elasticity, externality factor, and tax rate variations. The visual presentation (Figure: sensitivity_analysis.png) effectively communicates how results vary with parameters. This transparency allows readers to assess robustness.

### 3. Nuanced Policy Conclusion

The revised conclusion explicitly states that "optimal fines are mildly progressive" rather than flat. This nuance—that some income gradient is justified (0.5-1.0%), but less than current policy (1.67%)—is both theoretically defensible and policy-relevant. The earlier framing could have been misinterpreted as advocating purely flat fines.

### 4. Clear Acknowledgment of Context-Dependence

The paper now emphasizes that optimal fine structures depend on:
- Labor supply elasticity
- Existing tax rates
- Backward vs. contemporaneous income assessment
- Inequality aversion in social welfare function

This context-dependence is crucial for policy advice and represents a mature understanding of the problem.

## Recommendation: MINOR REVISION

The paper has improved dramatically and now makes a solid contribution to both transportation economics and optimal taxation literatures. The remaining issues are relatively minor and can be addressed with modest revisions:

### Required Changes:

1. **Justify or revise externality factor choice** (Section 5.2): Either use the full statistically-implied value as baseline or provide clearer justification for the 90% discount.

2. **Discuss income-speeding correlation** (Section 5.6): Add sensitivity analysis showing how optimal gradients vary if speeding propensity increases with income.

3. **Address model-data disconnect on absolute fine levels** (Section 4 or 6): Briefly explain why model-optimal fines (€700-1000) exceed Finnish flat fines (€200).

### Recommended Changes:

4. Consider alternative calibration with lower labor supply elasticity (labor_disutility = 40-50) as Finnish-specific baseline.

5. Add brief discussion of temporary vs. persistent deterrence effects.

6. Mention administrative costs in limitations section.

7. Discuss enforcement heterogeneity in limitations.

### Publication Merit

With these minor revisions, this paper will make a valuable contribution by:

1. Introducing labor supply considerations to traffic fine policy debates
2. Providing quantitative guidance on optimal income gradients
3. Demonstrating how institutional design (backward-looking assessment) can mitigate efficiency costs
4. Showing that Finnish policy, while perhaps steeper than optimal, is not dramatically so (~40-70% above optimum rather than 3-4× as initial version suggested)

The narrowed gap between optimal (0.5-1.0%) and actual (1.67%) policy is credible and suggests Finnish policymakers may have implicitly balanced competing considerations reasonably well, even if not explicitly modeling labor supply responses.

## Final Assessment

The authors have taken referee feedback seriously and produced a substantially improved paper. The incorporation of backward-looking income assessment is particularly important and changes the paper from a theoretical critique of the Finnish system to a nuanced analysis of institutional design choices. The finding that optimal gradients are positive but modest is policy-relevant and theoretically grounded.

My recommendation is **Minor Revision** contingent on addressing the externality calibration issue and including discussion of income-speeding correlation. These revisions should be straightforward and can likely be completed without additional empirical work.

I commend the authors for their responsiveness to feedback and look forward to seeing the final version.

---

**Martti Kaila**
Senior Lecturer in Economics
Adam Smith Business School
University of Glasgow
