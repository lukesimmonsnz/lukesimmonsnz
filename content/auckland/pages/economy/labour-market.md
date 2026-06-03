---
title: "Labour Market Inequality and Precarious Work"
section: economy
subpage: labour-market
order: 1
updated: 2026-04-26
summary: >
  Real wage growth in Auckland has lagged productivity growth for two decades. Underemployment runs at 8-10% of the labour force, concentrated in South and West Auckland. Gig and platform economy growth has created a precarious tier of workers without sick leave, guaranteed hours, or ACC coverage. The debate centres on whether extending employment protections to all workers or maintaining labour market flexibility is the higher-return intervention.

status: draft
generated_from: problem.auckland.economy.labour_market
---

# Labour Market Inequality and Precarious Work

<p class="horizon-band">Analysis horizon: 10yr · 50yr</p>



## The two-tier market

Auckland's labour market is functionally two markets: a primary market of permanent employment with full protections and a secondary market of casual, gig, and variable-hours employment without social insurance. The secondary market is not confined to teenagers and students — it includes adult heads of household in South and West Auckland working multiple casual jobs to cover rent. The income volatility of the secondary market is absorbed partly by families, partly by community, and partly by the welfare system; the platform companies that profit from it bear none of the risk.


## Wage growth as a distributional choice

Wages growing below productivity is not a market outcome; it is a consequence of the balance of power between workers and employers in wage-setting. Low union density, no sectoral bargaining, and a minimum wage set by annual political decision rather than automatic formula have produced a structural bias. The fact that profit share has risen while labour share has fallen is a measurement of this bias, not a natural law.


---

## References



- **Household Labour Force Survey 2023**, 2023 — <https://www.stats.govt.nz/topics/employment>

- **NZIER Productivity and Economic Performance 2023**, 2023 — <https://www.nzier.org.nz/publications>


<details class="technical-appendix" markdown="1">
<summary><strong>Technical details</strong> — drivers, solution camps, claims, and systems model</summary>

### Drivers


The following structural drivers contribute to this problem.


#### Labour Market Dualism and Precarious Work



- **Category:** regulatory
- **Timescale:** medium
- **Consensus:** contested

#### Weak Wage-Setting Institutions



- **Category:** institutional
- **Timescale:** long
- **Consensus:** contested


### Solution camps

A number of distinct positions recur in policy debates on this issue. Each is defensible on its own terms; none is obviously correct. Presented in alphabetical order without ranking.


#### Labour Market Flexibility and Employer Investment

Auckland's employment growth is driven by flexible, adaptive businesses; regulation that raises the cost of employment at the margin — hours guarantees, mandatory sick leave, higher minimum wages — reduces total employment by making some low-productivity jobs unviable. Flexibility in employment arrangements enables firms to manage demand volatility without layoffs; the welfare function is better served by a strong social safety net than by employment regulation.

**Flagship moves:**

- Maintain flexible employment law that allows variable-hours contracts for genuine casuals.
- Index minimum wage to inflation (CPI) only, not median wage, to protect employment viability of low-productivity roles.
- Reduce employer PAYE and ACC levy burden to incentivise full employment over contractor use.

**Tensions:**

- Employer flexibility arguments are strongest for genuinely marginal businesses; the majority of gig workers work for large, profitable platforms where the flexibility argument masks rent extraction from workers without exit options.

- CPI-only minimum wage indexation allows the real wage floor to fall relative to median wages over time; this is in tension with living wage norms and productivity sharing arguments.


**Interventions on the system:**

- Simplify casual employment contracting rules to reduce compliance cost for small employers while maintaining anti-exploitation provisions.
 (state variable: `small_business_employment_cost_index`, sign: -)
- Introduce a refundable employment tax credit for employers who convert casual workers to permanent part-time or full-time roles, incentivising the conversion without mandating it.
 (state variable: `precarious_worker_coverage_rate`, sign: +)


#### Labour Standards Reform and Worker Protection

The growth of precarious work without social insurance represents an externality: gig workers' income risk is partly borne by the public health and welfare systems when volatility produces hardship. Extending minimum employment protections (sick leave, guaranteed hours, ACC coverage) to all workers regardless of employment classification corrects this externality and narrows the labour market inequality that suppresses consumption in high-deprivation Auckland areas.

**Flagship moves:**

- Legislate minimum guaranteed hours (10 hours/week) for all workers employed more than 6 months with the same employer.
- Extend ACC work injury cover to all platform and gig workers classified as contractors.
- Raise minimum wage annually to a fixed percentage (e.g. 60%) of median wage, removing political discretion.

**Tensions:**

- Mandatory hours guarantees and higher minimum wages may reduce employer flexibility and increase casualisation as employers avoid the 6-month tenure trigger; the employment effect is empirically contested.

- ACC extension to gig workers raises levy costs for platform companies that may pass costs through to consumers or reduce worker pay rates.


**Interventions on the system:**

- Amend Employment Relations Act to extend minimum employment protections to all workers earning more than $10,000 per year from any single employer, regardless of contractor classification.
 (state variable: `precarious_worker_coverage_rate`, sign: +) (relaxes: `Contractor classification exclusion from employment protections`)
- Set minimum wage at 60% of median wage in legislation, with automatic annual adjustment, removing discretionary annual reviews.
 (state variable: `real_minimum_wage_median_ratio`, sign: +)


### Claims cited on this page

- **Real wage growth in Auckland has lagged productivity growth over the past two decades; median wage growth after inflation has been below labour productivity growth in most years, with the gap reflected in rising corporate profit share and falling labour share of national income.
** — Household Labour Force Survey 2023; NZIER Productivity and Economic Performance 2023.
- **Auckland underemployment (workers employed part-time who want full- time work) runs at approximately 8-10% of the labour force, substantially above the headline unemployment rate; underemployment is concentrated in South and West Auckland, among youth, and in service sectors where casual and variable-hours contracts are common.
** *(confidence: medium)* — Household Labour Force Survey 2023.
- **Gig and platform economy employment in Auckland has grown substantially; workers classified as independent contractors lack employment protections (sick leave, holiday pay, minimum hours guarantees), creating a two-tier labour market where a growing share of Auckland workers bear income volatility risk without social insurance coverage.
** *(confidence: medium)* — Household Labour Force Survey 2023.

### Systems-model notes

*State variables:* precarious_worker_coverage_rate, real_minimum_wage_median_ratio, small_business_employment_cost_index, underemployment_rate.

*Constraints:* Employment effect: labour protection mandates may reduce total employment at margin; evidence is mixed, Platform power: large gig platforms have monopsonistic wage-setting power that flexibility arguments do not address, Social insurance gap: welfare system partly compensates for precarious income volatility but not completely.

*Inputs:* minimum_hours_guarantee_threshold, minimum_wage_indexation_method, gig_worker_acc_coverage, employer_conversion_incentives.


*Feedback loops:*

- `Precarious income → consumption volatility → weaker domestic demand → lower employment stability`
- `Wage growth below productivity → rising profit share → reduced worker spending → growth dependent on credit`


</details>

---

*Generated from `problem.auckland.economy.labour_market` on 2026-05-06. Do not hand-edit. Edit the entity files under the region's `data/` directory and re-run the region's render.py.*
