
from pathlib import Path

import pandas as pd
from sqlalchemy import text

from ecommerce_pipeline.db import create_db_engine


PROJECT_ROOT = Path(__file__).resolve().parents[2]
OUTPUT_DIR = PROJECT_ROOT / "outputs"

QUERIES = {
    "monthly_sales": """
        SELECT
            DATE_TRUNC('month', o.order_date)::DATE AS sales_month,
            COUNT(DISTINCT o.order_id) AS order_count,
            ROUND(SUM(oi.quantity * oi.unit_price), 2) AS gross_revenue
        FROM orders AS o
        JOIN order_items AS oi
            ON o.order_id = oi.order_id
        WHERE o.status <> 'cancelled'
        GROUP BY DATE_TRUNC('month', o.order_date)::DATE
        ORDER BY sales_month
    """,
    "top_products": """
        SELECT
            p.product_name,
            SUM(oi.quantity) AS units_sold,
            ROUND(SUM(oi.quantity * oi.unit_price), 2) AS gross_sales
        FROM order_items AS oi
        JOIN orders AS o
            ON oi.order_id = o.order_id
        JOIN products AS p
            ON oi.product_id = p.product_id
        WHERE o.status <> 'cancelled'
        GROUP BY p.product_id, p.product_name
        ORDER BY units_sold DESC, gross_sales DESC
        LIMIT 5
    """,
    "category_revenue": """
        SELECT
            cat.category_name,
            SUM(oi.quantity) AS units_sold,
            ROUND(SUM(oi.quantity * oi.unit_price), 2) AS gross_revenue
        FROM categories AS cat
        JOIN products AS p
            ON cat.category_id = p.category_id
        JOIN order_items AS oi
            ON p.product_id = oi.product_id
        JOIN orders AS o
            ON oi.order_id = o.order_id
        WHERE o.status <> 'cancelled'
        GROUP BY cat.category_id, cat.category_name
        ORDER BY gross_revenue DESC
    """,
}


def extract_analytics() -> None:
    """Run analytics queries and save their results as CSV files."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    engine = create_db_engine()

    try:
        for report_name, query in QUERIES.items():
            with engine.connect() as connection:
                dataframe = pd.read_sql(
                    text(query),
                    connection,
                )

            output_path = OUTPUT_DIR / f"{report_name}.csv"
            dataframe.to_csv(output_path, index=False)

            try:
                display_path = output_path.relative_to(PROJECT_ROOT)
            except ValueError:
                # Supports test output directories outside the project.
                display_path = output_path

            print(f"Exported {len(dataframe)} rows to {display_path}")
    finally:
        engine.dispose()


if __name__ == "__main__":
    extract_analytics()
