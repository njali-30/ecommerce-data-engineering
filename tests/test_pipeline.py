
import pytest

from ecommerce_pipeline import run_pipeline


def test_pipeline_stops_when_quality_check_fails(monkeypatch):
    extraction_called = False

    def fake_quality_checks():
        return {
            "customers_without_email": 1,
            "products_with_invalid_price": 0,
            "order_items_with_invalid_quantity": 0,
            "orders_without_customers": 0,
        }

    def fake_extract_analytics():
        nonlocal extraction_called
        extraction_called = True

    monkeypatch.setattr(
        run_pipeline,
        "run_quality_checks",
        fake_quality_checks,
    )
    monkeypatch.setattr(
        run_pipeline,
        "extract_analytics",
        fake_extract_analytics,
    )

    with pytest.raises(SystemExit, match="data quality checks failed"):
        run_pipeline.main()

    assert extraction_called is False


def test_pipeline_runs_extraction_when_quality_checks_pass(
    monkeypatch, capsys
):
    extraction_called = False

    def fake_quality_checks():
        return {
            "customers_without_email": 0,
            "products_with_invalid_price": 0,
            "order_items_with_invalid_quantity": 0,
            "orders_without_customers": 0,
        }

    def fake_extract_analytics():
        nonlocal extraction_called
        extraction_called = True

    monkeypatch.setattr(
        run_pipeline,
        "run_quality_checks",
        fake_quality_checks,
    )
    monkeypatch.setattr(
        run_pipeline,
        "extract_analytics",
        fake_extract_analytics,
    )

    run_pipeline.main()

    captured = capsys.readouterr()

    assert extraction_called is True
    assert "Pipeline completed successfully." in captured.out
