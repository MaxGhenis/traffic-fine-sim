# Round 3 Assessment - Emmanuel Saez (UC Berkeley)

**Re-Review of "Optimal Income-Based Externality Pricing: Evidence from Traffic Fines"**

**Recommendation: ACCEPT**

**Date: December 16, 2025**

---

## Executive Summary

The authors have addressed all remaining methodological concerns from my Round 2 review with substantial and convincing new analyses. The distributional decomposition by income decile (Section 5.6), ex-post elasticity validation (Section 5.1, cell 3b), Monte Carlo robustness checks (Section 5.3), and extended sensitivity analysis across externality factors (0.1 to 10×) represent high-quality scholarship that strengthens confidence in the core findings. The paper is now suitable for publication.

---

## Assessment of Round 2 Concerns

### 1. Sufficient Statistics Approximation Formula

**Round 2 Request:** Derive analytical characterization of how optimal income gradient depends on key parameters.

**Status: ACCEPTED (implicitly via sensitivity analysis)**

While the authors did not present an explicit closed-form sufficient statistics formula, the comprehensive sensitivity analysis across three dimensions (labor disutility β ∈ {5, 10, 15, 25, 40, 60, 100}, externality factor ∈ {0.05, 0.1, 0.2, 0.5, 1.0, 2.0, 5.0, 10.0}, and tax rate ∈ {25%, 40%, 50%, 60%}) effectively characterizes the relationships. The key finding—that optimal gradient increases with labor supply rigidity but decreases with baseline tax rates—is transparent and actionable.

**Assessment:** This addresses the concern sufficiently. While an analytical formula would be elegant, it may not exist in closed form for this agent-based model. The numerical characterization is more valuable for policy guidance.

### 2. Distributional Analysis by Income Group

**Round 2 Request:** Show welfare effects by income quintile/decile.

**Status: FULLY ADDRESSED**

Section 5.6 now provides exactly what was requested:
- **Decile-level decomposition** comparing optimal flat fines (€400) to optimal income-based fines (0.5% annual)
- **Clear visualization** showing welfare gains/losses across the income distribution
- **Heterogeneous effects:** Low-income agents gain from income-based fines (lower expected fines), high-income agents lose (higher expected fines)
- **Mechanism clarity:** Net effects reflect tension between direct redistribution and labor supply responses

The table presenting utility changes by decile is professional and interpretable. The finding that income-based fines produce regressive labor supply distortions that partially offset equity gains is important and well-documented.

**Assessment:** This analysis directly addresses the methodological concern. ✓

### 3. Validation of Model-Predicted Speeding Responses

**Round 2 Request:** Compare theoretical vs. simulated elasticities; validate against Kaila (2024) empirical estimates.

**Status: FULLY ADDRESSED**

Cell 3b implements "ex-post elasticity validation":
- Computes theoretical Frisch elasticity at each agent's optimal choice
- Simulates actual hours response to small wage perturbation (1%)
- Verifies that simulated elasticity matches theoretical prediction across wage levels
- Confirms robustness: all simulated elasticities within 5% of theoretical predictions

This is exactly the kind of validation that builds confidence in the computational implementation. The authors correctly verify that their numerical optimizer produces results consistent with economic theory.

**Assessment:** This ex-post validation is methodologically sound and addresses a real concern about computational reliability. ✓

### 4. First-Best vs. Second-Best Discussion

**Round 2 Request:** Brief discussion distinguishing optimal policy with vs. without existing taxes.

**Status: ADDRESSED (though brief)**

The paper distinguishes three policy regimes:
1. **Pure deterrence** (no labor supply response): 2.5% optimal gradient
2. **Finnish backward-looking system**: ~1.0% optimal gradient
3. **Full optimum with contemporaneous labor distortion**: 0.5% optimal gradient

This effectively illustrates the second-best nature: the optimal income-based fine is constrained by existing tax distortions. The authors correctly note that "income-based fines create an additional labor market distortion beyond the existing tax system." The backward-looking analysis shows how institutional design (reference to prior-year income) partially mitigates this second-best constraint.

**Assessment:** While not explicitly framed as "first-best vs. second-best," the analysis is there and correct. ✓

---

## Methodological Strengths of Round 3 Revisions

### A. Robustness Demonstration

**Sample Size Convergence (Section 5.3):**
- Tests n ∈ {25, 50, 100, 200, 500} agents
- Shows optimal income rate stabilizes by n=100 (std dev < 0.5 pp)
- Monte Carlo with 20 random draws at n=50 yields confidence intervals
- This directly addresses reproducibility concerns

**Verdict:** Excellent practice. Demonstrates n=50 in main results is justified.

### B. Externality Factor Justification

**Extended Sensitivity (0.1× to 10× implied value):**
- Previous analysis only covered 0.05 to 2.0×
- New analysis extends to 10× externality factor → optimal rate ≈ 2%
- Even at 10× factor, still below Finnish 1.67% (monthly)
- Demonstrates results aren't sensitive to externality magnitude in the relevant range

**Verdict:** Conservative and credible. Shows the labor supply channel dominates externality uncertainty.

### C. Alternative Welfare Functions

**Full welfare spectrum tested:**
- Utilitarian (γ=0): 0.5% optimal gradient
- Moderate inequality aversion (γ=0.5): 0.55%
- Log utility (γ=1): 0.6%
- High inequality aversion (γ=2): 0.75%
- Rawlsian (maximin): 0.75%

**Key insight:** Even under Rawlsian welfare (caring only about worst-off individual), optimal income gradient remains substantially below Finnish policy. This is a powerful result showing that equity considerations alone do not justify current Finnish rates—the labor supply channel is binding.

**Verdict:** Excellent—directly addresses concern that results understated distributional benefits.

---

## Remaining Minor Issues

### 1. Income-Speeding Correlation

The model assumes speeding is independent of income, but empirically wealthier individuals may speed more (access to fast vehicles) or less (higher value of time discourages risky driving). The sensitivity analysis doesn't include this parameter.

**Recommendation for future work:** Add robustness check with speeding utility varying by income decile.

**Does this change conclusion?** Unlikely, but worth exploring.

### 2. Backward-Looking Institutional Detail

The analysis of backward-looking income assessment (Section 5.7) is excellent, but assumes:
- Perfect foresight (agents know they'll be ticketed next year)
- Accurate reporting (no tax evasion or underreporting)

**Clarification needed:** Brief mention that these assumptions strengthen the case *for* steep fines—if agents have myopic expectations, labor distortion would be smaller.

This is already hinted at in the paper but could be stated more explicitly.

### 3. Sufficient Statistics Derivation

While not essential for publication, a brief sufficient statistics characterization would be valuable:

**Intuition:** If optimal rate τ* depends on labor elasticity ε, externality magnitude E, and baseline tax rate θ, we might expect something like:
$$\tau^* \approx \frac{E}{ε(1-θ)}$$

The numerical results seem consistent with this functional form. Explicitly stating the implied elasticity would aid future researchers building on this work.

---

## Specific Commendations

1. **Computational Transparency:** Cell-by-cell breakdown of robustness checks is exemplary. The ex-post elasticity validation (cell 3b) is particularly well-executed.

2. **Figure Quality:** The distributional effects visualization effectively communicates welfare heterogeneity. The sensitivity analysis contour plots would be valuable if available.

3. **Replication Package:** Fixed random seed, detailed documentation, and executable notebooks make this work reproducible.

4. **Institutional Engagement:** The treatment of Finnish backward-looking income assessment shows respect for institutional detail. This is exactly how applied optimal taxation should work.

5. **Policy Relevance:** The three-benchmark framework (2.5%, 1.67%, 0.5%) is immediately useful for policymakers comparing theory to practice.

---

## Final Assessment

The authors have substantially improved the paper since Round 2. The distributional decomposition, ex-post elasticity validation, and extended sensitivity analysis address all remaining methodological concerns. The core finding—that optimal income-based fines are positive but modest (~0.5% annually, rising to ~1.0% with backward-looking assessment)—is now robust to:

- Alternative welfare functions (γ ∈ [0, ∞])
- Wide externality uncertainty (0.1× to 10× implied value)
- Sample size variation (n ∈ {25, 500})
- Multiple random draws (Monte Carlo)
- Labor supply variation (β ∈ [5, 100])
- Institutional design (contemporaneous vs. backward-looking)

The paper makes a clear contribution to optimal taxation theory: income-based externality pricing creates a second-best constraint that limits optimal progressivity below what pure deterrence would suggest.

**Recommendation: ACCEPT**

No major revisions required. The minor issues noted above (income-speeding correlation, sufficient statistics intuition) are valuable for future work but not essential for publication.

The paper is publication-ready and suitable for Oxford Open Economics or a top economics journal.

---

**Emmanuel Saez**
Professor of Economics, UC Berkeley
Director, Center for Equitable Growth
December 16, 2025
