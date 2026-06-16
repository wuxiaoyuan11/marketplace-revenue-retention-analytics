# Tableau Quick Start

Use this if you want the fastest Tableau Public version.

## Step 1: Open Tableau Public

Open Tableau Public, then choose:

```text
Connect -> Text file
```

Connect the CSV files from:

```text
dashboard/bi_export/
```

For the first version, connect one file per sheet. Do not spend time joining tables.

## Step 2: Build These 6 Sheets

### Sheet 1: Monthly GMV

File:

```text
monthly_revenue.csv
```

Fields:

- Columns: `month`
- Rows: `gmv`
- Marks: Line

### Sheet 2: Top Categories

File:

```text
category_revenue.csv
```

Fields:

- Rows: `product_category`
- Columns: `gmv`
- Sort: descending
- Filter: Top 10 by GMV
- Marks: Bar

### Sheet 3: Cohort Retention

File:

```text
cohort_retention.csv
```

Fields:

- Rows: `cohort_month`
- Columns: `month_number`
- Color: `retention_rate`
- Label: `retention_rate`
- Format: percentage

### Sheet 4: RFM Segment GMV

File:

```text
rfm_segment_summary.csv
```

Fields:

- Columns: `rfm_segment`
- Rows: `total_gmv`
- Marks: Bar
- Sort: descending

### Sheet 5: Delivery Delay and Review Score

File:

```text
delivery_review.csv
```

Fields:

- Columns: `delivery_delay_bucket`
- Rows: `avg_review_score`
- Marks: Bar

### Sheet 6: Opportunity Sizing

File:

```text
opportunity_sizing_tableau.csv
```

Fields:

- Rows: `short_scenario`
- Columns: `estimated_gmv_impact`
- Marks: Bar
- Sort: descending
- Tooltip: `scenario`, `baseline`, `assumption`, `strategic_use`, `impact_as_pct_of_total_gmv`

## Step 3: Build 3 Dashboards

### Dashboard 1: Executive Overview

Add:

- Monthly GMV
- Top Categories
- GMV by State, optional from `state_revenue.csv`
- KPI cards: Total GMV, Orders, Customers, AOV

### Dashboard 2: Retention and RFM

Add:

- Cohort Retention
- RFM Segment GMV
- Customer Count vs Avg Monetary, optional

### Dashboard 3: Operations and Opportunities

Add:

- Delivery Delay and Review Score
- High-GMV Low-Satisfaction Categories, from `category_satisfaction.csv`
- Opportunity Sizing

## Step 4: Publish

In Tableau Public:

```text
File -> Save to Tableau Public
```

Use this project title:

```text
Marketplace Revenue, Retention and Experience Analytics
```

After publishing, copy the Tableau Public URL and add it to your resume and GitHub README.
