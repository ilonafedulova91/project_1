import os

import pandas as pd
import pytest

from src.reports import expenses_per_category, spending_by_weekday, spending_by_workday


@pytest.fixture
def data():
    return pd.DataFrame(
        {
            "Дата операции": ["01.10.2022", "01.11.2023", "15.11.2023", "01.12.2023"],
            "Категория": ["Еда", "Еда", "Транспорт", "Еда"],
            "Сумма операции": [100, 200, 300, 400],
        }
    )


def test_expenses_per_category(data):
    result = expenses_per_category(data, "Еда", "05.12.2023")

    assert isinstance(result, pd.DataFrame)
    assert not result.empty
    assert result["Сумма операции"].iloc[0] == 600


def test_save_report(data):
    filename = "report.json"

    if os.path.exists(filename):
        os.remove(filename)

    expenses_per_category(data, "Еда", "05.12.2023")

    assert os.path.exists(filename)

    os.remove(filename)


def test_spending_by_weekday(data):
    result = spending_by_weekday(data, "05.12.2023")

    assert isinstance(result, pd.DataFrame)
    assert "weekday" in result.columns
    assert "Сумма операции" in result.columns


def test_spending_by_workday(data):
    result = spending_by_workday(data, "05.12.2023")

    assert isinstance(result, pd.DataFrame)
    assert "is_weekend" in result.columns


def test_empty_category(data):
    result = expenses_per_category(data, "Неизвестно", "05.12.2023")

    assert result.empty
