# Marketplace Revenue, Retention and Experience Analytics

An end-to-end e-commerce marketplace analytics project using SQL, Python, DuckDB, and Tableau to identify revenue drivers, customer retention risks, delivery experience issues, and GMV growth opportunities.

## Dashboard

[View the Tableau Public dashboard](https://public.tableau.com/app/profile/xiaoyuan.wu/viz/marketplace_revenue_retention_dashboard/MarketplaceAnalyticsOverview)

The dashboard summarizes marketplace performance across two views:

- **Revenue & Opportunity**: monthly GMV trend, top GMV categories, and estimated opportunity sizing.
- **Retention & Experience**: RFM customer segments, delivery delay impact, and cohort retention.

## Business Context

Marketplace teams need to understand not only where revenue comes from, but also whether growth is sustainable. This project analyzes the Brazilian E-Commerce Public Dataset by Olist to answer:

- Which product categories and customer segments contribute the most GMV?
- How strong is repeat purchase behavior after a customer's first order?
- How does delivery delay affect customer satisfaction?
- Which business opportunities should be prioritized based on potential GMV impact?

## Dataset

Source: [Brazilian E-Commerce Public Dataset by Olist](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce)

The dataset contains marketplace orders, customers, products, sellers, payments, reviews, and geolocation data. Raw Kaggle CSV files are excluded from this repository; only aggregated outputs for dashboard reproduction are included.

## Tools

- **SQL**: data modeling, revenue analysis, retention cohort, RFM segmentation
- **DuckDB**: local analytical database
- **Python**: data pipeline, visualization, opportunity sizing
- **Tableau Public**: executive dashboard

## Analysis Workflow

```text
Raw marketplace data
        -> analytical order-level model
        -> SQL metric tables
        -> Python validation and opportunity sizing
        -> Tableau dashboard
        -> business recommendations
```

## Key Findings

- Total delivered GMV analyzed is approximately **15.42M BRL**.
- Average order value is approximately **159.85 BRL**, while orders per customer are only **1.03**, indicating limited repeat purchase behavior.
- The repeat customer rate is approximately **3.0%**, making retention the biggest structural growth issue.
- The top 5 product categories contribute approximately **39.4%** of category-level GMV.
- **At Risk** customers contribute approximately **4.53M BRL** in historical GMV, representing a meaningful win-back opportunity.
- A 5% win-back scenario for At Risk customers is estimated to affect approximately **226.7K BRL** in GMV.
- Orders delayed by 8+ days have an average review score of **1.70**, compared with **4.21** for on-time or early deliveries.

## Business Recommendations

1. Prioritize win-back campaigns for high-value At Risk customers.
2. Improve first-purchase lifecycle activation to increase second-order conversion.
3. Protect high-GMV categories such as `health_beauty`, `watches_gifts`, and `bed_bath_table`.
4. Monitor high-revenue categories with weaker satisfaction before scaling paid traffic.
5. Reduce severe delivery delays through seller SLA tracking and proactive logistics alerts.

## Methodology

### Revenue Analysis

Built monthly, category, and geography-level GMV views using delivered orders and payment value. Order-level payment value is aggregated before item-level joins to avoid GMV inflation from one-to-many relationships.

### Cohort Retention

Grouped customers by first purchase month and calculated later-month activity to evaluate repeat purchase behavior.

### RFM Segmentation

Segmented customers by recency, frequency, and monetary value into groups such as Champions, Loyal Customers, At Risk, Dormant, and One-time / Mid Value.

### Delivery Experience

Compared review scores across delivery delay buckets to quantify the relationship between logistics performance and customer satisfaction.

### Opportunity Sizing

Estimated directional GMV impact for practical scenarios, including At Risk customer win-back, month-1 retention lift, delayed-order reduction, and Potential Loyalist conversion.

## Repository Structure

```text
.
├── dashboard/
│   ├── bi_export/                 # Aggregated Tableau-ready CSV files
│   └── README.md
├── reports/
│   ├── figures/                   # Python-generated visualizations
│   └── business_recommendations.md
├── sql/                           # SQL analysis scripts
├── src/                           # Python pipeline scripts
├── requirements.txt
└── README.md
```

## Reproducibility

To reproduce the full pipeline, download the original Olist CSV files from Kaggle and place them under `data/raw/`, then run:

```bash
python3 -m pip install -r requirements.txt
python3 src/build_duckdb.py
python3 src/run_sql_analysis.py
python3 src/opportunity_sizing.py
python3 src/prepare_bi_exports.py
```

The Tableau dashboard is published publicly here:

```text
https://public.tableau.com/app/profile/xiaoyuan.wu/viz/MarketplaceRevenueRetentionExperienceAnalytics/MarketplaceAnalyticsOverview
```
