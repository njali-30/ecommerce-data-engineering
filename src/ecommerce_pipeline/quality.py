
import logging

from sqlalchemy import text

from ecommerce_pipeline.db import create_db_engine


logger = logging.getLogger(__name__)


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
    logger.info("Starting data quality checks")

    engine = create_db_engine()
    results: dict[str, int] = {}

    try:
        with engine.connect() as connection:
            for check_name, query in QUALITY_CHECKS.items():
                logger.info("Running quality check: %s", check_name)

                issue_count = connection.execute(
                    text(query)
                ).scalar_one()

                results[check_name] = issue_count

                if issue_count == 0:
                    logger.info(
                        "PASS: %s - %d issue(s)",
                        check_name,
                        issue_count,
                    )
                else:
                    logger.error(
                        "FAIL: %s - %d issue(s)",
                        check_name,
                        issue_count,
                    )

        failed_checks = sum(
            1 for count in results.values() if count > 0
        )

        logger.info(
            "Data quality checks completed: %d passed, %d failed",
            len(results) - failed_checks,
            failed_checks,
        )

        return results

    except Exception:
        logger.exception("Data quality checks failed to execute")
        raise

    finally:
        engine.dispose()
        logger.debug("Database engine disposed")


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    results = run_quality_checks()

    if any(count > 0 for count in results.values()):
        raise SystemExit("Data quality checks failed.")

    logger.info("All data quality checks passed")
