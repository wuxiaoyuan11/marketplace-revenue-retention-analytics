from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
PROCESSED_DIR = ROOT / "data" / "processed"
REPORT_DIR = ROOT / "reports"


def money(value: float) -> str:
    return f"{value:,.0f}"


def pct(value: float) -> str:
    return f"{value:.1%}"


def metric_value(metric: str, value: float) -> str:
    if "rate" in metric.lower():
        return pct(value)
    if metric in {"AOV", "Orders per customer", "GMV per customer"}:
        return f"{value:,.2f}"
    return money(value)


def load_order_level() -> pd.DataFrame:
    wide = pd.read_csv(
        PROCESSED_DIR / "order_item_wide.csv",
        parse_dates=["purchase_ts"],
        low_memory=False,
    )
    order_cols = [
        "order_id",
        "customer_unique_id",
        "customer_state",
        "order_status",
        "purchase_ts",
        "order_payment_value",
        "review_score",
        "delivery_days",
        "delivery_delay_days",
    ]
    order_level = wide[order_cols].drop_duplicates("order_id")
    return order_level[order_level["order_status"].eq("delivered")].copy()


def build_metric_tree(order_level: pd.DataFrame) -> pd.DataFrame:
    total_gmv = order_level["order_payment_value"].sum()
    orders = order_level["order_id"].nunique()
    customers = order_level["customer_unique_id"].nunique()
    aov = total_gmv / orders
    orders_per_customer = orders / customers
    gmv_per_customer = total_gmv / customers
    repeat_customers = (
        order_level.groupby("customer_unique_id")["order_id"].nunique().loc[lambda s: s >= 2].count()
    )
    repeat_customer_rate = repeat_customers / customers

    metrics = [
        ("Total GMV", total_gmv, "Delivered order payment value"),
        ("Orders", orders, "Number of delivered orders"),
        ("Customers", customers, "Unique purchasing customers"),
        ("AOV", aov, "GMV / orders"),
        ("Orders per customer", orders_per_customer, "Orders / customers"),
        ("GMV per customer", gmv_per_customer, "GMV / customers"),
        ("Repeat customers", repeat_customers, "Customers with 2+ delivered orders"),
        ("Repeat customer rate", repeat_customer_rate, "Repeat customers / customers"),
    ]
    return pd.DataFrame(metrics, columns=["metric", "value", "definition"])


def size_opportunities(order_level: pd.DataFrame) -> pd.DataFrame:
    rfm = pd.read_csv(PROCESSED_DIR / "rfm_segment_summary.csv")
    cohort = pd.read_csv(PROCESSED_DIR / "cohort_retention.csv")
    delivery = pd.read_csv(PROCESSED_DIR / "review_delivery_analysis.csv")

    total_gmv = order_level["order_payment_value"].sum()
    aov = total_gmv / order_level["order_id"].nunique()

    at_risk = rfm.loc[rfm["rfm_segment"].eq("At Risk")].iloc[0]
    at_risk_customers = at_risk["customers"]
    at_risk_avg_monetary = at_risk["avg_monetary"]

    dormant = rfm.loc[rfm["rfm_segment"].eq("Dormant")].iloc[0]
    potential = rfm.loc[rfm["rfm_segment"].eq("Potential Loyalists")].iloc[0]

    month1_retention = cohort.loc[cohort["month_number"].eq(1), "retention_rate"].mean()
    cohort0_customers = cohort.loc[cohort["month_number"].eq(0), "cohort_customers"].sum()

    delayed_8 = delivery.loc[delivery["delivery_delay_bucket"].eq("Delayed 8+ days")].iloc[0]
    delayed_any = delivery[delivery["delivery_delay_bucket"].str.contains("Delayed")]

    scenarios = [
        {
            "scenario": "Win back 5% of At Risk customers",
            "baseline": f"{money(at_risk_customers)} At Risk customers; avg monetary {money(at_risk_avg_monetary)}",
            "assumption": "5% of At Risk users place one additional order at their historical average monetary value",
            "formula": "At Risk customers x 5% x At Risk avg monetary value",
            "estimated_gmv_impact": at_risk_customers * 0.05 * at_risk_avg_monetary,
            "strategic_use": "Retention campaign sizing",
            "validation_plan": "Run a holdout-based win-back test and measure incremental conversion, GMV, and margin versus control.",
        },
        {
            "scenario": "Win back 3% of Dormant customers",
            "baseline": f"{money(dormant['customers'])} Dormant customers; avg monetary {money(dormant['avg_monetary'])}",
            "assumption": "3% of Dormant users return with one order at their historical average monetary value",
            "formula": "Dormant customers x 3% x Dormant avg monetary value",
            "estimated_gmv_impact": dormant["customers"] * 0.03 * dormant["avg_monetary"],
            "strategic_use": "Low-cost reactivation test",
            "validation_plan": "Test low-cost reactivation coupons and compare reactivation rate, subsidy cost, and incremental GMV.",
        },
        {
            "scenario": "Convert 10% of Potential Loyalists to a second order",
            "baseline": f"{money(potential['customers'])} Potential Loyalists; platform AOV {money(aov)}",
            "assumption": "10% place a second order at platform AOV",
            "formula": "Potential Loyalist customers x 10% x platform AOV",
            "estimated_gmv_impact": potential["customers"] * 0.10 * aov,
            "strategic_use": "Post-first-purchase activation",
            "validation_plan": "Measure second-order conversion lift from post-delivery lifecycle campaigns against a control group.",
        },
        {
            "scenario": "Increase month-1 retention by 1 percentage point",
            "baseline": f"Current avg month-1 retention {pct(month1_retention)}",
            "assumption": "A +1pp lift creates additional retained customers who purchase at platform AOV",
            "formula": "Cohort customers x 1pp retention lift x platform AOV",
            "estimated_gmv_impact": cohort0_customers * 0.01 * aov,
            "strategic_use": "Lifecycle marketing target",
            "validation_plan": "Track month-1 retention, second-order GMV, and repeat purchase rate before and after lifecycle interventions.",
        },
        {
            "scenario": "Reduce 8+ day delayed order GMV by 20%",
            "baseline": f"{money(delayed_8['orders'])} orders; {money(delayed_8['gmv'])} delayed GMV; avg score {delayed_8['avg_review_score']:.2f}",
            "assumption": "20% of severe-delay GMV is moved into a healthier delivery experience",
            "formula": "8+ day delayed GMV x 20%",
            "estimated_gmv_impact": delayed_8["gmv"] * 0.20,
            "strategic_use": "SLA and seller operations sizing",
            "validation_plan": "Monitor SLA intervention sellers versus comparable sellers on delay rate, review score, and repeat purchase.",
        },
        {
            "scenario": "Reduce all delayed order GMV by 10%",
            "baseline": f"{money(delayed_any['orders'].sum())} delayed orders; {money(delayed_any['gmv'].sum())} delayed GMV",
            "assumption": "10% of delayed GMV is protected from severe dissatisfaction risk",
            "formula": "All delayed GMV x 10%",
            "estimated_gmv_impact": delayed_any["gmv"].sum() * 0.10,
            "strategic_use": "Logistics improvement target",
            "validation_plan": "Track delayed-order GMV exposure, complaint rate, review score, and downstream repeat purchase after SLA changes.",
        },
    ]

    out = pd.DataFrame(scenarios)
    out["impact_as_pct_of_total_gmv"] = out["estimated_gmv_impact"] / total_gmv
    return out.sort_values("estimated_gmv_impact", ascending=False)


def write_markdown(metric_tree: pd.DataFrame, opportunities: pd.DataFrame) -> None:
    metric_lines = []
    for _, row in metric_tree.iterrows():
        value = metric_value(row["metric"], row["value"])
        metric_lines.append(f"| {row['metric']} | {value} | {row['definition']} |")

    opportunity_lines = []
    formula_lines = []
    validation_lines = []
    for _, row in opportunities.iterrows():
        opportunity_lines.append(
            "| {scenario} | {impact} | {pct_total} | {assumption} |".format(
                scenario=row["scenario"],
                impact=money(row["estimated_gmv_impact"]),
                pct_total=pct(row["impact_as_pct_of_total_gmv"]),
                assumption=row["assumption"],
            )
        )
        formula_lines.append(f"| {row['scenario']} | {row['formula']} |")
        validation_lines.append(f"| {row['scenario']} | {row['validation_plan']} |")

    text = f"""# GMV Metric Tree and Opportunity Sizing

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
{chr(10).join(metric_lines)}

## Opportunity Sizing Scenarios

These are directional estimates, not causal experiment results. They are useful for prioritizing which initiatives are large enough to test.

| Scenario | Estimated GMV Impact | % of Total GMV | Assumption |
|---|---:|---:|---|
{chr(10).join(opportunity_lines)}

## Assumptions and Formulas

| Scenario | Formula |
|---|---|
{chr(10).join(formula_lines)}

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
{chr(10).join(validation_lines)}

"""
    (REPORT_DIR / "gmv_metric_tree_opportunity_sizing.md").write_text(text)


def main() -> None:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    order_level = load_order_level()
    metric_tree = build_metric_tree(order_level)
    opportunities = size_opportunities(order_level)

    metric_tree.to_csv(PROCESSED_DIR / "gmv_metric_tree.csv", index=False)
    opportunities.to_csv(PROCESSED_DIR / "opportunity_sizing.csv", index=False)
    write_markdown(metric_tree, opportunities)

    print("Saved data/processed/gmv_metric_tree.csv")
    print("Saved data/processed/opportunity_sizing.csv")
    print("Saved reports/gmv_metric_tree_opportunity_sizing.md")


if __name__ == "__main__":
    main()
