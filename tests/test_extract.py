
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

def test_monthly_sales_revenue_matches_expected_total(monthly_sales):
    expected_total = 36673.00

    actual_total = round(monthly_sales["gross_revenue"].sum(), 2)

    assert actual_total == expected_total

def test_category_revenue_matches_expected_results(category_revenue):
    expected = {
        "Electronics": 14691.00,
        "Home & Kitchen": 9592.00,
        "Clothing": 7393.00,
        "Books": 4997.00,
    }

    actual = dict(
        zip(category_revenue["category_name"], category_revenue["gross_revenue"])
    )

    assert actual == expected
    assert round(category_revenue["gross_revenue"].sum(), 2) == 36673.00


def test_top_products_match_expected_ranking(top_products):
    expected = [
        ("Water Bottle", 6, 2994.00),
        ("Cotton T-Shirt", 5, 2995.00),
        ("USB-C Charger", 4, 3596.00),
        ("SQL for Beginners", 4, 2600.00),
        ("Wireless Headphones", 3, 7497.00),
    ]

    actual = list(
        top_products[
            ["product_name", "units_sold", "gross_sales"]
        ].itertuples(index=False, name=None)
    )

    actual = [
        (name, int(units), round(float(sales), 2))
        for name, units, sales in actual
    ]

    assert actual == expected

