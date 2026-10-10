from unittest.mock import MagicMock

from ecommerce_pipeline import quality


def test_run_quality_checks_returns_all_results(monkeypatch):
    mock_engine = MagicMock()
    mock_connection = MagicMock()

    mock_engine.connect.return_value.__enter__.return_value = (
        mock_connection
    )

    mock_connection.execute.return_value.scalar_one.side_effect = [
        0,  # customers_without_email
        0,  # products_with_invalid_price
        0,  # order_items_with_invalid_quantity
        0,  # orders_without_customers
    ]

    monkeypatch.setattr(
        quality,
        "create_db_engine",
        lambda: mock_engine,
    )

    results = quality.run_quality_checks()

    assert results == {
        "customers_without_email": 0,
        "products_with_invalid_price": 0,
        "order_items_with_invalid_quantity": 0,
        "orders_without_customers": 0,
    }

    assert mock_connection.execute.call_count == 4
    mock_engine.dispose.assert_called_once()


def test_run_quality_checks_disposes_engine_on_failure(monkeypatch):
    mock_engine = MagicMock()
    mock_connection = MagicMock()

    mock_engine.connect.return_value.__enter__.return_value = (
        mock_connection
    )
    mock_connection.execute.side_effect = RuntimeError(
        "Database query failed"
    )

    monkeypatch.setattr(
        quality,
        "create_db_engine",
        lambda: mock_engine,
    )

    import pytest

    with pytest.raises(RuntimeError, match="Database query failed"):
        quality.run_quality_checks()

    mock_engine.dispose.assert_called_once()
