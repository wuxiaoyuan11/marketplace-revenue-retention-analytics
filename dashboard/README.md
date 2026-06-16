# Dashboard Guide

Open this file in a browser:

```text
dashboard/index.html
```

## What This Dashboard Shows

This dashboard summarizes the project into a portfolio-ready business view:

1. Executive KPIs
2. Revenue trend
3. Product category contribution
4. RFM customer segment value
5. Delivery delay and review score relationship
6. Cohort retention
7. Opportunity sizing
8. High-GMV categories with satisfaction risk

## How To Explain It In Interviews

Start with the business problem:

```text
I wanted to understand what drives marketplace GMV, why repeat purchase is weak, which customers should be prioritized for retention, and how logistics experience affects satisfaction.
```

Then explain the workflow:

```text
I used SQL to build analytical wide tables from orders, customers, products, payments, reviews, and delivery timestamps. Then I used Python to generate business metrics, RFM segments, cohort retention, and opportunity sizing scenarios.
```

Then highlight the strongest findings:

- The marketplace generated 15.42M delivered GMV.
- AOV is about 159.85, while orders per customer is only 1.03.
- Repeat customer rate is only 3.0%, so repeat purchase is a key growth bottleneck.
- At Risk customers contribute 4.53M historical GMV and are the largest modeled opportunity.
- A 5% At Risk win-back scenario could affect about 226.7K GMV.
- Severe 8+ day delivery delays have much lower review scores than on-time orders.

Then close with recommendations:

```text
I would prioritize At Risk win-back campaigns, post-first-purchase activation, and logistics SLA improvements for high-GMV categories and sellers.
```

