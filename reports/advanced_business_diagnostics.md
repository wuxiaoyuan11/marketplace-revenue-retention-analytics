# Advanced Business Diagnostics

This report extends the core revenue, retention, and satisfaction analysis with three business diagnostics that are useful for marketplace operations and BA-style decision support.

## 1. Seller SLA Risk

Seller SLA risk estimates which sellers combine meaningful GMV scale with operational risk. The score uses delivered-order GMV multiplied by three experience-risk signals:

```text
SLA risk score = GMV x (late delivery rate + severe delay rate + poor review rate)
```

Top seller risk example:

| Metric | Value |
|---|---:|
| Delivered orders | 973 |
| GMV | 237,807 |
| Late delivery rate | 9.1% |
| Severe delay rate | 4.5% |
| Poor review rate | 25.3% |
| SLA risk score | 92,630 |

Business interpretation: seller operations should not only rank sellers by GMV or delay rate separately. A risk-weighted view helps identify sellers where operational improvement could protect both customer experience and revenue.

Output tables:

```text
data/processed/seller_sla_summary.csv
dashboard/bi_export/seller_sla_summary.csv
```

## 2. Category Satisfaction Risk Score

Category risk combines revenue concentration, review gap, delivery delay, and poor-review exposure.

```text
Category risk score =
GMV share x (review gap index + late delivery rate + severe delay rate + poor review rate)
```

Top risk categories:

| Rank | Category | GMV | Avg Review Score | Late Delivery Rate | Poor Review Rate |
|---:|---|---:|---:|---:|---:|
| 1 | bed_bath_table | 1,225,209 | 3.92 | 7.0% | 17.9% |
| 2 | watches_gifts | 1,264,333 | 4.07 | 7.2% | 14.7% |
| 3 | health_beauty | 1,412,090 | 4.19 | 7.6% | 12.4% |
| 4 | computers_accessories | 1,032,724 | 3.99 | 6.5% | 16.9% |
| 5 | furniture_decor | 880,330 | 3.95 | 7.0% | 17.8% |

Business interpretation: `health_beauty` is the largest GMV category, but `bed_bath_table` ranks highest in risk because it combines large GMV, below-ideal review score, and high poor-review exposure. This suggests category-level quality and seller operations should be improved before scaling demand generation.

Output tables:

```text
data/processed/category_risk_score.csv
dashboard/bi_export/category_risk_score.csv
```

## 3. Cohort LTV Proxy

Because the dataset does not include gross margin or marketing cost, this project uses cumulative GMV per original cohort customer as an LTV proxy.

```text
Cumulative GMV per cohort customer =
cumulative cohort GMV / original cohort customer count
```

Across observable cohorts with six months of history:

| Metric | Value |
|---|---:|
| Average month-0 GMV per cohort customer | 163.42 |
| Average month-6 cumulative GMV per cohort customer | 166.17 |
| Incremental lift from month 0 to month 6 | 1.7% |

Business interpretation: most cohort value is captured in the first purchase month. This supports the retention finding that the marketplace has weak repeat purchase behavior and should prioritize first-to-second order activation.

Output tables:

```text
data/processed/cohort_ltv_proxy.csv
dashboard/bi_export/cohort_ltv_proxy.csv
```

## How These Diagnostics Improve the Analysis

- Seller SLA risk connects customer satisfaction to marketplace operations.
- Category risk score turns descriptive category rankings into a prioritization framework.
- Cohort LTV proxy gives a revenue-based retention view beyond simple active-customer retention.
