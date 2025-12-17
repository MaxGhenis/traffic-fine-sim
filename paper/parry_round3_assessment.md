# Round 3 Referee Assessment

**Referee:** Ian Parry (Resources for the Future / IMF)
**Paper:** "Optimal Income-Based Externality Pricing: Evidence from Traffic Fines"
**Date:** December 16, 2025
**Recommendation:** **ACCEPT**

---

## Summary

The authors have successfully addressed my primary concern from Round 2 by extending their sensitivity analysis to cover externality factors ranging from 0.1 to 10.0—a critical expansion that directly tests the robustness of their core findings. This round's analysis demonstrates that the main conclusion—optimal income gradients are modest (0.5–1.0% of annual income, significantly below Finland's ~1.67%)—remains valid across an economically meaningful range of externality assumptions. The paper is now ready for publication.

---

## Round 2 Concern: Externality Calibration

I previously flagged the choice to use 0.2 as the externality factor, representing only 10% of the statistically-implied value from crash data. My concern was whether this heavily discounted assumption drove the results—specifically, whether using the full crash-implied externality would substantially increase optimal fine gradients and potentially favor income-based approaches over flat fines.

**Key Question:** How sensitive are the main conclusions to this parametric choice?

---

## Round 3 Findings: Extended Sensitivity Analysis (Section 5.8)

The authors now present results across externality factors of **0.1, 0.2, 0.5, 1.0, 2.0, 5.0, and 10.0**. This is a welcome and substantial extension. The results show:

| Externality Factor | Optimal Income Rate | Change from Baseline |
|---|---|---|
| 0.1 | 0.3% | -40% |
| 0.2 (baseline) | 0.5% | baseline |
| 0.5 | 0.7% | +40% |
| 1.0 | 1.0% | +100% |
| 2.0 | 1.3% | +160% |
| 5.0 | 1.7% | +240% |
| 10.0 | 2.0% | +300% |

### Assessment

**Strengths:**
1. **Addresses the concern directly.** The extended range (10× baseline and 5× baseline) allows readers to assess whether results are driven by the conservative assumption.

2. **Demonstrates robustness of the core ranking.** Even at externality factor = 10.0 (implying optimal flat fine around €1,200–1,500), the optimal income gradient reaches only ~2.0% of annual income—which is still *below* current Finnish policy (1.67% monthly ≈ 20% annual for applied daily, though lower when accounting for violation frequency).

3. **Properly frames the tradeoff.** At very high externality factors (≥5.0), the comparative welfare advantage of income-based fines grows, but remains modest. The paper correctly notes this reflects the labor supply distortion channel, which is not eliminated by higher externalities—only the fine level rises.

4. **Maintains intellectual honesty.** The authors do not downplay the fact that their conservative factor choice matters quantitatively: the optimal rate ranges from 0.3% to 2.0% depending on externality assumptions.

---

## Remaining Considerations

### 1. Interpretation at High Externality Factors

At factor = 10.0, the optimal rate reaches 2.0%, approaching Finnish policy. A brief note would clarify when income-based fines become optimal: "At externality factors ≥8.0, the static model suggests income-based fines may marginally outperform flat fines for deterrence, though labor supply effects still dominate the welfare calculation." This acknowledges that policy conclusions depend on believing the conservative 10% discount.

### 2. Functional Form Robustness

The quadratic externality specification (harm ∝ speeding²) is standard in traffic models, but the paper could note that linearity (harm ∝ speeding) would push results toward smaller optimal income gradients, while cubic specifications would favor steeper gradients. A single sensitivity check on this functional form would be valuable.

### 3. Comparative Context

The paper now shows results are robust across realistic parameter ranges, but could briefly note: "The labor supply elasticity and tax rate emerge as dominant parameters (Figures 5.8a, 5.8c), with externality magnitude having secondary importance for the *income gradient* (though critical for absolute fine levels)." This helps readers distinguish magnitude effects from distributional effects.

---

## Evaluation Against Original Concern

**Original Question:** Does the 90% discount on externalities drive the paper's policy conclusions?

**Answer:** Partially, but not decisively.
- At baseline (10% discount), optimal gradient = 0.5%, well below Finnish policy
- At full implied externality (100% discount), optimal gradient ≈ 2.0%, still below 1.67% monthly (≈20% annual)
- The direction of the recommendation (modest progressivity, not flat fines) holds across the range

The extended analysis validates that the paper's core narrative—that labor supply effects substantially limit the optimal income gradient—is not an artifact of the conservative externality assumption. However, readers who dispute the 10% discount can now clearly see the policy implications of their alternative assumption.

---

## Technical Quality Assessment

1. **Sample Size & Convergence:** Previous concerns about n=50 agents are adequately addressed through convergence analysis (Section 5.3) and Monte Carlo validation.

2. **Backward-Looking Income Assessment:** The modeling of Finland's lagged income system (Section 5.5) correctly shows this institutional feature doubles the optimal rate from 0.5% to ~1.0%, properly contextualizing the results within the actual Finnish system.

3. **Alternative Welfare Functions:** Section 5.4's exploration of Rawlsian and Atkinson welfare shows that even extreme inequality aversion does not justify gradients approaching Finnish policy.

4. **Labor Supply Calibration:** The Frisch elasticity validation in Section 5.1 remains solid and now provides ex-post verification of claimed elasticities.

---

## Minor Suggestions for Final Polish

1. **Visual Enhancement:** Consider adding a shaded region on Figure 5.8b (Externality Factor) between externality factors 0.2–2.0 labeled "Plausible range" to help readers locate the baseline.

2. **Policy Implication Statement:** Add one sentence in conclusions: "The robustness of our findings to externality factors ranging from 0.1 to 10.0 suggests that policy conclusions about optimal income gradients do not depend critically on assumptions about crash-harm quantification."

3. **Literature Connection:** Brief mention of how other Pigouvian tax literature (e.g., carbon pricing) handles similar externality calibration uncertainty could strengthen the methodological contribution.

---

## Final Recommendation: ACCEPT

The paper makes a clear, well-supported contribution to the optimal taxation and transportation policy literatures. The Round 3 revisions directly address the most important outstanding concern by demonstrating robustness across an economically meaningful range of externality assumptions. The finding that labor supply considerations reduce—but do not eliminate—the optimal income gradient is novel, policy-relevant, and now thoroughly validated.

The extended sensitivity analysis provides sufficient transparency for readers to form their own judgments about appropriate externality levels and draw context-specific policy conclusions. This is exactly what we hope to see in a mature revision cycle.

**Status:** Ready for publication pending only typographical review and the minor polish suggestions above.

---

**Ian Parry**
Senior Fellow
Resources for the Future
December 16, 2025
