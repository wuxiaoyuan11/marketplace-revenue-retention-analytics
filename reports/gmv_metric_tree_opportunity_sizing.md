# GMV Metric Tree and Opportunity Sizing

## Why This Matters

This section turns descriptive analysis into business decision support. Instead of only saying which category or customer group performs better, it estimates how much GMV could be affected if the business improves retention, reactivation, or delivery reliability.

## GMV Metric Tree

At the marketplace level:

```text
GMV = Orders x AOV
Orders = Customers x Orders per Customer
GMV per Customer = AOV x Orders per Customer
Repeat GMV growth depends on repeat customer rate, repeat frequency, and AOV.
```

| Metric | Value | Definition |
|---|---:|---|
| Total GMV | 15,422,462 | Delivered order payment value |
| Orders | 96,478 | Number of delivered orders |
| Customers | 93,358 | Unique purchasing customers |
| AOV | 159.85 | GMV / orders |
| Orders per customer | 1.03 | Orders / customers |
| GMV per customer | 165.20 | GMV / customers |
| Repeat customers | 2,801 | Customers with 2+ delivered orders |
| Repeat customer rate | 3.0% | Repeat customers / customers |

## Opportunity Sizing Scenarios

These are directional estimates, not causal experiment results. They are useful for prioritizing which initiatives are large enough to test.

| Scenario | Estimated GMV Impact | % of Total GMV | Assumption |
|---|---:|---:|---|
| Win back 5% of At Risk customers | 226,813 | 1.5% | 5% of At Risk users place one additional order at their historical average monetary value |
| Increase month-1 retention by 1 percentage point | 149,237 | 1.0% | A +1pp lift creates additional retained customers who purchase at platform AOV |
| Reduce all delayed order GMV by 10% | 115,089 | 0.7% | 10% of delayed GMV is protected from severe dissatisfaction risk |
| Reduce 8+ day delayed order GMV by 20% | 104,665 | 0.7% | 20% of severe-delay GMV is moved into a healthier delivery experience |
| Win back 3% of Dormant customers | 45,620 | 0.3% | 3% of Dormant users return with one order at their historical average monetary value |
| Convert 10% of Potential Loyalists to a second order | 3,773 | 0.0% | 10% place a second order at platform AOV |

## Assumptions and Formulas

| Scenario | Formula |
|---|---|
| Win back 5% of At Risk customers | At Risk customers x 5% x At Risk avg monetary value |
| Increase month-1 retention by 1 percentage point | Cohort customers x 1pp retention lift x platform AOV |
| Reduce all delayed order GMV by 10% | All delayed GMV x 10% |
| Reduce 8+ day delayed order GMV by 20% | 8+ day delayed GMV x 20% |
| Win back 3% of Dormant customers | Dormant customers x 3% x Dormant avg monetary value |
| Convert 10% of Potential Loyalists to a second order | Potential Loyalist customers x 10% x platform AOV |

## Limitations

- These estimates are directional sizing exercises, not causal lift estimates.
- GMV impact does not equal profit impact because margin, discount cost, logistics cost, and refund cost are not available in the dataset.
- Customer reactivation assumptions may overlap across segments, so scenarios should not be added together without de-duplication.
- Delivery-improvement scenarios estimate GMV exposure protected from poor experience, not guaranteed incremental GMV.
- The dataset does not include browsing, impressions, marketing spend, or campaign touchpoints, so conversion funnel and attribution analysis are approximated from order behavior.

## Business Interpretation

1. The largest modeled opportunity is At Risk customer win-back. This segment has high historical monetary value and contributes a large share of GMV, so even a 5% reactivation assumption creates meaningful upside.
2. Increasing month-1 retention by 1 percentage point is also attractive because the cohort base is large, so even a small retention lift can create meaningful GMV.
3. Delivery delay improvements should be treated as both a satisfaction lever and a revenue protection lever. Severe delays have much lower review scores, so reducing them can protect trust and future repeat purchase.
4. Potential Loyalists are smaller in scale, but they are very recent customers. This makes them useful for low-friction lifecycle tests such as second-order coupons or category-based recommendations.

## How To Validate These Opportunities

| Scenario | Validation plan |
|---|---|
| Win back 5% of At Risk customers | Run a holdout-based win-back test and measure incremental conversion, GMV, and margin versus control. |
| Increase month-1 retention by 1 percentage point | Track month-1 retention, second-order GMV, and repeat purchase rate before and after lifecycle interventions. |
| Reduce all delayed order GMV by 10% | Track delayed-order GMV exposure, complaint rate, review score, and downstream repeat purchase after SLA changes. |
| Reduce 8+ day delayed order GMV by 20% | Monitor SLA intervention sellers versus comparable sellers on delay rate, review score, and repeat purchase. |
| Win back 3% of Dormant customers | Test low-cost reactivation coupons and compare reactivation rate, subsidy cost, and incremental GMV. |
| Convert 10% of Potential Loyalists to a second order | Measure second-order conversion lift from post-delivery lifecycle campaigns against a control group. |

