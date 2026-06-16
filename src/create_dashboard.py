from html import escape
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
PROCESSED_DIR = ROOT / "data" / "processed"
DASHBOARD_DIR = ROOT / "dashboard"
OUTPUT_PATH = DASHBOARD_DIR / "index.html"


def fmt_money(value: float) -> str:
    if abs(value) >= 1_000_000:
        return f"{value / 1_000_000:.2f}M"
    if abs(value) >= 1_000:
        return f"{value / 1_000:.1f}K"
    return f"{value:,.0f}"


def fmt_number(value: float) -> str:
    return f"{value:,.0f}"


def fmt_pct(value: float) -> str:
    return f"{value:.1%}"


def table_html(df: pd.DataFrame, money_cols=None, pct_cols=None, max_rows=8) -> str:
    money_cols = set(money_cols or [])
    pct_cols = set(pct_cols or [])
    rows = []
    for _, row in df.head(max_rows).iterrows():
        cells = []
        for col in df.columns:
            value = row[col]
            if pd.isna(value):
                text = "-"
            elif col in money_cols:
                text = fmt_money(float(value))
            elif col in pct_cols:
                text = fmt_pct(float(value))
            elif isinstance(value, float):
                text = f"{value:,.2f}"
            else:
                text = str(value)
            cells.append(f"<td>{escape(text)}</td>")
        rows.append("<tr>" + "".join(cells) + "</tr>")

    headers = "".join(f"<th>{escape(str(col).replace('_', ' ').title())}</th>" for col in df.columns)
    return f"""
    <table>
      <thead><tr>{headers}</tr></thead>
      <tbody>{''.join(rows)}</tbody>
    </table>
    """


def kpi_card(label: str, value: str, note: str) -> str:
    return f"""
    <article class="kpi">
      <span>{escape(label)}</span>
      <strong>{escape(value)}</strong>
      <small>{escape(note)}</small>
    </article>
    """


def figure_card(title: str, src: str, caption: str) -> str:
    return f"""
    <section class="figure-block">
      <h3>{escape(title)}</h3>
      <img src="{escape(src)}" alt="{escape(title)}">
      <p>{escape(caption)}</p>
    </section>
    """


def main() -> None:
    metric_tree = pd.read_csv(PROCESSED_DIR / "gmv_metric_tree.csv")
    opportunities = pd.read_csv(PROCESSED_DIR / "opportunity_sizing.csv")
    category_revenue = pd.read_csv(PROCESSED_DIR / "category_revenue.csv")
    rfm = pd.read_csv(PROCESSED_DIR / "rfm_segment_summary.csv")
    delivery = pd.read_csv(PROCESSED_DIR / "review_delivery_analysis.csv")
    category_satisfaction = pd.read_csv(PROCESSED_DIR / "category_satisfaction.csv")

    metrics = dict(zip(metric_tree["metric"], metric_tree["value"]))
    top_category = category_revenue.iloc[0]
    at_risk = rfm.loc[rfm["rfm_segment"].eq("At Risk")].iloc[0]
    severe_delay = delivery.loc[delivery["delivery_delay_bucket"].eq("Delayed 8+ days")].iloc[0]
    on_time = delivery.loc[delivery["delivery_delay_bucket"].eq("On time / Early")].iloc[0]
    best_opportunity = opportunities.iloc[0]

    kpis = [
        kpi_card("Total GMV", fmt_money(metrics["Total GMV"]), "Delivered order payment value"),
        kpi_card("Orders", fmt_number(metrics["Orders"]), "Delivered orders"),
        kpi_card("Customers", fmt_number(metrics["Customers"]), "Unique purchasing customers"),
        kpi_card("AOV", fmt_money(metrics["AOV"]), "GMV / orders"),
        kpi_card("Repeat Rate", fmt_pct(metrics["Repeat customer rate"]), "Customers with 2+ orders"),
        kpi_card("Top Category", str(top_category["product_category"]), f"{fmt_money(top_category['gmv'])} GMV"),
        kpi_card("At Risk GMV", fmt_money(at_risk["total_gmv"]), "High-value reactivation segment"),
        kpi_card("Best Sized Opportunity", fmt_money(best_opportunity["estimated_gmv_impact"]), best_opportunity["scenario"]),
    ]

    category_table = category_revenue[
        ["product_category", "gmv", "orders", "aov", "avg_review_score"]
    ].head(8)
    rfm_table = rfm[
        ["rfm_segment", "customers", "avg_recency_days", "avg_frequency", "avg_monetary", "total_gmv"]
    ]
    opportunity_table = opportunities[
        ["scenario", "estimated_gmv_impact", "impact_as_pct_of_total_gmv", "strategic_use"]
    ]
    risk_category_table = (
        category_satisfaction[category_satisfaction["gmv"] > category_satisfaction["gmv"].median()]
        .sort_values(["avg_review_score", "gmv"], ascending=[True, False])
        [["product_category", "gmv", "orders", "avg_review_score", "avg_delivery_days"]]
        .head(8)
    )

    html = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>E-commerce Revenue Analytics Dashboard</title>
  <style>
    :root {{
      --ink: #172033;
      --muted: #5b6578;
      --line: #d9dee8;
      --bg: #f6f7f9;
      --panel: #ffffff;
      --blue: #2563eb;
      --green: #0f9f6e;
      --amber: #c47a0b;
      --red: #c2413b;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      color: var(--ink);
      background: var(--bg);
      font-family: Inter, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      line-height: 1.45;
    }}
    header {{
      padding: 36px 40px 28px;
      background: #ffffff;
      border-bottom: 1px solid var(--line);
    }}
    header h1 {{
      margin: 0;
      max-width: 1120px;
      font-size: 34px;
      line-height: 1.15;
      letter-spacing: 0;
    }}
    header p {{
      max-width: 980px;
      margin: 12px 0 0;
      color: var(--muted);
      font-size: 16px;
    }}
    main {{
      max-width: 1280px;
      margin: 0 auto;
      padding: 28px 24px 48px;
    }}
    h2 {{
      margin: 34px 0 14px;
      font-size: 22px;
      letter-spacing: 0;
    }}
    h3 {{
      margin: 0 0 14px;
      font-size: 17px;
      letter-spacing: 0;
    }}
    .kpi-grid {{
      display: grid;
      grid-template-columns: repeat(4, minmax(0, 1fr));
      gap: 12px;
    }}
    .kpi {{
      min-height: 116px;
      padding: 16px;
      background: var(--panel);
      border: 1px solid var(--line);
      border-radius: 8px;
    }}
    .kpi span {{
      display: block;
      color: var(--muted);
      font-size: 13px;
    }}
    .kpi strong {{
      display: block;
      margin-top: 8px;
      font-size: 25px;
      line-height: 1.2;
    }}
    .kpi small {{
      display: block;
      margin-top: 8px;
      color: var(--muted);
      font-size: 12px;
    }}
    .figure-grid {{
      display: grid;
      grid-template-columns: repeat(2, minmax(0, 1fr));
      gap: 16px;
    }}
    .figure-block, .table-block, .insight-block {{
      background: var(--panel);
      border: 1px solid var(--line);
      border-radius: 8px;
      padding: 18px;
    }}
    .figure-block img {{
      width: 100%;
      height: auto;
      display: block;
      border: 1px solid #edf0f5;
      border-radius: 6px;
    }}
    .figure-block p, .insight-block p, .insight-block li {{
      color: var(--muted);
      font-size: 14px;
    }}
    .table-grid {{
      display: grid;
      grid-template-columns: 1fr;
      gap: 16px;
    }}
    table {{
      width: 100%;
      border-collapse: collapse;
      font-size: 13px;
    }}
    th, td {{
      padding: 10px 9px;
      border-bottom: 1px solid #edf0f5;
      text-align: left;
      vertical-align: top;
    }}
    th {{
      color: var(--muted);
      font-weight: 650;
      background: #fbfcfd;
    }}
    td:nth-child(n+2), th:nth-child(n+2) {{
      text-align: right;
    }}
    .insight-grid {{
      display: grid;
      grid-template-columns: repeat(3, minmax(0, 1fr));
      gap: 16px;
    }}
    .tag {{
      display: inline-block;
      margin-bottom: 10px;
      padding: 4px 8px;
      border-radius: 999px;
      color: #ffffff;
      font-size: 12px;
      font-weight: 650;
    }}
    .tag.blue {{ background: var(--blue); }}
    .tag.green {{ background: var(--green); }}
    .tag.red {{ background: var(--red); }}
    footer {{
      max-width: 1280px;
      margin: 0 auto;
      padding: 0 24px 34px;
      color: var(--muted);
      font-size: 12px;
    }}
    @media (max-width: 920px) {{
      header {{ padding: 28px 22px 22px; }}
      header h1 {{ font-size: 27px; }}
      .kpi-grid, .figure-grid, .insight-grid {{ grid-template-columns: 1fr; }}
      main {{ padding: 20px 14px 36px; }}
      table {{ font-size: 12px; }}
    }}
  </style>
</head>
<body>
  <header>
    <h1>E-commerce User Behavior and Revenue Analytics</h1>
    <p>Marketplace analytics dashboard built from SQL outputs on the Olist dataset. It connects revenue drivers, user segmentation, retention, logistics experience, and opportunity sizing.</p>
  </header>
  <main>
    <section class="kpi-grid">
      {''.join(kpis)}
    </section>

    <h2>Revenue, Retention, and Experience Trends</h2>
    <section class="figure-grid">
      {figure_card("Monthly GMV Trend", "../reports/figures/01_monthly_gmv_trend.png", "GMV grew strongly through 2017 and peaked around the year-end shopping period.")}
      {figure_card("Top Product Categories by GMV", "../reports/figures/02_top_category_gmv.png", "Revenue is concentrated in a small set of categories such as health_beauty, watches_gifts, and bed_bath_table.")}
      {figure_card("GMV by RFM Segment", "../reports/figures/03_rfm_segment_gmv.png", "Loyal Customers, At Risk customers, and Champions drive the majority of customer value.")}
      {figure_card("Review Score by Delivery Delay", "../reports/figures/04_delivery_delay_review_score.png", f"On-time orders average {on_time['avg_review_score']:.2f} stars, while 8+ day delayed orders average {severe_delay['avg_review_score']:.2f} stars.")}
      {figure_card("Cohort Retention Heatmap", "../reports/figures/05_cohort_retention_heatmap.png", "Retention is weak after first purchase, highlighting a lifecycle activation opportunity.")}
    </section>

    <h2>Business Interpretation</h2>
    <section class="insight-grid">
      <article class="insight-block">
        <span class="tag blue">Growth</span>
        <h3>GMV needs repeat-purchase lift</h3>
        <p>The marketplace has {fmt_number(metrics["Customers"])} purchasing customers but only {fmt_pct(metrics["Repeat customer rate"])} repeat customer rate. Growth should focus on converting first-time buyers into second purchases.</p>
      </article>
      <article class="insight-block">
        <span class="tag green">Retention</span>
        <h3>At Risk users are high-value</h3>
        <p>At Risk customers represent {fmt_money(at_risk["total_gmv"])} historical GMV. A 5% win-back scenario is the largest modeled opportunity at {fmt_money(best_opportunity["estimated_gmv_impact"])} GMV.</p>
      </article>
      <article class="insight-block">
        <span class="tag red">Experience</span>
        <h3>Severe delays hurt trust</h3>
        <p>Orders delayed 8+ days have much lower review scores than on-time orders. Logistics improvements should focus on high-GMV categories and sellers with recurring delay risk.</p>
      </article>
    </section>

    <h2>Tables for Decision Making</h2>
    <section class="table-grid">
      <div class="table-block">
        <h3>Top Categories by GMV</h3>
        {table_html(category_table, money_cols=["gmv", "aov"])}
      </div>
      <div class="table-block">
        <h3>RFM Segment Summary</h3>
        {table_html(rfm_table, money_cols=["avg_monetary", "total_gmv"])}
      </div>
      <div class="table-block">
        <h3>Opportunity Sizing</h3>
        {table_html(opportunity_table, money_cols=["estimated_gmv_impact"], pct_cols=["impact_as_pct_of_total_gmv"], max_rows=6)}
      </div>
      <div class="table-block">
        <h3>High-GMV Categories With Satisfaction Risk</h3>
        {table_html(risk_category_table, money_cols=["gmv"])}
      </div>
    </section>
  </main>
  <footer>
    Generated from SQL and Python outputs in this repository. Dataset: Brazilian E-Commerce Public Dataset by Olist.
  </footer>
</body>
</html>
"""

    DASHBOARD_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(html)
    print(f"Saved dashboard to: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()

