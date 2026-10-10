
import os

import pandas as pd
import pytest

from ecommerce_pipeline import extract, quality
from ecommerce_pipeline.db import test_connection as check_database_connection


pytestmark = pytest.mark.skipif(
    os.getenv("RUN_DB_INTEGRATION") != "1",
    reason="Set RUN_DB_INTEGRATION=1 to run PostgreSQL integration tests.",
)


@pytest.fixture
def test_database(monkeypatch):
    """Ensure integration tests connect only to ecommerce_test."""
    monkeypatch.setenv("DB_NAME", "ecommerce_test")

    database_name = check_database_connection()

    assert database_name == "ecommerce_test", (
        f"Unsafe database target: {database_name}"
    )

    return database_name


def test_postgres_connection_targets_test_database(test_database):
    assert test_database == "ecommerce_test"


def test_real_database_quality_checks_pass(test_database):
    results = quality.run_quality_checks()

    assert results == {
        "customers_without_email": 0,
        "products_with_invalid_price": 0,
        "order_items_with_invalid_quantity": 0,
        "orders_without_customers": 0,
    }


def test_analytics_extraction_from_postgres(
    test_database, monkeypatch, tmp_path
):
    """Verify analytics results using real PostgreSQL data."""
    # Keep integration-test CSVs separate from project outputs.
    monkeypatch.setattr(extract, "OUTPUT_DIR", tmp_path)

    extract.extract_analytics()

    monthly = pd.read_csv(tmp_path / "monthly_sales.csv")
    products = pd.read_csv(tmp_path / "top_products.csv")
    categories = pd.read_csv(tmp_path / "category_revenue.csv")

    # Monthly sales checks.
    assert len(monthly) == 6
    assert int(monthly["order_count"].sum()) == 11
    assert round(monthly["gross_revenue"].sum(), 2) == 36673.00

    # Top products checks.
    assert len(products) == 5
    assert products.iloc[0]["product_name"] == "Water Bottle"

    # Category revenue checks.
    assert len(categories) == 4
    assert round(categories["gross_revenue"].sum(), 2) == 36673.00
