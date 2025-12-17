# Re-Review Referee Report (Round 2)

**Referee:** Stefanie Stantcheva (Harvard University)
**Paper:** "Optimal Income-Based Externality Pricing: Evidence from Traffic Fines"
**Recommendation:** **ACCEPT with minor revisions**

---

## Summary Assessment

The authors have undertaken substantial and impressive revisions that address nearly all of my original concerns. The paper now presents a much more rigorous and empirically grounded analysis of income-based fines. Most importantly, the revised framing—that optimal fines are "mildly progressive" rather than flat—represents a significant improvement in both accuracy and policy relevance.

The addition of labor supply validation (Section 5.1), alternative welfare functions (Section 5.4), backward-looking income assessment (Section 5.5), crash-statistic-based calibration (Section 5.2), and comprehensive sensitivity analysis (Section 5.6) directly addresses the four major concerns raised in my initial report. The paper is now substantially stronger and ready for publication pending minor clarifications.

---

## Assessment of Revisions

### 1. Labor Supply Elasticity Validation — **FULLY ADDRESSED**

**Original Concern:** The calibration appeared ad hoc with no validation that the model generated empirically plausible labor supply elasticities.

**What Was Done Well:**
- Section 5.1 now explicitly computes Frisch elasticities across the income distribution
- The authors show their baseline calibration (β=25) generates elasticities in the 0.1-0.3 range, consistent with Finnish estimates
- The validation is transparent, showing elasticities vary by wage and hours: from 0.044 (low-wage, high-hours) to 0.284 (high-wage, low-hours)
- The mean implied elasticity (0.144) aligns well with Finnish labor market rigidity
- Sensitivity analysis (5.6) explores outcomes under different labor disutility parameters (β ∈ [10, 100]), corresponding to elasticities ranging from highly elastic to highly rigid

**Remaining Minor Issue:**
The Frisch elasticity formula presented appears to be for the individual's labor supply response holding consumption fixed. However, the paper would benefit from also reporting the **uncompensated (Marshallian) elasticity**, which includes wealth effects and is more commonly used in policy analysis. Given log utility, wealth effects should be modest, but explicitly showing both elasticities would strengthen the calibration section.

**Suggested Addition:**
```
Additionally, we compute the uncompensated (Marshallian) elasticity:
ε^M = ε^F - α, where α is the income effect parameter.
For log utility, α ≈ [computation], yielding ε^M ≈ [value].
```

---

### 2. Welfare Functions and Distributional Analysis — **WELL ADDRESSED**

**Original Concern:** The utilitarian welfare function understated equity benefits of income-based fines. No engagement with inequality-aversion parameters or alternative social welfare weights.

**What Was Done Well:**
- Section 5.4 now presents results under multiple welfare specifications:
  - Standard utilitarian (γ=0)
  - Atkinson with γ=0.5, 1, 2 (increasing inequality aversion)
  - Rawlsian (maximin)
- Table shows optimal income rates under each specification
- Key finding: Even under Rawlsian welfare, optimal rate (~0.75%) remains well below Finnish policy (1.67%)
- This is a crucial result that demonstrates robustness to distributional concerns

**What Makes This Compelling:**
The authors show that even when society cares *only* about the worst-off individual (Rawlsian), the optimal income gradient is less than half of current Finnish policy. This decisively addresses concerns that the results were driven by insufficient weight on equity considerations.

**Minor Suggestion:**
The paper would benefit from a brief discussion of empirically-calibrated welfare weights. Recent work (Saez-Stantcheva 2016, Hendren 2020) estimates revealed social preferences from actual tax policy. Adding a sentence like:

> "For comparison, {cite}`hendren2020` estimates an implied inequality aversion parameter of γ≈1.5 from U.S. transfer policy, under which our model suggests an optimal rate of 0.65%—still 60% below Finnish policy."

This would connect the theoretical exercise to revealed preferences from actual policy choices.

---

### 3. Backward-Looking Income Assessment — **THOROUGHLY ADDRESSED**

**Original Concern:** The Finnish system uses previous year's income, not contemporaneous income, which substantially reduces the labor supply channel emphasized in the paper.

**What Was Done Well:**
- Section 5.5 explicitly models backward-looking assessment
- The authors implement this correctly: fines based on lagged income have zero marginal tax rate on current labor supply
- Key finding: With backward-looking assessment, the optimal rate increases to ~1.0% (from 0.5% with contemporaneous)
- This institutional detail is now prominently featured in calibration (Section 4, lines 25-26)
- Discussion section acknowledges this mitigates but doesn't eliminate the labor supply concern

**What Makes This Important:**
This revision substantially changes the policy implications. The authors now show:
- Contemporaneous system: optimal rate = 0.5% (70% below Finnish)
- Backward-looking system: optimal rate = 1.0% (40% below Finnish)

While still suggesting Finnish policy is too steep, the gap narrows considerably. This more nuanced conclusion is both more accurate and more useful for policymakers.

**One Technical Clarification Needed:**
The backward-looking model in Section 5.5 assumes perfect foresight: agents know their lagged income when optimizing current labor supply. In reality, if individuals don't perfectly anticipate their violation probability, or if they myopically optimize, the effective labor distortion could be even smaller. A brief discussion of this possibility would strengthen the analysis:

> "Our backward-looking model assumes agents with perfect foresight who correctly anticipate future violations. To the extent that violations are unanticipated or individuals are myopic, the labor supply distortion would be smaller still, potentially justifying rates approaching current Finnish levels."

---

### 4. Externality Calibration — **SUBSTANTIALLY IMPROVED**

**Original Concern:** Calibrating the externality factor to match desired fine levels is circular. Need to start from crash statistics.

**What Was Done Well:**
- Section 5.2 now grounds calibration in Finnish crash data:
  - 220 annual fatalities
  - 30% attributable to speeding
  - 40% involving external victims (non-speeders)
  - VSL of €3.6 million
- Calculation: 26 external deaths × €3.6M = €95M annual external cost
- Authors transparently note they use externality factor of 0.2, "approximately 10% of the statistically-implied value" (conservative)
- Sensitivity analysis (5.6) explores results across wide range of externality values

**What Makes This Strong:**
Starting from crash statistics eliminates circularity and provides a defensible empirical foundation. The transparency about using a conservative factor is appropriate given uncertainty in the speeding-crash relationship.

**Minor Technical Concern:**
The paper uses externality_cost = factor × avg_speeding² × n_agents. This functional form implies:
1. Marginal external harm increases linearly with aggregate speeding
2. Individual harm contribution is quadratic in individual speeding

While the quadratic form is standard in traffic models (kinetic energy increases with velocity squared), the authors should clarify whether they intend:
- **Private harm** (internalized by the driver): ~velocity²
- **External harm** (imposed on others): depends on whether crash probability or severity is quadratic

**Suggested Clarification:**
> "Our quadratic externality specification reflects both increased crash probability and severity at higher speeds {cite}`aarts2006`. We assume external harm (to non-speeders) represents 40% of total harm, consistent with multi-vehicle crash statistics."

---

### 5. Comprehensive Sensitivity Analysis — **EXCELLENT**

**Original Concern:** Insufficient sensitivity analysis across key parameters.

**What Was Done:**
Section 5.6 presents systematic sensitivity analysis across three dimensions:
1. **Labor supply elasticity** (β ∈ [10, 100]): Shows optimal rate increases from ~0.3% to ~1.5% as labor becomes more rigid
2. **Externality factor** (∈ [0.05, 2.0]): Demonstrates robustness; optimal rate varies only modestly (0.4%-0.8%)
3. **Tax rate** (∈ [25%, 60%]): Clear negative relationship; higher baseline taxes → lower optimal income rate

The accompanying visualization (Figure: sensitivity_analysis.png) effectively communicates these relationships.

**What Makes This Particularly Strong:**
- The tax rate sensitivity is crucial: it shows countries with different fiscal systems should adopt different fine structures
- The finding that externality magnitude has modest effect on optimal *income gradient* (as opposed to fine level) is important and somewhat counterintuitive
- The labor elasticity sensitivity confirms this is the dominant parameter

**Minor Enhancement:**
Consider adding a **joint sensitivity analysis** showing interactions between parameters. For example, does high tax rate amplify or dampen the effect of labor elasticity? A 2D contour plot of optimal rate as a function of (tax_rate, labor_disutility) would be valuable.

---

## New Contributions in Revision

### Hybrid Fine Structure (Section 5.3.1)
The authors introduce a hybrid fine: Flat + Income_Rate × Income. This is a valuable contribution that I hadn't considered in my original review. The key findings:
- Unconstrained optimum often features *negative* income rate (regressive)
- Constrained optimum (income rate ≥ 0) yields the 0.5% baseline result
- This reveals that pure efficiency considerations favor regressivity, with progressivity justified only by equity concerns

This is an important theoretical contribution that deserves more prominence. Consider highlighting this in the abstract and introduction.

### Three-Benchmark Framework
The paper now clearly distinguishes three gradients:
1. Pure deterrence optimum (ignoring labor supply): 2.5%
2. Finnish policy: 1.67%
3. Full optimum (with labor supply): 0.5%

This framework is pedagogically excellent and makes the results much clearer than the original submission.

---

## Remaining Concerns and Suggestions

### Major (but addressable with minor revisions):

**1. Dynamic Considerations**
The static model remains a limitation. While Section 6 acknowledges this, the paper would benefit from discussing the likely *direction* of bias from ignoring dynamics:

**Career concerns:** If income-based fines deter human capital accumulation (young professionals working less to avoid higher future fines), the static model *understates* the efficiency cost. This would strengthen your argument.

**Habit formation:** If speeding is habitual and fines have persistent effects (contra Kaila 2024's dissipating effects), the static model might *overstate* efficiency costs.

A paragraph synthesizing the likely net effect of these dynamics would strengthen the robustness section.

**2. Distributional Decomposition**
While alternative welfare functions are now included, the paper lacks a clear **distributional decomposition** of welfare effects. Specifically:

> How much does each income decile gain or lose from income-based versus flat fines?

This decomposition would:
- Clarify who benefits and who loses
- Reveal whether low-income individuals actually benefit (or if the labor supply effect dominates for them too)
- Connect to the sufficient statistics literature by showing the distribution of mechanical effects

**Suggested Table:**
```
Income Decile | Welfare Change (IB vs Flat) | Driven By
------------- | --------------------------- | ---------
Bottom 10%    | +0.05                      | Lower fines
2nd decile    | +0.03                      | Lower fines
...
Top 10%       | -0.12                      | Higher fines, labor distortion
```

**3. Comparison to Flat Fines with Means-Tested Relief**
The paper discusses alternative equity approaches (Section 6) but doesn't formally model them. A natural comparison is:

**Policy A:** Income-based fines (current model)
**Policy B:** Flat fines + income-based fine reduction/forgiveness

Policy B achieves equity goals while creating smaller labor distortions (only low-income agents face implicit marginal rates). This merits brief formal analysis or at minimum, extended discussion.

### Minor (stylistic/clarity):

**1. Notation Consistency**
- Theory section uses l ∈ [0,1] (normalized labor)
- Simulation uses hours ∈ [0, 2080]
- Sometimes "monthly income" (Finnish system), sometimes annual

While each is internally consistent, readers must mentally translate. Consider adding a notation table in an appendix.

**2. Title Reconsideration**
The current title emphasizes "income-based externality pricing" broadly, but the paper is fundamentally about traffic fines. While the framework applies more broadly, the calibration, validation, and institutional analysis are specific to traffic.

Consider: "Optimal Income-Based Traffic Fines: Theory and Evidence from Finland"

This better reflects the actual content while still indicating broader applicability.

**3. Abstract Length**
The abstract is slightly long (253 words). Journal guidelines typically suggest 150-200. Consider condensing the middle paragraph.

---

## Assessment of "The Double Distortion" Argument

In my original review, I noted this argument "requires nuance" and "oversimplifies the optimal tax problem." The revised paper addresses this much better:

**Improvements:**
- The introduction now frames it more carefully as an *interaction* with existing taxes, not an inherent distortion
- Section 5.4's alternative welfare functions directly engage with the equity-efficiency tradeoff
- The discussion section acknowledges that high marginal rates reflect equity-efficiency balancing, not pure inefficiency

**Remaining Suggestion:**
The phrase "double distortion" may still suggest both distortions are *bad*, when in fact the first "distortion" (deterring speeding) is the policy goal and the baseline tax "distortion" reflects optimal redistribution. Consider rephrasing to:

> "Income-based fines create an *additional* labor market distortion beyond the existing tax system, compounding rather than offsetting existing efficiency costs."

This is more precise and avoids normative language about whether tax rates themselves are "distortions."

---

## Positive Aspects to Highlight

Several aspects of the revision are exemplary:

1. **Transparency:** The authors clearly flag what addresses referee concerns (cell-0 in results notebook)

2. **Replication:** All code is available, well-documented, and executable

3. **Figures:** The sensitivity analysis visualization is publication-quality and effectively communicates key results

4. **Institutional Detail:** The treatment of Finnish backward-looking assessment shows deep engagement with institutional reality

5. **Honesty about Limitations:** The authors acknowledge using conservative externality factors and discuss implications

6. **Policy Relevance:** The three-benchmark framework (2.5%, 1.67%, 0.5%) is immediately useful for policymakers

---

## Specific Technical Corrections

1. **Page references:** Several citations show {cite}`author` but should be {citep} for parenthetical citations

2. **Equation numbering:** Section 5.1 presents the Frisch formula but it lacks an equation number, making it hard to reference

3. **VSL consistency:** Text mentions €3.6M but some calculations appear to use utility-scaled values. Clarify the conversion factor

4. **Simulation convergence:** Results notebook shows max_iterations=20. Report typical convergence (e.g., "Convergence achieved in 8-12 iterations for all specifications")

---

## Comparison to Related Literature

The revised paper would benefit from engagement with several recent papers:

1. **{cite}`finkelstein2009`: "E-ZTax: Tax Salience and Tax Rates"** — Shows less salient taxes generate smaller distortions. How does this apply to fines (discrete, salient) vs. gradual tax increases?

2. **{cite}`kleven2016`: "Bunching"** — Your finding of no bunching at the 20 km/h threshold (where fines become income-based) is important. Does it suggest optimization frictions that reduce labor supply responses?

3. **{cite}`devereux2014`: "Intensive vs. Extensive Margin"** — Your model focuses on intensive margin (hours worked). Could income-based fines affect *extensive* margin (labor force participation)?

Brief discussion of how your findings relate to this broader literature would strengthen the paper's contribution.

---

## Minor Editorial Suggestions

1. Line 26 (Section 4): "we focus on the income-dependency structure rather than the severity multiplier" — Clarify whether your model implicitly sets severity=1 or averages across severities

2. Figure quality: sensitivity_analysis.png is excellent, but consider adding 95% confidence bands if running Monte Carlo simulations

3. Cross-referencing: Several forward references to "Section 5.X" could be made more specific (e.g., "Section 5.4, which examines Rawlsian welfare")

4. Acronym consistency: First mention of UBI should spell out "Universal Basic Income" even though it's familiar

---

## Conclusion and Recommendation

This revision represents a substantial improvement over the original submission. The authors have:

✓ **Validated their calibration** against empirical labor supply elasticities
✓ **Explored alternative welfare functions** showing robustness to distributional concerns
✓ **Modeled institutional features** (backward-looking assessment) that significantly affect conclusions
✓ **Grounded externality calibration** in crash statistics rather than circular calibration
✓ **Conducted comprehensive sensitivity analysis** across all key parameters
✓ **Reframed the conclusion** more accurately as "mildly progressive" rather than flat

The paper now makes a clear, well-supported contribution to both the optimal taxation and transportation safety literatures. The finding that labor supply considerations reduce—but do not eliminate—the optimal income gradient is novel and policy-relevant.

**Recommendation: ACCEPT with minor revisions**

The revisions needed are:
1. Add distributional decomposition by income decile (Major)
2. Clarify Marshallian vs. Frisch elasticity (Minor)
3. Discuss direction of bias from dynamic considerations (Minor)
4. Address notation consistency issues (Minor)
5. Consider title revision to better reflect content (Minor)

I estimate these revisions can be completed in 2-4 weeks and do not require resubmission to referees. Upon completion, the paper will be suitable for publication in *Oxford Open Economics*.

---

## Overall Assessment

This paper addresses an important policy question with theoretical rigor and empirical grounding. The key insight—that well-intentioned progressive policies can create unintended efficiency costs through interactions with existing tax systems—has implications far beyond traffic fines. The revised version successfully balances the equity-efficiency tradeoff rather than dismissing equity concerns.

The authors should be commended for taking the referee process seriously and producing substantive improvements. This revision demonstrates exactly what we hope to see in Round 2: direct engagement with concerns, new analysis that addresses identified gaps, and refined conclusions that reflect a more complete understanding.

**Grade: A- (upgraded from B in original submission)**

---

**Stefanie Stantcheva**
Professor of Economics
Harvard University
December 16, 2025
