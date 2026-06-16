from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


ROOT = Path(__file__).resolve().parents[1]
PROCESSED_DIR = ROOT / "data" / "processed"
FIGURE_DIR = ROOT / "reports" / "figures"


def money_axis(ax) -> None:
    ax.yaxis.set_major_formatter(lambda x, _: f"{x / 1_000_000:.1f}M")


def save_plot(filename: str) -> None:
    FIGURE_DIR.mkdir(parents=True, exist_ok=True)
    plt.tight_layout()
    plt.savefig(FIGURE_DIR / filename, dpi=200, bbox_inches="tight")
    plt.close()


def plot_monthly_gmv() -> None:
    df = pd.read_csv(PROCESSED_DIR / "monthly_revenue.csv", parse_dates=["month"])
    df = df.dropna(subset=["gmv"])

    plt.figure(figsize=(11, 5))
    ax = sns.lineplot(data=df, x="month", y="gmv", marker="o", color="#2563eb")
    ax.set_title("Monthly GMV Trend")
    ax.set_xlabel("Month")
    ax.set_ylabel("GMV")
    money_axis(ax)
    ax.grid(axis="y", alpha=0.25)
    save_plot("01_monthly_gmv_trend.png")


def plot_top_category_gmv() -> None:
    df = pd.read_csv(PROCESSED_DIR / "category_revenue.csv").head(10)

    plt.figure(figsize=(11, 6))
    ax = sns.barplot(data=df, y="product_category", x="gmv", color="#10b981")
    ax.set_title("Top 10 Product Categories by GMV")
    ax.set_xlabel("GMV")
    ax.set_ylabel("Product Category")
    ax.xaxis.set_major_formatter(lambda x, _: f"{x / 1_000:.0f}K")
    ax.grid(axis="x", alpha=0.25)
    save_plot("02_top_category_gmv.png")


def plot_rfm_segment_gmv() -> None:
    df = pd.read_csv(PROCESSED_DIR / "rfm_segment_summary.csv")
    df = df.sort_values("total_gmv", ascending=False)

    plt.figure(figsize=(11, 5))
    ax = sns.barplot(data=df, x="rfm_segment", y="total_gmv", color="#f59e0b")
    ax.set_title("GMV Contribution by RFM Segment")
    ax.set_xlabel("RFM Segment")
    ax.set_ylabel("Total GMV")
    money_axis(ax)
    ax.tick_params(axis="x", rotation=20)
    ax.grid(axis="y", alpha=0.25)
    save_plot("03_rfm_segment_gmv.png")


def plot_delivery_review() -> None:
    df = pd.read_csv(PROCESSED_DIR / "review_delivery_analysis.csv")
    order = [
        "On time / Early",
        "Delayed 1-3 days",
        "Delayed 4-7 days",
        "Delayed 8+ days",
        "Unknown",
    ]
    df["delivery_delay_bucket"] = pd.Categorical(
        df["delivery_delay_bucket"], categories=order, ordered=True
    )
    df = df.sort_values("delivery_delay_bucket")

    plt.figure(figsize=(10, 5))
    ax = sns.barplot(
        data=df,
        x="delivery_delay_bucket",
        y="avg_review_score",
        color="#ef4444",
    )
    ax.set_title("Average Review Score by Delivery Delay")
    ax.set_xlabel("Delivery Delay Bucket")
    ax.set_ylabel("Average Review Score")
    ax.set_ylim(0, 5)
    ax.tick_params(axis="x", rotation=20)
    ax.grid(axis="y", alpha=0.25)
    save_plot("04_delivery_delay_review_score.png")


def plot_cohort_retention() -> None:
    df = pd.read_csv(PROCESSED_DIR / "cohort_retention.csv", parse_dates=["cohort_month"])
    df = df[df["month_number"].between(0, 12)]
    pivot = df.pivot_table(
        index=df["cohort_month"].dt.strftime("%Y-%m"),
        columns="month_number",
        values="retention_rate",
        aggfunc="mean",
    )

    plt.figure(figsize=(12, 7))
    ax = sns.heatmap(
        pivot,
        cmap="Blues",
        annot=True,
        fmt=".1%",
        linewidths=0.4,
        cbar_kws={"label": "Retention Rate"},
    )
    ax.set_title("Monthly Cohort Retention")
    ax.set_xlabel("Months Since First Purchase")
    ax.set_ylabel("First Purchase Cohort")
    save_plot("05_cohort_retention_heatmap.png")


def main() -> None:
    plot_monthly_gmv()
    plot_top_category_gmv()
    plot_rfm_segment_gmv()
    plot_delivery_review()
    plot_cohort_retention()
    print(f"Saved figures to: {FIGURE_DIR}")


if __name__ == "__main__":
    main()
