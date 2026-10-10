
from pathlib import Path

import pandas as pd
import pytest

from ecommerce_pipeline.extract import QUERIES
from ecommerce_pipeline.quality import QUALITY_CHECKS


PROJECT_ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = PROJECT_ROOT / "outputs"


@pytest.fixture
def monthly_sales():
    path = OUTPUT_DIR / "monthly_sales.csv"
    assert path.exists(), f"Missing report: {path}"
    return pd.read_csv(path)


@pytest.fixture
def top_products():
    path = OUTPUT_DIR / "top_products.csv"
    assert path.exists(), f"Missing report: {path}"
    return pd.read_csv(path)


@pytest.fixture
def category_revenue():
    path = OUTPUT_DIR / "category_revenue.csv"
    assert path.exists(), f"Missing report: {path}"
    return pd.read_csv(path)


def test_analytics_queries_are_defined():
    assert {
        "monthly_sales",
        "top_products",
        "category_revenue",
    } == set(QUERIES)


def test_quality_checks_are_defined():
    assert {
        "customers_without_email",
        "products_with_invalid_price",
        "order_items_with_invalid_quantity",
        "orders_without_customers",
    } == set(QUALITY_CHECKS)


def test_monthly_sales_report(monthly_sales):
    assert len(monthly_sales) == 6
    assert {
        "sales_month",
        "order_count",
        "gross_revenue",
    }.issubset(monthly_sales.columns)

    assert monthly_sales["sales_month"].is_unique
    assert monthly_sales["order_count"].gt(0).all()
    assert monthly_sales["gross_revenue"].notna().all()
    assert monthly_sales["gross_revenue"].ge(0).all()


def test_top_products_report(top_products):
    assert len(top_products) == 5
    assert {
        "product_name",
        "units_sold",
        "gross_sales",
    }.issubset(top_products.columns)

    assert top_products["product_name"].notna().all()
    assert top_products["product_name"].is_unique
    assert top_products["units_sold"].gt(0).all()
    assert top_products["gross_sales"].ge(0).all()


def test_category_revenue_report(category_revenue):
    assert len(category_revenue) == 4
    assert {
        "category_name",
        "units_sold",
        "gross_revenue",
    }.issubset(category_revenue.columns)

    assert category_revenue["category_name"].notna().all()
    assert category_revenue["category_name"].is_unique
    assert category_revenue["units_sold"].gt(0).all()
    assert category_revenue["gross_revenue"].ge(0).all()
