from pathlib import Path

import duckdb


ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = ROOT / "data" / "raw"
DB_PATH = ROOT / "data" / "processed" / "olist_analytics.duckdb"

TABLES = {
    "customers": "olist_customers_dataset.csv",
    "geolocation": "olist_geolocation_dataset.csv",
    "order_items": "olist_order_items_dataset.csv",
    "order_payments": "olist_order_payments_dataset.csv",
    "order_reviews": "olist_order_reviews_dataset.csv",
    "orders": "olist_orders_dataset.csv",
    "products": "olist_products_dataset.csv",
    "sellers": "olist_sellers_dataset.csv",
    "category_translation": "product_category_name_translation.csv",
}


def validate_files() -> None:
    missing = [filename for filename in TABLES.values() if not (RAW_DIR / filename).exists()]
    if missing:
        missing_list = "\n".join(f"- {name}" for name in missing)
        raise FileNotFoundError(
            "Missing raw CSV files in data/raw/:\n"
            f"{missing_list}\n\n"
            "Download the Olist Kaggle dataset and place the original CSV files in data/raw/."
        )


def main() -> None:
    validate_files()
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    con = duckdb.connect(str(DB_PATH))
    for table_name, filename in TABLES.items():
        csv_path = RAW_DIR / filename
        con.execute(
            f"""
            CREATE OR REPLACE TABLE {table_name} AS
            SELECT *
            FROM read_csv_auto('{csv_path.as_posix()}', header = true);
            """
        )

    con.close()
    print(f"Created DuckDB database: {DB_PATH}")


if __name__ == "__main__":
    main()
