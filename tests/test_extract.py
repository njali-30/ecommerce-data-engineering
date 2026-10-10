
from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = PROJECT_ROOT / "outputs"


def test_monthly_sales_csv_exists():
    assert (OUTPUT_DIR / "monthly_sales.csv").exists()


def test_monthly_sales_has_expected_rows_and_columns():
    dataframe = pd.read_csv(OUTPUT_DIR / "monthly_sales.csv")

    assert len(dataframe) == 6
    assert {
        "sales_month",
        "order_count",
        "gross_revenue",
    }.issubset(dataframe.columns)


def test_top_products_csv_has_expected_rows():
    dataframe = pd.read_csv(OUTPUT_DIR / "top_products.csv")

    assert len(dataframe) == 5
    assert {
        "product_name",
        "units_sold",
        "gross_sales",
    }.issubset(dataframe.columns)


def test_category_revenue_csv_has_expected_rows():
    dataframe = pd.read_csv(OUTPUT_DIR / "category_revenue.csv")

    assert len(dataframe) == 4
    assert {
        "category_name",
        "units_sold",
        "gross_revenue",
    }.issubset(dataframe.columns)


def test_exported_revenue_values_are_valid():
    dataframe = pd.read_csv(OUTPUT_DIR / "monthly_sales.csv")

    assert dataframe["gross_revenue"].notna().all()
    assert (dataframe["gross_revenue"] >= 0).all()
