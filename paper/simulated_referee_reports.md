# Simulated Referee Reports

## Editor's Summary

We have received three referee reports on your manuscript. While all referees find the research question interesting and the basic insight valuable, they raise several concerns that need to be addressed before the paper can be considered for publication. The main issues relate to: (1) empirical validation, (2) heterogeneity in behavioral responses, and (3) welfare weights. We invite you to revise and resubmit your manuscript addressing these concerns.

---

## Referee Report #1

### Summary

This paper examines whether income-based traffic fines improve welfare compared to flat fines, accounting for labor supply distortions. The key insight—that income-based fines create implicit marginal tax rates affecting labor decisions—is novel and important. The paper is well-written and makes a valuable contribution to both the public economics and transportation policy literatures.

### Major Comments

1. **Empirical Validation**: While the simulation approach is reasonable, the paper would benefit significantly from empirical validation. The authors should:
   - Use data from Finland or Switzerland to test whether high-income individuals reduced labor supply after income-based fines were introduced
   - Examine whether jurisdictions with income-based fines show different patterns of labor force participation
   - At minimum, calibrate the model to match observed speeding and labor patterns in countries with different fine systems

2. **Heterogeneous Risk Preferences**: The model assumes identical utility functions within income groups. This is problematic because:
   - Risk preferences likely correlate with both income and speeding behavior
   - High-income individuals might have different values of time, affecting the speeding utility
   - The optimal fine system could depend on the correlation between income and risk preferences
   
   The authors should extend the model to include heterogeneous risk preferences and examine how this affects their results.

3. **Dynamic Considerations**: The static model misses important dynamic effects:
   - Habit formation in speeding behavior
   - Reputation effects from violations
   - Human capital accumulation effects of reduced labor supply
   
   While a fully dynamic model might be intractable, the authors should discuss these limitations more thoroughly and potentially include a two-period example.

### Minor Comments

- Table 1 should include standard errors or confidence intervals for the optimal parameters
- The sensitivity analysis focuses on labor supply elasticity but should also examine sensitivity to the speeding utility parameter
- The welfare decomposition (Table 3) would be clearer as a percentage of total welfare rather than absolute values
- Some notation is inconsistent between Section 3 and Section 5 (particularly the death probability function)

### Recommendation

Revise and resubmit. The paper makes an important contribution but needs empirical grounding and more complete treatment of heterogeneity.

---

## Referee Report #2

### Summary

The authors present an interesting analysis of income-based traffic fines, highlighting an underappreciated distortion through labor supply effects. The theoretical framework is solid and the computational approach is appropriate. However, I have significant concerns about the welfare analysis and policy conclusions.

### Major Comments

1. **Welfare Weights and Social Preferences**: The paper uses a utilitarian welfare function with equal weights across individuals. This is problematic for several reasons:
   - Most social welfare functions place higher weight on low-income individuals
   - The policy debate around income-based fines explicitly involves equity concerns that utilitarian welfare ignores
   - Results might reverse under alternative welfare functions (e.g., Rawlsian)
   
   The authors must examine how their results change under different social welfare functions, particularly those that incorporate inequality aversion.

2. **Enforcement Endogeneity**: The model takes enforcement probability as exogenous, but this is unrealistic:
   - Police might target enforcement differently under different fine systems
   - Income-based fines might reduce the need for intensive enforcement
   - Political economy factors could lead to different enforcement patterns
   
   The authors should extend the model to include endogenous enforcement or at least discuss this limitation more carefully.

3. **Alternative Policy Instruments**: The paper presents a false dichotomy between flat and income-based fines. Why not consider:
   - Progressive fine structures with brackets (like income taxes)
   - Fines based on vehicle value (proxy for wealth)
   - Point systems combined with income-based financial penalties
   - Time-based penalties (community service) that naturally scale with opportunity cost
   
   A complete analysis should compare a broader range of policy instruments.

### Minor Comments

- The literature review misses several relevant papers on day-fines in criminal justice
- Figure 1 Panel B is misleading—it shows the MTR for speeders but not the distribution of speeders across income
- The calibration to U.S. parameters may not be appropriate given that income-based fines are primarily used in Nordic countries
- The paper should discuss implementation costs and administrative feasibility

### Recommendation

Major revision required. The core insight is valuable but the welfare analysis needs substantial expansion to support the policy conclusions.

---

## Referee Report #3

### Summary

This paper studies an important and timely question with a novel approach. The identification of income-based fines as implicit taxes is clever and the modeling approach is sophisticated. The paper is technically sound and well-executed. However, I have concerns about the behavioral assumptions and external validity.

### Major Comments

1. **Behavioral Assumptions**: The rational agent model may miss important behavioral factors:
   - **Salience**: Income-based fines might be more/less salient than flat fines, affecting deterrence independent of the amount
   - **Mental accounting**: People might treat fines differently from taxes psychologically
   - **Fairness perceptions**: Perceived fairness might affect compliance independent of financial incentives
   - **Hyperbolic discounting**: The immediate cost of fines vs. future labor income might matter
   
   The authors should either incorporate behavioral factors or provide evidence that they don't affect the main conclusions.

2. **Identification and Causality**: The simulation approach, while useful, cannot establish causal effects. The authors should:
   - Be more careful about causal language throughout
   - Validate key behavioral parameters using quasi-experimental evidence
   - Consider a structural estimation approach using data from countries with fine reforms
   - Discuss what variation would be needed to test their key predictions

3. **External Validity and Context**: The results may be highly context-dependent:
   - Labor market institutions differ dramatically across countries
   - Social norms around speeding vary culturally
   - The interaction with other policies (public transit, urban design) matters
   - Income inequality levels affect the relevance of the distortion
   
   The paper needs a more thorough discussion of when and where the results apply.

### Minor Comments

- The abstract should quantify the main finding (e.g., "welfare decreases by X% under income-based fines")
- Section 4 (methodology) is currently missing from the submitted paper
- The computational approach should be validated against analytical solutions for simplified cases
- Code availability and replication materials should be clearly specified
- The conclusion overstates the policy implications given the model's limitations

### Recommendation

Revise and resubmit. The paper makes a novel contribution but needs to address behavioral considerations and be more careful about external validity.

---

## Editor's Decision

Based on these reports, we invite you to revise and resubmit your manuscript. Priority should be given to:

1. **Empirical validation** using data from countries with income-based fines (Referee 1)
2. **Alternative welfare functions** incorporating inequality aversion (Referee 2)  
3. **Behavioral extensions** or evidence that behavioral factors don't alter conclusions (Referee 3)
4. **Heterogeneity** in preferences and its impact on results (Referee 1)
5. **Broader policy alternatives** beyond the flat/income-based dichotomy (Referee 2)

Please also:
- Add the missing Section 4 on methodology
- Provide replication materials and code
- Address the minor comments from all referees
- Include a detailed response letter explaining how you addressed each comment

We look forward to receiving your revised manuscript within 6 months.

---

## Authors' Response Strategy

To address these referee comments, we should:

### Major Revisions
1. Add empirical validation using Finnish traffic violation and tax record data
2. Extend welfare analysis to include Rawlsian and inequality-averse social welfare functions  
3. Include a behavioral extension with salience effects and test robustness
4. Add heterogeneous risk preferences within income groups
5. Compare progressive bracket systems and time-based penalties

### Minor Revisions
1. Add confidence intervals via bootstrap to all tables
2. Include Section 4 with detailed methodology
3. Fix notation consistency
4. Expand sensitivity analyses
5. Upload code to GitHub with full replication instructions

### Response Letter Structure
- Thank editor and referees
- Table summarizing how each comment was addressed
- Point-by-point responses with manuscript page numbers
- Summary of major changes
- Highlight new results that strengthen (or qualify) conclusions