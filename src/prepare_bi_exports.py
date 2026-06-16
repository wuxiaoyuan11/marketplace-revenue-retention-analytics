from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
PROCESSED_DIR = ROOT / "data" / "processed"
BI_DIR = ROOT / "dashboard" / "bi_export"


EXPORTS = {
    "monthly_revenue": {
        "source": "monthly_revenue.csv",
        "columns": ["month", "orders", "customers", "gmv", "aov", "avg_review_score"],
    },
    "category_revenue": {
        "source": "category_revenue.csv",
        "columns": ["product_category", "orders", "customers", "gmv", "aov", "avg_review_score"],
    },
    "state_revenue": {
        "source": "state_revenue.csv",
        "columns": [
            "customer_state",
            "orders",
            "customers",
            "gmv",
            "aov",
            "avg_delivery_days",
            "avg_review_score",
        ],
    },
    "cohort_retention": {
        "source": "cohort_retention.csv",
        "columns": [
            "cohort_month",
            "month_number",
            "active_customers",
            "cohort_customers",
            "retention_rate",
        ],
    },
    "rfm_segment_summary": {
        "source": "rfm_segment_summary.csv",
        "columns": [
            "rfm_segment",
            "customers",
            "avg_recency_days",
            "avg_frequency",
            "avg_monetary",
            "total_gmv",
        ],
    },
    "delivery_review": {
        "source": "review_delivery_analysis.csv",
        "columns": ["delivery_delay_bucket", "orders", "avg_review_score", "gmv"],
    },
    "category_satisfaction": {
        "source": "category_satisfaction.csv",
        "columns": [
            "product_category",
            "orders",
            "gmv",
            "avg_review_score",
            "avg_delivery_days",
            "avg_delivery_delay_days",
        ],
    },
    "state_satisfaction": {
        "source": "state_satisfaction.csv",
        "columns": [
            "customer_state",
            "orders",
            "gmv",
            "avg_review_score",
            "avg_delivery_days",
            "avg_delivery_delay_days",
        ],
    },
    "opportunity_sizing": {
        "source": "opportunity_sizing.csv",
        "columns": [
            "scenario",
            "baseline",
            "assumption",
            "estimated_gmv_impact",
            "impact_as_pct_of_total_gmv",
            "strategic_use",
        ],
    },
    "gmv_metric_tree": {
        "source": "gmv_metric_tree.csv",
        "columns": ["metric", "value", "definition"],
    },
}

SHORT_SCENARIOS = {
    "Win back 5% of At Risk customers": "At Risk win-back",
    "Increase month-1 retention by 1 percentage point": "Month-1 retention lift",
    "Reduce all delayed order GMV by 10%": "Delayed order reduction",
    "Reduce 8+ day delayed order GMV by 20%": "Severe delay reduction",
    "Win back 3% of Dormant customers": "Dormant win-back",
    "Convert 10% of Potential Loyalists to a second order": "Potential loyalist conversion",
}


DATA_DICTIONARY = [
    ("month", "Month of order purchase", "monthly_revenue"),
    ("orders", "Number of delivered orders", "multiple"),
    ("customers", "Number of unique purchasing customers", "multiple"),
    ("gmv", "Gross merchandise volume / order payment value", "multiple"),
    ("aov", "Average order value, calculated as GMV divided by orders", "multiple"),
    ("avg_review_score", "Average customer review score from 1 to 5", "multiple"),
    ("product_category", "English product category name", "category tables"),
    ("customer_state", "Brazil customer state abbreviation", "state tables"),
    ("cohort_month", "Month of customer's first purchase", "cohort_retention"),
    ("month_number", "Months since first purchase", "cohort_retention"),
    ("retention_rate", "Active customers divided by original cohort size", "cohort_retention"),
    ("rfm_segment", "Customer segment based on recency, frequency, and monetary value", "rfm_segment_summary"),
    ("avg_recency_days", "Average days since last purchase for the RFM segment", "rfm_segment_summary"),
    ("avg_frequency", "Average delivered order count for the RFM segment", "rfm_segment_summary"),
    ("avg_monetary", "Average historical monetary value for the RFM segment", "rfm_segment_summary"),
    ("total_gmv", "Total historical GMV contributed by the RFM segment", "rfm_segment_summary"),
    ("delivery_delay_bucket", "Delivery delay bucket based on estimated vs actual delivery date", "delivery_review"),
    ("avg_delivery_days", "Average days from purchase to customer delivery", "satisfaction tables"),
    ("avg_delivery_delay_days", "Average difference between estimated and actual delivery date", "satisfaction tables"),
    ("scenario", "Business opportunity scenario", "opportunity_sizing"),
    ("estimated_gmv_impact", "Directional GMV impact under the scenario assumption", "opportunity_sizing"),
    ("impact_as_pct_of_total_gmv", "Estimated GMV impact divided by total GMV", "opportunity_sizing"),
]


def clean_for_bi(df: pd.DataFrame) -> pd.DataFrame:
    cleaned = df.copy()
    for col in cleaned.select_dtypes(include=["object"]).columns:
        cleaned[col] = cleaned[col].fillna("Unknown")
    return cleaned


def main() -> None:
    BI_DIR.mkdir(parents=True, exist_ok=True)

    for export_name, spec in EXPORTS.items():
        df = pd.read_csv(PROCESSED_DIR / spec["source"])
        df = clean_for_bi(df[spec["columns"]])
        df.to_csv(BI_DIR / f"{export_name}.csv", index=False)

        if export_name == "opportunity_sizing":
            tableau_df = df.copy()
            tableau_df["short_scenario"] = tableau_df["scenario"].map(SHORT_SCENARIOS).fillna(
                tableau_df["scenario"]
            )
            tableau_df = tableau_df[
                [
                    "short_scenario",
                    "scenario",
                    "baseline",
                    "assumption",
                    "estimated_gmv_impact",
                    "impact_as_pct_of_total_gmv",
                    "strategic_use",
                ]
            ]
            tableau_df.to_csv(BI_DIR / "opportunity_sizing_tableau.csv", index=False)

    dictionary = pd.DataFrame(DATA_DICTIONARY, columns=["field", "definition", "used_in"])
    dictionary.to_csv(BI_DIR / "data_dictionary.csv", index=False)

    print(f"Saved BI-ready files to: {BI_DIR}")


if __name__ == "__main__":
    main()
