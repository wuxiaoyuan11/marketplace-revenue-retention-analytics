# Marketplace Revenue, Retention and Experience Analytics

End-to-end e-commerce marketplace analytics project for Data Analyst / Business Analyst internship applications.

This project uses SQL, Python, DuckDB, and Tableau Public to analyze GMV growth, product category contribution, customer retention, RFM user segmentation, delivery experience, and business opportunity sizing on the Brazilian E-Commerce Public Dataset by Olist.

## Tableau Dashboard

[View the Tableau Public dashboard](https://public.tableau.com/app/profile/xiaoyuan.wu/viz/marketplace_revenue_retention_dashboard/MarketplaceAnalyticsOverview)

The dashboard covers:

- Monthly GMV trend
- Top product categories by GMV
- RFM customer segment GMV
- Delivery delay vs review score
- Cohort retention heatmap
- Estimated GMV impact by business opportunity

## Business Questions

1. What drives marketplace GMV growth across time, category, and region?
2. Which product categories contribute the most revenue?
3. Which customer segments are high-value, at-risk, dormant, or one-time buyers?
4. How weak is repeat purchase behavior after first purchase?
5. How does delivery delay affect customer review score?
6. Which business opportunities should be prioritized based on estimated GMV impact?

## Dataset

Dataset: [Brazilian E-Commerce Public Dataset by Olist](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce)

The raw Kaggle CSV files are not included in this repository because of file size and data-source hygiene. To reproduce the project, download the dataset from Kaggle and place the original CSV files in:

```text
data/raw/
```

Expected files:

```text
olist_customers_dataset.csv
olist_geolocation_dataset.csv
olist_order_items_dataset.csv
olist_order_payments_dataset.csv
olist_order_reviews_dataset.csv
olist_orders_dataset.csv
olist_products_dataset.csv
olist_sellers_dataset.csv
product_category_name_translation.csv
```

## Project Workflow

```text
Raw Kaggle CSVs
      |
      v
DuckDB analytical database
      |
      v
SQL wide tables and metric outputs
      |
      v
Python visualization and opportunity sizing
      |
      v
Tableau-ready BI exports and dashboard
      |
      v
Business recommendations and resume-ready insights
```

## Key Findings

- Total delivered GMV analyzed: about 15.42M BRL.
- AOV is about 159.85 BRL, while orders per customer are only 1.03.
- Repeat customer rate is about 3.0%, showing weak repeat purchase behavior.
- Top 5 product categories contribute about 39.4% of category-level GMV.
- At Risk customers contribute about 4.53M historical GMV, or 29.4% of RFM GMV.
- A 5% At Risk win-back scenario is estimated to affect about 226.7K GMV.
- Orders delayed by 8+ days have an average review score of 1.70, compared with 4.21 for on-time or early deliveries.

## Recommendations

1. Prioritize win-back campaigns for At Risk customers with high historical monetary value.
2. Improve first-purchase lifecycle activation to increase month-1 retention and second-order conversion.
3. Protect high-GMV categories such as `health_beauty`, `watches_gifts`, and `bed_bath_table`.
4. Fix high-GMV but lower-satisfaction categories before increasing paid traffic.
5. Reduce severe delivery delays through seller SLA monitoring and proactive logistics alerts.

## Repository Structure

```text
.
├── dashboard/
│   ├── bi_export/                      # Small Tableau / Power BI-ready CSV files
│   ├── marketplace_revenue_retention_dashboard.twb
│   ├── tableau_powerbi_build_guide.md
│   └── tableau_quick_start.md
├── data/
│   ├── raw/                            # Raw Kaggle CSV files, ignored by git
│   └── processed/                      # Generated analytical outputs, ignored by git
├── reports/
│   ├── figures/                        # Python-generated chart images
│   ├── business_recommendations.md
│   └── gmv_metric_tree_opportunity_sizing.md
├── sql/                                # SQL analysis scripts
├── src/                                # Python pipeline scripts
├── requirements.txt
└── README.md
```

## How To Reproduce

Install dependencies:

```bash
python3 -m pip install -r requirements.txt
```

Build the local DuckDB analytical database:

```bash
python3 src/build_duckdb.py
```

Run SQL analysis:

```bash
python3 src/run_sql_analysis.py
```

Generate Python chart images:

```bash
MPLCONFIGDIR=.matplotlib python3 src/create_visualizations.py
```

Run GMV metric tree and opportunity sizing:

```bash
python3 src/opportunity_sizing.py
```

Prepare Tableau / Power BI exports:

```bash
python3 src/prepare_bi_exports.py
```

Optional local HTML dashboard:

```bash
python3 src/create_dashboard.py
```

Open:

```text
dashboard/index.html
```

## Analysis Modules

### SQL Wide Table

The project integrates orders, customers, order items, products, payments, reviews, sellers, and category translation into an analytical wide table.

Important modeling detail:

- Order-level payment value is aggregated before joining to item-level records.
- This avoids inflated GMV caused by one-to-many joins between orders, items, and payments.

### Revenue Analysis

Metrics:

- GMV
- AOV
- orders
- customers
- monthly trend
- category contribution
- state contribution

### Cohort Retention

Customers are grouped by first purchase month. Retention is measured by whether customers place another delivered order in later months.

### RFM Segmentation

Customers are segmented by:

- Recency: days since last purchase
- Frequency: number of delivered orders
- Monetary: total payment value

Segments include:

- Champions
- Loyal Customers
- Potential Loyalists
- At Risk
- Dormant
- One-time / Mid Value

### Customer Satisfaction

Review score is analyzed against:

- delivery delay bucket
- product category
- customer state
- delivery days

### Opportunity Sizing

The project estimates directional GMV impact for scenarios such as:

- winning back 5% of At Risk customers
- increasing month-1 retention by 1 percentage point
- reducing delayed-order GMV exposure
- converting Potential Loyalists into second-order customers

## Resume Project Name

Marketplace Revenue, Retention and Experience Analytics

