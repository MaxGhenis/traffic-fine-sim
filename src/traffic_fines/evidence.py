"""Evidence sources for the traffic fines simulation model."""

from dataclasses import dataclass
from typing import Optional


@dataclass
class EffectSize:
    metric: str  # "elasticity", "relative_risk", "coefficient", "ratio", "exponent"
    point_estimate: float
    ci_lower: Optional[float] = None
    ci_upper: Optional[float] = None
    ci_level: float = 0.95


@dataclass
class Source:
    id: str
    citation: str
    url: str
    study_type: str  # "meta_analysis", "rct", "quasi_experimental", "theoretical", "administrative", "survey", "review"
    key_finding: str
    doi: Optional[str] = None
    database: Optional[str] = None
    effect_size: Optional[EffectSize] = None
    sample_size: Optional[int] = None
    population: Optional[str] = None


SOURCES: list[Source] = [
    # ── Optimal taxation & labor supply ──────────────────────────────
    Source(
        id="mirrlees1971",
        citation="Mirrlees, J. A. (1971). An exploration in the theory of optimum income taxation. Review of Economic Studies, 38(2), 175-208.",
        url="https://doi.org/10.2307/2296779",
        study_type="theoretical",
        key_finding="Optimal marginal tax rates depend on the distribution of abilities and labor supply elasticities; rates should be lower than commonly assumed.",
        doi="10.2307/2296779",
    ),
    Source(
        id="diamond_mirrlees1971",
        citation="Diamond, P. A., & Mirrlees, J. A. (1971). Optimal taxation and public production I: Production efficiency. American Economic Review, 61(1), 8-27.",
        url="https://doi.org/10.2307/1910538",
        study_type="theoretical",
        key_finding="Production efficiency is desirable even with distortionary taxation; intermediate goods should not be taxed.",
        doi="10.2307/1910538",
    ),
    Source(
        id="saez2001",
        citation="Saez, E. (2001). Using elasticities to derive optimal income tax rates. Review of Economic Studies, 68(1), 205-229.",
        url="https://doi.org/10.1111/1467-937X.00166",
        study_type="theoretical",
        key_finding="Derives optimal tax formulas using sufficient statistics (elasticities); optimal top rate depends on Pareto parameter and elasticity.",
        doi="10.1111/1467-937X.00166",
    ),
    Source(
        id="chetty2012",
        citation="Chetty, R. (2012). Bounds on elasticities with optimization frictions: A synthesis of micro and macro evidence. Econometrica, 80(3), 969-1018.",
        url="https://doi.org/10.3982/ECTA9043",
        study_type="meta_analysis",
        key_finding="Reconciles micro and macro labor supply elasticity estimates; Hicksian elasticity ~0.25 after accounting for frictions.",
        doi="10.3982/ECTA9043",
        effect_size=EffectSize(
            metric="elasticity",
            point_estimate=0.25,
            ci_lower=0.15,
            ci_upper=0.35,
        ),
    ),
    Source(
        id="keane2011",
        citation="Keane, M. P. (2011). Labor supply and taxes: A survey. Journal of Economic Literature, 49(4), 961-1075.",
        url="https://doi.org/10.1257/jel.49.4.961",
        study_type="review",
        key_finding="Comprehensive survey of labor supply elasticity estimates; Hicksian elasticities for men are small (0.1-0.3), larger for women.",
        doi="10.1257/jel.49.4.961",
    ),
    Source(
        id="saez_slemrod_giertz2012",
        citation="Saez, E., Slemrod, J., & Giertz, S. H. (2012). The elasticity of taxable income with respect to marginal tax rates: A critical review. Journal of Economic Literature, 50(1), 3-50.",
        url="https://doi.org/10.1257/jel.50.1.3",
        study_type="review",
        key_finding="Elasticity of taxable income ranges from 0.12 to 0.40; preferred estimate around 0.25 for broad income.",
        doi="10.1257/jel.50.1.3",
        effect_size=EffectSize(
            metric="elasticity",
            point_estimate=0.25,
            ci_lower=0.12,
            ci_upper=0.40,
        ),
    ),
    Source(
        id="feldstein1999",
        citation="Feldstein, M. (1999). Tax avoidance and the deadweight loss of the income tax. Review of Economics and Statistics, 81(4), 674-680.",
        url="https://doi.org/10.1162/003465399558391",
        study_type="quasi_experimental",
        key_finding="Taxable income elasticity captures behavioral responses beyond labor supply; deadweight loss of taxation is substantial.",
        doi="10.1162/003465399558391",
    ),
    # ── Speed-fatality power model ───────────────────────────────────
    Source(
        id="nilsson2004",
        citation="Nilsson, G. (2004). Traffic safety dimensions and the Power Model to describe the effect of speed on safety. Bulletin 221, Lund Institute of Technology.",
        url="https://lup.lub.lu.se/record/21612",
        study_type="meta_analysis",
        key_finding="Fatal crashes proportional to (v1/v0)^4; serious injuries to (v1/v0)^3; all injury crashes to (v1/v0)^2.",
        database="Lund University Publications",
        effect_size=EffectSize(
            metric="exponent",
            point_estimate=4.0,
            ci_lower=3.0,
            ci_upper=5.0,
        ),
        population="International road traffic studies",
    ),
    Source(
        id="elvik2019",
        citation="Elvik, R. (2019). A re-parameterisation of the Power Model of the relationship between the speed of traffic and the number of accidents and accident victims. Accident Analysis & Prevention, 124, 135-141.",
        url="https://doi.org/10.1016/j.aap.2018.11.014",
        study_type="meta_analysis",
        key_finding="Updated Power Model estimates: fatality exponent varies by road type; confirms nonlinear speed-crash relationship.",
        doi="10.1016/j.aap.2018.11.014",
        effect_size=EffectSize(
            metric="exponent",
            point_estimate=3.5,
            ci_lower=2.5,
            ci_upper=4.5,
        ),
    ),
    # ── Finnish day-fines ────────────────────────────────────────────
    Source(
        id="kaila2024",
        citation="Kaila, M. (2024). How do people react to income-based fines? Evidence from speeding tickets in Finland. CESifo Working Paper No. 11064.",
        url="https://www.cesifo.org/en/publications/2024/working-paper/how-do-people-react-income-based-fines-evidence-speeding-tickets",
        study_type="quasi_experimental",
        key_finding="Income-based fines reduce speeding more effectively among high-income drivers; limited labor supply distortion from day-fine system.",
        database="CESifo",
        population="Finnish drivers",
    ),
    Source(
        id="finnish_fines2023",
        citation="Statistics Finland (2023). Traffic offences and fines. Official Statistics of Finland.",
        url="https://stat.fi/en/statistics/rikam",
        study_type="administrative",
        key_finding="Administrative data on Finnish day-fine system; fines calibrated to net daily income minus fixed living costs.",
        database="Statistics Finland",
        population="Finland national",
    ),
    Source(
        id="kantorowicz_faure2021",
        citation="Kantorowicz-Reznichenko, E., & Faure, M. G. (2021). Day-fines: should the rich pay more? Review of Law & Economics, 17(3), 657-688.",
        url="https://doi.org/10.1515/rle-2021-0041",
        study_type="review",
        key_finding="Comparative analysis of day-fine systems across jurisdictions; income-based fines better achieve equal deterrence across income groups.",
        doi="10.1515/rle-2021-0041",
    ),
    # ── Pigouvian taxation & labor distortion ────────────────────────
    Source(
        id="bovenberg_demooij1994",
        citation="Bovenberg, A. L., & de Mooij, R. A. (1994). Environmental levies and distortionary taxation. American Economic Review, 84(4), 1085-1089.",
        url="https://www.jstor.org/stable/2118046",
        study_type="theoretical",
        key_finding="Optimal environmental tax is below Pigouvian level when interacting with distortionary labor taxes (tax-interaction effect).",
        doi="10.2307/2118046",
    ),
    Source(
        id="bovenberg_goulder1996",
        citation="Bovenberg, A. L., & Goulder, L. H. (1996). Optimal environmental taxation in the presence of other taxes: General-equilibrium analyses. American Economic Review, 86(4), 985-1000.",
        url="https://www.jstor.org/stable/2118314",
        study_type="theoretical",
        key_finding="Revenue-recycling effect partially offsets tax-interaction effect; optimal corrective tax still below marginal social damage.",
        doi="10.2307/2118314",
    ),
    Source(
        id="jacobs_demooij2015",
        citation="Jacobs, B., & de Mooij, R. A. (2015). Pigou meets Mirrlees: On the irrelevance of tax distortions for the second-best Pigouvian tax. Journal of Environmental Economics and Management, 71, 90-108.",
        url="https://doi.org/10.1016/j.jeem.2015.01.003",
        study_type="theoretical",
        key_finding="Optimal Pigouvian tax equals marginal external damage when income tax is optimized; tax distortions are irrelevant at second-best optimum.",
        doi="10.1016/j.jeem.2015.01.003",
    ),
    # ── Crime & deterrence ───────────────────────────────────────────
    Source(
        id="becker1968",
        citation="Becker, G. S. (1968). Crime and punishment: An economic approach. Journal of Political Economy, 76(2), 169-217.",
        url="https://doi.org/10.1086/259394",
        study_type="theoretical",
        key_finding="Rational agents weigh expected costs vs benefits of crime; optimal enforcement balances fine severity, detection probability, and enforcement costs.",
        doi="10.1086/259394",
    ),
    Source(
        id="polinsky_shavell1979",
        citation="Polinsky, A. M., & Shavell, S. (1979). The optimal tradeoff between the probability and magnitude of fines. American Economic Review, 69(5), 880-891.",
        url="https://www.jstor.org/stable/1813654",
        study_type="theoretical",
        key_finding="Maximal fines with low detection probability minimize enforcement costs; risk aversion limits optimal fine magnitude.",
        doi="10.2307/1813654",
    ),
    Source(
        id="polinsky_shavell1991",
        citation="Polinsky, A. M., & Shavell, S. (1991). A note on optimal fines when wealth varies among individuals. American Economic Review, 81(3), 618-621.",
        url="https://www.jstor.org/stable/2006526",
        study_type="theoretical",
        key_finding="When wealth varies, optimal fines should be wealth-dependent; flat fines over-deter the poor and under-deter the wealthy.",
        doi="10.2307/2006526",
    ),
    Source(
        id="polinsky2006",
        citation="Polinsky, A. M., & Shavell, S. (2007). The theory of public enforcement of law. In Handbook of Law and Economics (Vol. 1, pp. 403-454). Elsevier.",
        url="https://doi.org/10.1016/S1574-0730(07)01006-7",
        study_type="review",
        key_finding="Comprehensive review of optimal enforcement theory; sanctions should account for offender wealth, harm severity, and enforcement costs.",
        doi="10.1016/S1574-0730(07)01006-7",
    ),
    Source(
        id="garoupa1997",
        citation="Garoupa, N. (1997). The theory of optimal law enforcement. Journal of Economic Surveys, 11(3), 267-295.",
        url="https://doi.org/10.1111/1467-6419.00034",
        study_type="review",
        key_finding="Surveys extensions to Becker model including risk aversion, wealth heterogeneity, and income-dependent sanctions.",
        doi="10.1111/1467-6419.00034",
    ),
    Source(
        id="chalfin_mccrary2017",
        citation="Chalfin, A., & McCrary, J. (2017). Criminal deterrence: A review of the literature. Journal of Economic Literature, 55(1), 5-48.",
        url="https://doi.org/10.1257/jel.20141147",
        study_type="review",
        key_finding="Evidence supports deterrence through both police presence and sanction severity; elasticity of crime to police ~-0.3 to -0.5.",
        doi="10.1257/jel.20141147",
    ),
    Source(
        id="hansen2015",
        citation="Hansen, B. (2015). Punishment and deterrence: Evidence from drunk driving. American Economic Review, 105(4), 1581-1617.",
        url="https://doi.org/10.1257/aer.20130189",
        study_type="quasi_experimental",
        key_finding="Sharp punishment thresholds for BAC deter repeat drunk driving; marginal deterrent effect of harsher sanctions is significant.",
        doi="10.1257/aer.20130189",
        population="Washington State DUI offenders",
    ),
    Source(
        id="gneezy_rustichini2000",
        citation="Gneezy, U., & Rustichini, A. (2000). A fine is a price. Journal of Legal Studies, 29(1), 1-17.",
        url="https://doi.org/10.1086/468061",
        study_type="rct",
        key_finding="Introducing small fines for late daycare pickup increased lateness; fines can crowd out intrinsic motivation when set too low.",
        doi="10.1086/468061",
        sample_size=240,
        population="Israeli daycare parents",
    ),
    # ── Equity & monetary sanctions ──────────────────────────────────
    Source(
        id="harris2016",
        citation="Harris, A. (2016). A Pound of Flesh: Monetary Sanctions as Punishment for the Poor. Russell Sage Foundation.",
        url="https://www.russellsage.org/publications/pound-flesh",
        study_type="review",
        key_finding="Monetary sanctions disproportionately burden low-income individuals, creating cycles of debt, incarceration, and poverty.",
        database="Russell Sage Foundation",
    ),
    Source(
        id="lerman_weaver2014",
        citation="Lerman, A. E., & Weaver, V. M. (2014). Arresting Citizenship: The Democratic Consequences of American Crime Policy. University of Chicago Press.",
        url="https://doi.org/10.7208/chicago/9780226137988.001.0001",
        study_type="survey",
        key_finding="Contact with the criminal justice system, including monetary sanctions, erodes civic participation and trust in government.",
        doi="10.7208/chicago/9780226137988.001.0001",
        population="United States adults",
    ),
    Source(
        id="saez_stantcheva2016",
        citation="Saez, E., & Stantcheva, S. (2016). Generalized social marginal welfare weights for optimal tax theory. American Economic Review, 106(1), 24-45.",
        url="https://doi.org/10.1257/aer.20141362",
        study_type="theoretical",
        key_finding="Generalized welfare weights allow flexible social preferences beyond utilitarianism; optimal taxes depend on society's equity-efficiency tradeoff.",
        doi="10.1257/aer.20141362",
    ),
    # ── Traffic enforcement ──────────────────────────────────────────
    Source(
        id="deangelo_hansen2014",
        citation="DeAngelo, G., & Hansen, B. (2014). Life and death in the fast lane: Police enforcement and traffic fatalities. American Economic Journal: Economic Policy, 6(2), 231-257.",
        url="https://doi.org/10.1257/pol.6.2.231",
        study_type="quasi_experimental",
        key_finding="Reduced police enforcement during budget crises led to increased traffic fatalities; enforcement has strong deterrent effect on dangerous driving.",
        doi="10.1257/pol.6.2.231",
        population="Oregon drivers",
    ),
    Source(
        id="makowsky_stratmann2009",
        citation="Makowsky, M. D., & Stratmann, T. (2009). Political economy at any speed: What determines traffic citations? American Economic Review, 99(1), 509-527.",
        url="https://doi.org/10.1257/aer.99.1.509",
        study_type="quasi_experimental",
        key_finding="Out-of-town drivers receive more tickets; revenue motives influence traffic enforcement patterns beyond safety concerns.",
        doi="10.1257/aer.99.1.509",
        population="Massachusetts drivers",
    ),
    Source(
        id="bourgeon_picard2007",
        citation="Bourgeon, J.-M., & Picard, P. (2007). Point-record driving licence and road safety: An economic approach. Journal of Public Economics, 91(9), 1603-1629.",
        url="https://doi.org/10.1016/j.jpubeco.2007.02.007",
        study_type="theoretical",
        key_finding="Point-record systems create dynamic deterrence; combining monetary fines with license points improves enforcement effectiveness.",
        doi="10.1016/j.jpubeco.2007.02.007",
    ),
    # ── Other ────────────────────────────────────────────────────────
    Source(
        id="kaplow_shavell2002",
        citation="Kaplow, L., & Shavell, S. (2002). Fairness versus Welfare. Harvard University Press.",
        url="https://doi.org/10.4159/9780674039315",
        study_type="theoretical",
        key_finding="Welfare-based policy evaluation dominates fairness-based criteria; redistributive concerns should operate through the tax-transfer system.",
        doi="10.4159/9780674039315",
    ),
    Source(
        id="harberger1964",
        citation="Harberger, A. C. (1964). The measurement of waste. American Economic Review, 54(3), 58-76.",
        url="https://www.jstor.org/stable/1818326",
        study_type="theoretical",
        key_finding="Deadweight loss from taxation is proportional to the square of the tax rate; provides framework for measuring efficiency costs of distortions.",
        doi="10.2307/1818326",
    ),
    Source(
        id="chetty_looney_kroft2009",
        citation="Chetty, R., Looney, A., & Kroft, K. (2009). Salience and taxation: Theory and evidence. American Economic Review, 99(4), 1145-1177.",
        url="https://doi.org/10.1257/aer.99.4.1145",
        study_type="quasi_experimental",
        key_finding="Less salient taxes generate smaller behavioral responses; tax salience matters for both efficiency and optimal tax design.",
        doi="10.1257/aer.99.4.1145",
    ),
    Source(
        id="taubinsky_reesjones2018",
        citation="Taubinsky, D., & Rees-Jones, A. (2018). Attention variation and welfare: Theory and evidence from a tax salience experiment. Review of Economic Studies, 85(4), 2462-2496.",
        url="https://doi.org/10.1093/restud/rdx069",
        study_type="rct",
        key_finding="Heterogeneous attention to taxes affects welfare; optimal corrective taxes should account for attention variation across consumers.",
        doi="10.1093/restud/rdx069",
    ),
    Source(
        id="maag_etal2012",
        citation="Maag, E., Steuerle, C. E., Chakravarti, R., & Quakenbush, C. (2012). How marginal tax rates affect families at various levels of poverty. National Tax Journal, 65(4), 759-782.",
        url="https://doi.org/10.17310/ntj.2012.4.02",
        study_type="administrative",
        key_finding="Effective marginal tax rates can exceed 80% for low-income families due to benefit phase-outs; creates poverty traps and labor supply disincentives.",
        doi="10.17310/ntj.2012.4.02",
        population="US low-income families",
    ),
    Source(
        id="eu_vsl2014",
        citation="European Commission, DG MOVE (2014). Update of the Handbook on External Costs of Transport. Ricardo-AEA.",
        url="https://transport.ec.europa.eu/transport-themes/sustainable-transport/internalisation-transport-external-costs_en",
        study_type="administrative",
        key_finding="Value of statistical life for transport safety ~3.6M EUR (2010); provides standardized methodology for valuing accident risk reduction.",
        database="European Commission DG MOVE",
        population="European Union",
    ),
    # ── US calibration sources ──────────────────────────────────────
    Source(
        id="epa_vsl2024",
        citation="U.S. Environmental Protection Agency (2024). Mortality Risk Valuation. EPA Guidelines for Economic Analysis.",
        url="https://www.epa.gov/environmental-economics/mortality-risk-valuation",
        study_type="administrative",
        key_finding="Central VSL estimate of $11.6 million (2024 USD) for use in regulatory impact analyses; based on meta-analysis of stated and revealed preference studies.",
        database="US EPA",
        population="United States adults",
    ),
    Source(
        id="nhtsa_fars2024",
        citation="National Highway Traffic Safety Administration (2024). Fatality Analysis Reporting System (FARS). US DOT.",
        url="https://www.nhtsa.gov/research-data/fatality-analysis-reporting-system-fars",
        study_type="administrative",
        key_finding="1.37 deaths per 100 million VMT in 2023; approximately 40,990 traffic fatalities. Base fatality rate for active drivers ~0.00012 per year.",
        database="NHTSA FARS",
        population="United States drivers",
    ),
    Source(
        id="policyengine_us2024",
        citation="PolicyEngine (2024). PolicyEngine US microsimulation model. Enhanced CPS microdata.",
        url="https://policyengine.org",
        study_type="administrative",
        key_finding="Microsimulation of US federal and state tax-benefit system; computes marginal tax rates capturing federal/state income tax, FICA, EITC, and benefit phase-outs for ~155k CPS respondents.",
        database="PolicyEngine",
        population="United States, Enhanced CPS",
    ),
    Source(
        id="sf_income_fines2025",
        citation="City and County of San Francisco (2025). Income-Based Traffic Fine Pilot Program. San Francisco Municipal Transportation Agency.",
        url="https://www.sfmta.com/",
        study_type="administrative",
        key_finding="San Francisco launched the first major US income-based traffic fine program in 2025, scaling penalties with ability to pay for certain traffic violations.",
        database="SFMTA",
        population="San Francisco drivers",
    ),
    Source(
        id="staten_island_pilot1988",
        citation="Hillsman, S. T. (1990). Fines and Day Fines as a Means of Intermediate Sanctions. National Institute of Justice.",
        url="https://www.ojp.gov/pdffiles1/Digitization/122471NCJRS.pdf",
        study_type="quasi_experimental",
        key_finding="The Staten Island Day-Fine Project (1988-1990) demonstrated that income-scaled fines were feasible in the US criminal justice context; collection rates improved relative to fixed fines.",
        database="National Institute of Justice",
        population="Staten Island, New York",
    ),
    Source(
        id="census_cps2024",
        citation="U.S. Census Bureau (2024). Current Population Survey, Annual Social and Economic Supplement.",
        url="https://www.census.gov/programs-surveys/cps.html",
        study_type="survey",
        key_finding="Median household income approximately $80,610 (2023); individual earnings distribution provides basis for microsimulation of tax-benefit system interactions.",
        database="U.S. Census Bureau",
        population="United States",
        sample_size=155000,
    ),
]

_SOURCE_INDEX: dict[str, Source] = {s.id: s for s in SOURCES}


def get_source(source_id: str) -> Source | None:
    """Return a source by its id, or None if not found."""
    return _SOURCE_INDEX.get(source_id)


def validate_sources() -> list[str]:
    """Check all sources for common issues. Returns list of error strings."""
    errors: list[str] = []
    for s in SOURCES:
        if not s.url.startswith("http"):
            errors.append(f"{s.id}: URL does not start with http")
        if not s.doi and not s.database:
            errors.append(f"{s.id}: missing both DOI and database")
        if s.study_type == "meta_analysis" and s.effect_size is None:
            errors.append(f"{s.id}: meta_analysis without effect_size")
    return errors
