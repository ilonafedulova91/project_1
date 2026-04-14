from datetime import datetime, timedelta
from functools import wraps
from typing import Optional

import pandas as pd


def save_report(filename=None):
    """This function creates a report from the data frame."""

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)

            name = filename or "report.json"
            result.to_json(name, ensure_ascii=False, indent=4)

            return result

        return wrapper

    return decorator


@save_report()
def expenses_per_category(transactions: pd.DataFrame, category: str, date: Optional[str] = None) -> pd.DataFrame:
    """This function creates a expenses report from the data frame."""
    if date:
        end_date = datetime.strptime(date, "%d.%m.%Y")
    else:
        end_date = datetime.now()

    start_date = end_date - timedelta(days=90)

    transactions["Дата операции"] = pd.to_datetime(transactions["Дата операции"], format="%d.%m.%Y")

    df = transactions[
        (transactions["Дата операции"] >= start_date)
        & (transactions["Дата операции"] <= end_date)
        & (transactions["Категория"] == category)
    ]

    return df.groupby("Категория")["Сумма операции"].sum().reset_index()


def spending_by_weekday(transactions: pd.DataFrame, date: Optional[str] = None) -> pd.DataFrame:
    """This function creates a spending report for a weekday from the data frame."""
    if date:
        end_date = pd.to_datetime(date)
    else:
        end_date = pd.Timestamp.now()

    start_date = end_date - pd.Timedelta(days=90)

    df = transactions.copy()
    df["Дата операции"] = pd.to_datetime(df["Дата операции"], format="%d.%m.%Y")

    df = df[(df["Дата операции"] >= start_date) & (df["Дата операции"] <= end_date)]

    df["weekday"] = df["Дата операции"].dt.day_name()

    return df.groupby("weekday")["Сумма операции"].mean().reset_index()


def spending_by_workday(transactions: pd.DataFrame, date: Optional[str] = None) -> pd.DataFrame:
    """This function creates a spending report for a workday from the data frame."""
    if date:
        end_date = pd.to_datetime(date)
    else:
        end_date = pd.Timestamp.now()

    start_date = end_date - pd.Timedelta(days=90)

    df = transactions.copy()
    df["Дата операции"] = pd.to_datetime(df["Дата операции"], format="%d.%m.%Y")

    df = df[(df["Дата операции"] >= start_date) & (df["Дата операции"] <= end_date)]

    df["is_weekend"] = df["Дата операции"].dt.weekday >= 5

    return df.groupby("is_weekend")["Сумма операции"].mean().reset_index()
