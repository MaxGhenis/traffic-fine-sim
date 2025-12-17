# Round 4 Assessment: Critical Finding Requires Major Revision

**Referee:** Stefanie Stantcheva (Harvard University)
**Paper:** "Optimal Income-Based Externality Pricing: Evidence from Traffic Fines"
**Date:** December 16, 2025
**Assessment:** MAJOR REVISIONS REQUIRED

---

## Executive Summary

The authors' discovery that switching from grid search to continuous optimization (scipy.optimize.minimize) fundamentally changes the optimal fine structure from "mildly progressive" (0.5% income gradient) to "essentially flat" (€702 + 0.002% income) represents a critical finding that demands substantial revision. The unconstrained optimum showing *negative* income gradients (€1435 - 13.55% income, i.e., regressive) is theoretically important but requires careful interpretation. I recommend major revisions rather than rejection, but the paper's central narrative must shift.

---

## Critical Issues

### 1. **Grid Search Artifact vs. Genuine Solution (CREDIBILITY CONCERN)**

The most pressing question: is the previous 0.5% result a genuine local optimum that continuous optimization missed, or purely a grid resolution artifact?

**What suggests grid artifact:** If the constrained optimum truly sits at 0.002% income rate, this would require extraordinary fine-tuning to land exactly there via coarse grid search. The fact that continuous optimization found €702 + 0.002% suggests this represents a *boundary* of the feasible region rather than an interior solution.

**What I need to verify:**
- Report the gradient of the welfare function at the 0.5% point. If it's near zero, 0.5% may be a local optimum that continuous optimization converges to differently based on initial conditions.
- Compare welfare levels: Does €702 flat + 0.002% income (continuous) actually yield *higher* welfare than the 0.5% solution? If the welfare difference is trivial (< 0.1%), the grid finding might be robust.
- Run continuous optimization with multiple initializations. If different starting points converge to different solutions, you've found multiple local optima.

**Recommendation:** Before revising the paper, confirm this is not a numerical artifact by reporting conditioning numbers and checking solution stability.

---

### 2. **The Unconstrained Regressive Optimum (THEORETICALLY IMPORTANT)**

The unconstrained finding (€1435 - 13.55% income) is genuinely interesting and deserves prominent discussion. This reveals that *pure efficiency considerations favor regressivity*.

**Why this matters:** Under the Tinbergen principle, if policymakers want to optimize both deterrence *and* equity, they need two instruments (fine level + progressivity). But if equity concerns are handled through the tax-transfer system, then fines should purely optimize deterrence—which, in your model, means regressive fines to avoid labor supply distortions.

**Critical interpretation:** The regressive result doesn't mean "regressive fines are good." Rather, it means efficiency alone justifies regressivity *if* we ignore distributional concerns. This supports your paper's core insight: progressivity in fines requires an explicit equity rationale, not just deterrence.

**Suggested framing:** "Our unconstrained optimization reveals that pure efficiency considerations favor regressive fines by approximately 13.55% of income, compounding the existing tax burden on high earners. This counterintuitive result highlights the tension between deterrence objectives and labor supply efficiency. Progressivity becomes justified only by distributional considerations—a finding with implications for the broader debate on whether regulatory instruments should serve multiple policy objectives."

---

### 3. **Constrained Optimum at Boundary (IMPLICATIONS)**

That the constrained optimum (income rate ≥ 0) lands at precisely 0.002% suggests you're at a *boundary solution*. This has important implications:

**If true:** The constraint income rate ≥ 0 is *binding* at the optimum. This means welfare increases as income gradients become more regressive, stopped only by the normative constraint. Your paper should explicitly acknowledge this rather than presenting 0.002% as a "balanced" optimum.

**Revised narrative:** "When we restrict income gradients to non-negative values—reflecting distributional concerns—the optimal policy sits at the boundary: essentially flat fines. This boundary solution indicates that even minimal progressivity comes at a welfare cost. Policymakers choosing income-based fines must do so *despite* efficiency costs, justified by explicit equity preferences."

This is actually stronger than the "mildly progressive" framing because it's more honest about the trade-off.

---

## Does This Strengthen or Weaken the Contribution?

**Strengthen:**
- The regressive unconstrained optimum is a genuine theoretical contribution that adds nuance to optimal taxation
- The boundary solution clarifies that progressivity requires explicit equity weight, not efficiency
- Continuous optimization demonstrates rigor and transparency about numerical methods
- The result is more actionable: "flat fines are optimal" is clearer policy guidance than "0.5% is optimal"

**Weaken:**
- The previous Round 3 conclusion ("mildly progressive, 0.5% optimal") is invalidated
- Stantcheva's Round 3 praise for "nuanced conclusion" becomes outdated
- Risk of appearing to change conclusions for rhetorical advantage rather than methodological clarity
- Requires explaining why grid search was used initially—this may raise questions about rigor

---

## Recommended Revisions

**Major additions:**
1. **Section 5.7 - Numerical Methods:** Explain switch from grid search → continuous optimization. Report convergence diagnostics and multiple initialization tests.

2. **Reframe Section 5.3.1 (Hybrid Structures):** Prominently feature the unconstrained regressive result as a key finding, not a subsidiary robustness check.

3. **Revise Abstract & Introduction:** Replace "mildly progressive (0.5%)" with "essentially flat fines optimal; unconstrained optimum is regressive."

4. **New Table:** Compare welfare levels across three scenarios:
   - Unconstrained optimum: €1435 - 13.55% income, welfare = X
   - Constrained optimum: €702 + 0.002% income, welfare = X - ε
   - Finnish policy: 1.67% income, welfare = X - δ

   If ε and δ are small, acknowledge solutions are empirically similar.

5. **Discussion Box:** Explain boundary solution interpretation for non-technical readers.

---

## Credibility Assessment

**Is the finding credible?** Conditionally yes, but:
- ✓ Continuous optimization is methodologically superior to grid search
- ✓ Regressive unconstrained optimum aligns with theoretical predictions about labor supply distortions
- ✗ Need confirmation this isn't a numerical artifact (multiple initializations, gradient checks)
- ✗ Need comparison of welfare levels across solutions to assess practical importance

**Suggested presentation:** "Our switch to continuous optimization reveals the constrained optimum sits at the boundary (≤0.002% income gradient). The unconstrained optimum is substantially regressive (−13.55%), demonstrating that pure efficiency considerations favor regressivity. These findings suggest that any progressivity in fines requires explicit distributional objectives."

---

## Final Assessment

This finding does **not** weaken the paper—it strengthens it by being more precise about what efficiency implies. The key insight remains valid: income-based fines distort labor supply in ways flat fines do not. The contribution is sharpened from "progressivity should be modest" to "absent equity concerns, fines should be flat or regressive."

**Recommendation: ACCEPT WITH MAJOR REVISIONS**

Revise the narrative to embrace the continuous optimization finding as a methodological advance and substantive insight. The unconstrained regressive result is genuinely interesting and deserves prominence. Confirm the result is not a numerical artifact. Upon revision, this will be a stronger paper.

**Timeline:** ~4 weeks for revisions; no re-review needed if changes are transparent about methods.

---

**Stefanie Stantcheva**
Harvard University
