import json
from unittest.mock import patch

import pandas as pd

from src.views import events_page, main_page


@patch("src.views.get_stock_prices")
@patch("src.views.get_currency_rates")
@patch("src.views.load_settings_json")
def test_main_page(mock_settings_json, mock_currency_rates, mock_stock_prices):
    mock_settings_json.return_value = {"user_currencies": ["USD"], "user_stocks": ["AAPL"]}

    mock_currency_rates.return_value = [{"currency": "USD", "rate": 100}]
    mock_stock_prices.return_value = [{"AAPL": {"price": 100}}]

    df = pd.DataFrame(
        {
            "Дата операции": ["01.12.2023 00:00:00"],
            "Сумма операции": [100],
            "Категория": ["Еда"],
            "Описание": ["test"],
            "Номер карты": ["12345678"],
        }
    )

    result = main_page(df, "15.12.2023")
    result_dict = json.loads(result)

    assert "greeting" in result_dict
    assert "cards" in result_dict
    assert "top_transactions" in result_dict
    assert "currency_rates" in result_dict
    assert "stock_prices" in result_dict

    assert result_dict["currency_rates"] == [{"currency": "USD", "rate": 100}]
    assert result_dict["stock_prices"] == [{"AAPL": {"price": 100}}]


@patch("src.views.get_stock_prices")
@patch("src.views.get_currency_rates")
@patch("src.views.load_settings_json")
def test_events_page(mock_settings_json, mock_currency_rates, mock_stock_prices):
    mock_settings_json.return_value = {"user_currencies": ["USD"], "user_stocks": ["AAPL"]}

    mock_currency_rates.return_value = [{"currency": "USD", "rate": 100}]
    mock_stock_prices.return_value = [{"AAPL": {"price": 100}}]

    df = pd.DataFrame(
        {
            "Дата операции": ["01.12.2023 00:00:00"],
            "Сумма операции": [100],
            "Категория": ["Еда"],
        }
    )

    result = events_page(df, "15.12.2023")
    result_dict = json.loads(result)

    assert "expenses" in result_dict
    assert "income" in result_dict
    assert "currency_rates" in result_dict
    assert "stock_prices" in result_dict
