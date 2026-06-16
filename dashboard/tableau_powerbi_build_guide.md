# Tableau / Power BI Build Guide

This guide helps you build a portfolio-ready BI dashboard from the exported CSV files in:

```text
dashboard/bi_export/
```

Recommended tool: Tableau Public.

## 1. BI-Ready Data Files

Use these files as separate data sources:

```text
monthly_revenue.csv
category_revenue.csv
state_revenue.csv
cohort_retention.csv
rfm_segment_summary.csv
delivery_review.csv
category_satisfaction.csv
state_satisfaction.csv
opportunity_sizing.csv
opportunity_sizing_tableau.csv
gmv_metric_tree.csv
data_dictionary.csv
```

For a first portfolio version, you do not need to join the tables. Each file is already aggregated for a specific dashboard view.

## 2. Dashboard Structure

Build 3 dashboard pages:

1. Executive Overview
2. Customer Retention and RFM
3. Operations and Opportunity Sizing

Use a clean business style:

- White or very light background
- 3-5 KPI cards at the top
- Consistent blue/green/orange/red accent colors
- No decorative elements
- Clear chart titles with business meaning

## 3. Page 1: Executive Overview

Purpose: show overall marketplace performance.

Data source:

```text
monthly_revenue.csv
category_revenue.csv
state_revenue.csv
```

### KPI Cards

Create these calculated / aggregated KPIs:

- Total GMV: `SUM(gmv)` from `monthly_revenue.csv`
- Orders: `SUM(orders)` from `monthly_revenue.csv`
- Customers: `SUM(customers)` from `monthly_revenue.csv`
- AOV: `SUM(gmv) / SUM(orders)`
- Average Review Score: `AVG(avg_review_score)`

### Chart 1: Monthly GMV Trend

Data source: `monthly_revenue.csv`

Tableau:

- Columns: `month`
- Rows: `gmv`
- Marks: Line
- Tooltip: month, GMV, orders, AOV, avg review score

Power BI:

- Visual: Line chart
- X-axis: `month`
- Y-axis: `gmv`
- Tooltips: `orders`, `aov`, `avg_review_score`

Business message:

```text
GMV grew through 2017 and peaked around the year-end shopping period.
```

### Chart 2: Top Product Categories by GMV

Data source: `category_revenue.csv`

Tableau:

- Rows: `product_category`
- Columns: `gmv`
- Sort: descending by GMV
- Filter: Top 10 by GMV
- Marks: Bar

Power BI:

- Visual: Bar chart
- Y-axis: `product_category`
- X-axis: `gmv`
- Filter: Top 10

Business message:

```text
GMV is concentrated in a small number of categories, especially health_beauty, watches_gifts, and bed_bath_table.
```

### Chart 3: GMV by State

Data source: `state_revenue.csv`

Option A:

- Bar chart by `customer_state`
- Sort by `gmv`

Option B:

- Filled map if your BI tool recognizes Brazilian state abbreviations

Business message:

```text
Regional performance differs significantly, so logistics and marketing should be managed by geography.
```

## 4. Page 2: Customer Retention and RFM

Purpose: show user behavior, retention, and customer value segmentation.

Data source:

```text
cohort_retention.csv
rfm_segment_summary.csv
```

### Chart 1: Cohort Retention Heatmap

Data source: `cohort_retention.csv`

Tableau:

- Rows: `cohort_month`
- Columns: `month_number`
- Color: `retention_rate`
- Label: `retention_rate`
- Format as percentage

Power BI:

- Visual: Matrix
- Rows: `cohort_month`
- Columns: `month_number`
- Values: `retention_rate`
- Conditional formatting: background color

Business message:

```text
Month-1 retention is low, so post-first-purchase activation is a major growth lever.
```

### Chart 2: GMV by RFM Segment

Data source: `rfm_segment_summary.csv`

Tableau:

- Columns: `rfm_segment`
- Rows: `total_gmv`
- Marks: Bar
- Color: `rfm_segment`
- Sort descending by GMV

Power BI:

- Visual: Column chart
- X-axis: `rfm_segment`
- Y-axis: `total_gmv`

Business message:

```text
Loyal Customers, At Risk customers, and Champions drive most customer value.
```

### Chart 3: Customer Count vs Avg Monetary by Segment

Data source: `rfm_segment_summary.csv`

Tableau:

- Columns: `customers`
- Rows: `avg_monetary`
- Size: `total_gmv`
- Color: `rfm_segment`
- Marks: Circle

Business message:

```text
At Risk customers are valuable because they combine meaningful scale with high historical monetary value.
```

## 5. Page 3: Operations and Opportunity Sizing

Purpose: connect customer experience problems to business actions.

Data source:

```text
delivery_review.csv
category_satisfaction.csv
state_satisfaction.csv
opportunity_sizing.csv
```

### Chart 1: Delivery Delay vs Review Score

Data source: `delivery_review.csv`

Tableau:

- Columns: `delivery_delay_bucket`
- Rows: `avg_review_score`
- Marks: Bar
- Sort manually:
  1. On time / Early
  2. Delayed 1-3 days
  3. Delayed 4-7 days
  4. Delayed 8+ days
  5. Unknown

Business message:

```text
Severe delays are strongly associated with lower review scores.
```

### Chart 2: High-GMV Low-Satisfaction Categories

Data source: `category_satisfaction.csv`

Tableau:

- Columns: `gmv`
- Rows: `avg_review_score`
- Detail: `product_category`
- Size: `orders`
- Color: `avg_delivery_days`
- Marks: Circle

Alternative:

- Table sorted by `avg_review_score` ascending and `gmv` descending

Business message:

```text
High-GMV but low-rating categories should be fixed before increasing marketing investment.
```

### Chart 3: Opportunity Sizing Bar Chart

Data source: `opportunity_sizing.csv`

For Tableau display, use `opportunity_sizing_tableau.csv` because it includes `short_scenario` for cleaner chart labels.

Tableau:

- Rows: `short_scenario`
- Columns: `estimated_gmv_impact`
- Sort descending
- Label: `estimated_gmv_impact`
- Tooltip: `scenario`, `baseline`, `assumption`, `strategic_use`, `impact_as_pct_of_total_gmv`

Business message:

```text
At Risk customer win-back is the largest modeled opportunity, followed by month-1 retention lift.
```

## 6. Suggested Dashboard Titles

Use one of:

```text
Marketplace Revenue, Retention and Experience Analytics
```

or:

```text
E-commerce Growth and Customer Retention Dashboard
```

## 7. Final Interview Talk Track

Use this 45-second version:

```text
I built a marketplace analytics dashboard using SQL, Python, DuckDB, and Tableau-ready data exports. The analysis starts from a GMV metric tree, then breaks performance down by product category, region, customer RFM segment, cohort retention, and delivery experience. 

The key finding is that the platform has strong customer scale but weak repeat behavior: AOV is about 159.85, orders per customer are only 1.03, and repeat customer rate is about 3.0%. RFM analysis shows that At Risk customers contributed 4.53M historical GMV, and opportunity sizing suggests that winning back 5% of this segment could affect about 226.7K GMV. 

I also found that severe delivery delays are strongly associated with low review scores, so my recommendations focus on At Risk win-back, post-first-purchase activation, and logistics SLA improvements in high-GMV categories.
```
