import json
from datetime import datetime
from unittest.mock import patch

import pandas as pd
import pytest

from src.utils import (
    get_card_information,
    get_currency_rates,
    get_greetings,
    get_stock_prices,
    get_top_transaction,
    group_categories_expenses,
    group_categories_incomes,
    group_transfers_and_cash,
    load_data,
    load_settings_json,
    sorted_by_date,
    total_amount,
)


def test_load_settings_json(tmp_path):
    file = tmp_path / "settings.json"
    data = {"user_currencies": ["USD"]}

    with open(file, "w", encoding="utf-8") as f:
        json.dump(data, f)

    result = load_settings_json(file)

    assert result == data


def test_load_data_wrong_type():
    with pytest.raises(ValueError):
        load_data(123)


def test_load_data_wrong_extension():
    with pytest.raises(ValueError):
        load_data("test.csv")


def test_sorted_by_date():
    df = pd.DataFrame({"Дата операции": ["01.12.2023 00:00:00", "20.12.2023 00:00:00"], "Сумма операции": [100, 200]})

    result = sorted_by_date(df, "15.12.2023")

    assert len(result) == 1


@patch("src.utils.datetime")
def test_get_greetings_morning(mock_datetime):
    mock_datetime.now.return_value = datetime(2023, 1, 1, 8, 0, 0)
    mock_datetime.strptime = datetime.strptime

    assert get_greetings() == "Доброе утро"


@patch("src.utils.datetime")
def test_get_greetings_evening(mock_datetime):
    mock_datetime.now.return_value = datetime(2023, 1, 1, 19, 0, 0)
    mock_datetime.strptime = datetime.strptime

    assert get_greetings() == "Добрый вечер"


def test_get_card_information():
    df = pd.DataFrame({"Номер карты": ["1234567891234567", "1234567891234567"], "Сумма операции": [-100, -200]})

    result = get_card_information(df)

    assert result[0]["last_digits"] == "4567"
    assert result[0]["total_spent"] == -300
    assert result[0]["cashback"] == 3


def test_get_top_transaction():
    df = pd.DataFrame(
        {
            "Дата операции": ["01.12.2023", "02.12.2023"],
            "Сумма операции": [100, 200],
            "Категория": ["Еда", "Транспорт"],
            "Описание": ["test_1", "test_2"],
        }
    )

    result = get_top_transaction(df)

    assert len(result) == 2


def test_total_amount_expenses():
    df = pd.DataFrame({"Сумма операции": [-100, -200, 50]})

    assert total_amount(df) == 300


def test_total_amount_incomes():
    df = pd.DataFrame({"Сумма операции": [100, 200, -50]})

    assert total_amount(df, expenses=False) == 300


def test_group_categories_expenses():
    df = pd.DataFrame({"Категория": ["Еда", "Транспорт", "Переводы"], "Сумма операции": [-100, -200, -300]})

    result = group_categories_expenses(df)

    assert isinstance(result, list)
    assert any(item["category"] == "Еда" for item in result)


def test_group_transfers_and_cash():
    df = pd.DataFrame({"Категория": ["Еда", "Наличные", "Переводы"], "Сумма операции": [100, 200, 300]})

    result = group_transfers_and_cash(df)

    assert len(result) >= 1


def test_group_categories_incomes():
    df = pd.DataFrame({"Категория": ["Зарплата", "Кэшбэк"], "Сумма операции": [100, 200]})

    result = group_categories_incomes(df)

    assert len(result) == 2


@patch("src.utils.requests.get")
def test_get_currency_rates(mock_get):
    mock_get.return_value.json.return_value = {"conversion_rates": {"USD": 100}}

    result = get_currency_rates(["USD"])

    assert result[0]["currency"] == "USD"


@patch("src.utils.requests.get")
def test_get_stock_prices(mock_get):
    mock_get.return_value.json.return_value = {"close": 150}

    stocks = ["AAPL"]

    result = get_stock_prices(stocks)

    assert len(result) == 1
    assert result[0]["symbol"] == "AAPL"
