import os
from pathlib import Path

import duckdb


ROOT = Path(__file__).resolve().parents[1]
DB_PATH = ROOT / "data" / "processed" / "olist_analytics.duckdb"
SQL_DIR = ROOT / "sql"
OUT_DIR = ROOT / "data" / "processed"

QUERIES = [
    "01_core_wide_table.sql",
    "02_revenue_analysis.sql",
    "03_funnel_proxy.sql",
    "04_cohort_retention.sql",
    "05_rfm_segmentation.sql",
    "06_customer_satisfaction.sql",
    "08_advanced_business_diagnostics.sql",
]


def main() -> None:
    if not DB_PATH.exists():
        raise FileNotFoundError("DuckDB database not found. Run python src/build_duckdb.py first.")

    os.chdir(ROOT)
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    con = duckdb.connect(str(DB_PATH))

    for sql_file in QUERIES:
        query_path = SQL_DIR / sql_file
        print(f"Running {sql_file}")
        con.execute(query_path.read_text())

    con.close()
    print(f"Analysis outputs saved to: {OUT_DIR}")


if __name__ == "__main__":
    main()
