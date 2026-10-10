
from sqlalchemy import text

from ecommerce_pipeline.db import create_db_engine


QUALITY_CHECKS = {
    "customers_without_email": """
        SELECT COUNT(*)
        FROM customers
        WHERE email IS NULL OR TRIM(email) = ''
    """,
    "products_with_invalid_price": """
        SELECT COUNT(*)
        FROM products
        WHERE price < 0 OR price IS NULL
    """,
    "order_items_with_invalid_quantity": """
        SELECT COUNT(*)
        FROM order_items
        WHERE quantity <= 0 OR quantity IS NULL
    """,
    "orders_without_customers": """
        SELECT COUNT(*)
        FROM orders AS o
        LEFT JOIN customers AS c
            ON o.customer_id = c.customer_id
        WHERE c.customer_id IS NULL
    """,
}


def run_quality_checks() -> dict[str, int]:
    """Run database quality checks and return issue counts."""
    engine = create_db_engine()
    results = {}

    try:
        with engine.connect() as connection:
            for check_name, query in QUALITY_CHECKS.items():
                results[check_name] = connection.execute(
                    text(query)
                ).scalar_one()
    finally:
        engine.dispose()

    return results


if __name__ == "__main__":
    results = run_quality_checks()

    for check_name, issue_count in results.items():
        status = "PASS" if issue_count == 0 else "FAIL"
        print(f"{status}: {check_name} — {issue_count} issue(s)")

    if any(count > 0 for count in results.values()):
        raise SystemExit("Data quality checks failed.")
    print("All data quality checks passed.")

