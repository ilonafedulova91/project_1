import json

import pandas as pd

from src.utils import (
    get_card_information,
    get_currency_rates,
    get_greetings,
    get_stock_prices,
    get_top_transaction,
    group_categories_expenses,
    group_categories_incomes,
    group_transfers_and_cash,
    load_settings_json,
    sorted_by_date,
    total_amount,
)


def main_page(data: pd.DataFrame, date_str: str) -> str:
    """This function creates the main page of the website."""
    df = sorted_by_date(data, date_str)
    settings = load_settings_json()

    response = {
        "greeting": get_greetings(),
        "cards": get_card_information(df),
        "top_transactions": get_top_transaction(df),
        "currency_rates": get_currency_rates(settings["user_currencies"]),
        "stock_prices": get_stock_prices(settings["user_stocks"]),
    }

    return json.dumps(response, indent=2, ensure_ascii=False)


def events_page(data: pd.DataFrame, date_str: str, data_range: str = "M") -> str:
    """This function shows the events page."""
    end_date = pd.to_datetime(date_str, dayfirst=True)

    if data_range == "W":
        start_date = end_date - pd.Timedelta(days=end_date.weekday())
    elif data_range == "M":
        start_date = end_date.replace(day=1)
    elif data_range == "Y":
        start_date = end_date.replace(day=1, month=1)
    elif data_range == "ALL":
        start_date = pd.Timestamp.min

    df = data.copy()
    df["Дата операции"] = pd.to_datetime(df["Дата операции"], dayfirst=True)

    df = sorted_by_date(data, date_str)
    settings = load_settings_json()

    response = {
        "expenses": {
            "total_amount": total_amount(data),
            "main": group_categories_expenses(data),
            "transfers_and_cash": group_transfers_and_cash(data),
        },
        "income": {"total_amount": total_amount(data, expenses=False), "main": group_categories_incomes(data)},
        "currency_rates": get_currency_rates(settings["user_currencies"]),
        "stock_prices": get_stock_prices(settings["user_stocks"]),
    }

    return json.dumps(response, indent=2, ensure_ascii=False)
