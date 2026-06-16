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
| Win back 5% of At Risk customers | 226,677 | 1.5% | 5% of At Risk users place one additional order at their historical average monetary value |
| Increase month-1 retention by 1 percentage point | 149,237 | 1.0% | A +1pp lift creates additional retained customers who purchase at platform AOV |
| Reduce all delayed order GMV by 10% | 115,089 | 0.7% | 10% of delayed GMV is protected from severe dissatisfaction risk |
| Reduce 8+ day delayed order GMV by 20% | 104,665 | 0.7% | 20% of severe-delay GMV is moved into a healthier delivery experience |
| Win back 3% of Dormant customers | 44,198 | 0.3% | 3% of Dormant users return with one order at their historical average monetary value |
| Convert 10% of Potential Loyalists to a second order | 18,463 | 0.1% | 10% place a second order at platform AOV |

## Business Interpretation

1. The largest modeled opportunity is At Risk customer win-back. This segment has high historical monetary value and contributes a large share of GMV, so even a 5% reactivation assumption creates meaningful upside.
2. Increasing month-1 retention by 1 percentage point is also attractive because the cohort base is large, so even a small retention lift can create meaningful GMV.
3. Delivery delay improvements should be treated as both a satisfaction lever and a revenue protection lever. Severe delays have much lower review scores, so reducing them can protect trust and future repeat purchase.
4. Potential Loyalists are smaller in scale, but they are very recent customers. This makes them useful for low-friction lifecycle tests such as second-order coupons or category-based recommendations.

## How To Validate These Opportunities

- Run A/B tests for At Risk win-back campaigns and measure incremental conversion, GMV, and margin.
- Track first-purchase cohorts before and after post-delivery lifecycle campaigns.
- Monitor delivery SLA improvements by seller, state, and product category.
- Compare review score, repeat purchase, and complaint rate for orders moved out of severe-delay buckets.

