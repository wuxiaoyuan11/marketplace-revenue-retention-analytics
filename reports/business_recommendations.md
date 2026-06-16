# Business Recommendations

## Executive Summary

This analysis uses the Olist e-commerce marketplace dataset to evaluate revenue growth, customer retention, RFM segmentation, and delivery-related customer satisfaction.

Key outputs:

- Total delivered GMV analyzed: about 15.42M BRL.
- Top 5 product categories contribute about 39.4% of category-level GMV.
- At Risk customers contribute about 29.4% of total RFM GMV, making them a high-priority retention segment.
- Orders delayed by 8+ days have an average review score of 1.70, compared with 4.21 for on-time or early deliveries.
- Average month-1 cohort retention is about 5.5%, indicating a marketplace with strong one-time purchase behavior.
- Opportunity sizing estimates that winning back 5% of At Risk customers could bring about 226.7K incremental GMV under a directional reactivation assumption.

## Key Charts

Generated figures are saved in:

```text
reports/figures/
```

Files:

- `01_monthly_gmv_trend.png`
- `02_top_category_gmv.png`
- `03_rfm_segment_gmv.png`
- `04_delivery_delay_review_score.png`
- `05_cohort_retention_heatmap.png`

## Findings

### 0. GMV is mainly driven by customer scale, weak repeat behavior, and AOV

The GMV metric tree shows:

- Total GMV: 15.42M
- Delivered orders: 96,478
- Purchasing customers: 93,358
- AOV: 159.85
- Orders per customer: 1.03
- Repeat customer rate: 3.0%

This suggests that the marketplace has broad customer coverage but weak repeat behavior. Growth opportunities should therefore focus not only on acquiring orders, but also on increasing repeat purchase and customer lifecycle value.

### 1. Revenue is concentrated in a few major categories

Top categories by GMV:

1. health_beauty: 1.41M GMV
2. watches_gifts: 1.26M GMV
3. bed_bath_table: 1.23M GMV
4. sports_leisure: 1.12M GMV
5. computers_accessories: 1.03M GMV

The top 5 categories contribute about 39.4% of category-level GMV. This means category-level operations and marketing decisions can have a large impact on overall marketplace revenue.

### 2. Some high-GMV categories have satisfaction risks

Several categories have meaningful GMV but weaker review performance:

- bed_bath_table: 1.23M GMV, 3.92 average review score
- furniture_decor: 0.88M GMV, 3.95 average review score
- computers_accessories: 1.03M GMV, 3.99 average review score
- office_furniture: 0.34M GMV, 3.51 average review score

These categories are important because they combine revenue scale with experience risk.

### 3. At Risk customers are a major revenue protection opportunity

RFM segmentation shows:

- Loyal Customers: 5.19M GMV, 33.6% of RFM GMV
- At Risk: 4.53M GMV, 29.4% of RFM GMV
- Champions: 3.36M GMV, 21.8% of RFM GMV

At Risk customers have high historical monetary value but long recency. This group should be prioritized for win-back campaigns because protecting their revenue base is likely more efficient than acquiring new customers from scratch.

### 4. Delivery delay has a strong negative relationship with review score

Average review score by delivery delay:

- On time / Early: 4.21
- Delayed 1-3 days: 3.23
- Delayed 4-7 days: 2.09
- Delayed 8+ days: 1.70

The gap between on-time orders and 8+ day delayed orders is about 2.51 review points. Delivery reliability is therefore one of the clearest operational levers for improving customer satisfaction.

### 5. Repeat purchase behavior is weak

Average month-1 cohort retention is about 5.5%. This suggests many users behave like one-time purchasers. The business should treat post-first-purchase activation as a core lifecycle problem.

## Recommendations

### Recommendation 1: Protect high-GMV categories while improving low-score experiences

Prioritize category operations for high-GMV categories with relatively low ratings, especially `bed_bath_table`, `furniture_decor`, `computers_accessories`, and `office_furniture`.

Actions:

- Audit top sellers in these categories for late delivery, return rate, and review complaints.
- Improve product detail quality and delivery expectation setting.
- Create category-specific quality scorecards for sellers.

Expected business impact:

- Improve review score in high-revenue categories.
- Reduce refund, complaint, and churn risk.
- Protect category-level GMV.

### Recommendation 2: Launch win-back campaigns for At Risk customers

At Risk customers contribute about 4.53M GMV, or 29.4% of RFM GMV. They should receive targeted retention treatment.

Directional opportunity sizing:

- If 5% of At Risk customers place one additional order at their historical average monetary value, estimated GMV impact is about 226.7K.

Actions:

- Send personalized vouchers based on previous purchase category.
- Use limited-time free shipping or installment incentives.
- Prioritize users with high monetary value and long recency.

Expected business impact:

- Recover high-value customers before they become dormant.
- Improve repeat purchase rate.
- Increase GMV without relying only on new customer acquisition.

### Recommendation 3: Convert Potential Loyalists after first purchase

Month-1 retention is only about 5.5%, so the first 30 days after purchase are important.

Directional opportunity sizing:

- Increasing month-1 retention by 1 percentage point could create about 149.2K estimated GMV, assuming retained users purchase at platform AOV.

Actions:

- Trigger post-delivery campaigns within 7-14 days.
- Recommend complementary products from the same category.
- Offer a second-purchase coupon with a clear expiration date.

Expected business impact:

- Increase repeat purchase rate.
- Improve customer lifetime value.
- Build stronger cohorts over time.

### Recommendation 4: Reduce long delivery delays in high-impact regions and categories

Orders delayed 8+ days have an average review score of only 1.70. Long delays should be treated as a customer satisfaction risk.

Directional opportunity sizing:

- Reducing severe 8+ day delayed GMV exposure by 20% represents about 104.7K GMV in affected order value.
- Reducing all delayed GMV exposure by 10% represents about 115.1K GMV in affected order value.

Actions:

- Monitor delayed orders by state and seller.
- Set alerts for orders likely to miss estimated delivery.
- Improve seller logistics SLA for high-volume categories.
- Proactively notify customers when delivery risk is detected.

Expected business impact:

- Improve customer satisfaction and review score.
- Reduce negative reviews from severe delays.
- Improve trust in the marketplace.

### Recommendation 5: Use category-level investment instead of broad promotions

The top 5 categories account for about 39.4% of category-level GMV, but categories differ in AOV and satisfaction.

Actions:

- Increase marketing spend on high-GMV and high-score categories such as `health_beauty` and `sports_leisure`.
- For high-GMV but lower-score categories, fix experience issues before increasing paid traffic.
- Use AOV to decide whether to promote discounts, bundles, or free shipping.

Expected business impact:

- Improve marketing ROI.
- Avoid sending more traffic into weak customer experiences.
- Balance GMV growth with satisfaction.

## Dashboard Implications

The final dashboard should include:

- GMV trend and category contribution.
- RFM segment GMV and customer count.
- Cohort retention heatmap.
- Delivery delay vs review score.
- High-GMV low-score category and region tables.
