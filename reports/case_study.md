# Marketplace Revenue, Retention and Experience Analytics

## Executive Summary

This project analyzes marketplace revenue, customer retention, RFM segmentation, delivery experience, and GMV opportunity sizing using the Brazilian E-Commerce Public Dataset by Olist. The goal is to identify where GMV comes from, why repeat purchase is weak, which users and categories should be prioritized, and which operational levers could protect customer experience.

The analysis shows that the marketplace generated approximately **15.42M BRL** in delivered GMV, but repeat purchase behavior is structurally weak: orders per customer are only **1.03**, the repeat customer rate is approximately **3.0%**, and six-month cumulative GMV per cohort customer is only **1.7%** higher than month-0 GMV per cohort customer. This means most customer value is captured in the first purchase.

The strongest business opportunities are At Risk customer win-back, first-to-second purchase activation, and delivery reliability improvement for high-GMV categories and sellers.

## Business Questions

- What are the main drivers of marketplace GMV?
- Which product categories and customer segments contribute the most revenue?
- How strong is retention after the first purchase?
- How does delivery delay affect customer satisfaction?
- Which initiatives should be prioritized based on directional GMV impact?

## Methodology

### Data Modeling

I built an analytical order-item wide table using orders, customers, products, sellers, payments, reviews, and delivery timestamps. Payment value was aggregated at order level before item-level joins to avoid GMV inflation from one-to-many relationships.

### Revenue and Category Analysis

I analyzed GMV, AOV, orders, customers, and category contribution across time and product groups.

### Retention and Customer Segmentation

I created cohort retention tables based on first purchase month and built RFM customer segmentation using recency, frequency, and monetary value.

### Experience and Operations Diagnostics

I analyzed review score by delivery delay bucket, then added seller SLA risk and category satisfaction risk scoring to connect customer experience with operational prioritization.

### Opportunity Sizing

I estimated directional GMV impact for win-back, retention lift, and delivery improvement scenarios. These are not causal lift estimates; they are prioritization tools that should be validated through controlled tests.

## Key Findings

### 1. GMV growth is limited by weak repeat behavior

- Total delivered GMV: **15.42M BRL**
- Delivered orders: **96,478**
- Purchasing customers: **93,358**
- AOV: **159.85 BRL**
- Orders per customer: **1.03**
- Repeat customer rate: **3.0%**

Six-month cumulative GMV per cohort customer is only **1.7%** higher than month-0 GMV per cohort customer, suggesting that most value is captured at first purchase and repeat purchase contributes limited incremental value.

### 2. Revenue is concentrated in a small number of categories

The top 5 product categories contribute approximately **39.4%** of category-level GMV. Top categories include `health_beauty`, `watches_gifts`, `bed_bath_table`, `sports_leisure`, and `computers_accessories`.

### 3. High-GMV categories also carry experience risk

The category risk score highlights `bed_bath_table` as the highest-risk category because it combines large GMV, lower review score, late delivery exposure, and high poor-review rate.

Examples:

- `bed_bath_table`: **1.23M GMV**, **3.92** average review score, **17.9%** poor-review rate
- `computers_accessories`: **1.03M GMV**, **3.99** average review score, **16.9%** poor-review rate
- `furniture_decor`: **0.88M GMV**, **3.95** average review score, **17.8%** poor-review rate

### 4. At Risk customers are the largest retention opportunity

RFM segmentation shows that At Risk customers contribute approximately **4.53M BRL**, or **29.4%** of RFM GMV. These customers have high historical monetary value but long recency, making them a strong win-back target.

### 5. Delivery delay is strongly associated with lower review scores

Average review score by delivery delay bucket:

- On time / Early: **4.21**
- Delayed 1-3 days: **3.23**
- Delayed 4-7 days: **2.09**
- Delayed 8+ days: **1.70**

This shows that logistics reliability is a clear customer-experience lever.

## Opportunity Sizing

| Scenario | Estimated GMV Impact | Strategic Use |
|---|---:|---|
| Win back 5% of At Risk customers | 226,813 | Retention campaign sizing |
| Increase month-1 retention by 1 percentage point | 149,237 | Lifecycle marketing target |
| Reduce all delayed order GMV by 10% | 115,089 | Logistics improvement target |
| Reduce 8+ day delayed order GMV by 20% | 104,665 | SLA and seller operations sizing |
| Win back 3% of Dormant customers | 45,620 | Low-cost reactivation test |
| Convert 10% of Potential Loyalists to a second order | 3,773 | Post-first-purchase activation |

## Recommendations

1. **Prioritize At Risk customer win-back.** Use personalized category-based vouchers and free-shipping incentives for high-monetary customers with long recency.
2. **Improve first-to-second order conversion.** Trigger post-delivery lifecycle campaigns within 7-14 days and recommend complementary products.
3. **Protect high-GMV categories with experience risk.** Improve seller quality, product information, and delivery expectation setting for `bed_bath_table`, `computers_accessories`, and `furniture_decor`.
4. **Use seller SLA risk to target operations.** Prioritize sellers with high GMV and high poor-review or delay exposure instead of ranking sellers by delay rate alone.
5. **Validate opportunity sizing through experiments.** Use holdout-based win-back campaigns, cohort tracking, and seller SLA pilots to measure incremental GMV and margin.

## Limitations

- The dataset does not include browsing, impressions, or marketing spend, so full funnel conversion and attribution cannot be measured.
- GMV impact is not profit impact because margin, discount cost, logistics cost, and refund cost are not available.
- Opportunity sizing scenarios are directional assumptions, not causal estimates.
- Retention is based on completed delivered orders and may understate user engagement outside purchase behavior.

## Deliverables

- SQL analysis scripts in `sql/`
- Python pipeline scripts in `src/`
- Business reports in `reports/`
- Tableau dashboard published on Tableau Public
- Aggregated BI-ready CSV files in `dashboard/bi_export/`
