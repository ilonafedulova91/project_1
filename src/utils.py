import json
import os
from datetime import datetime

import pandas as pd
import requests
from dotenv import load_dotenv

load_dotenv()
API_KEY_CURRENCIES = os.getenv("API_KEY_CURRENCIES")
API_KEY_STOCKS = os.getenv("API_KEY_STOCKS")

JSON_PATH = "C:\\PythonProjects\\project_1\\user_settings.json"


def load_settings_json(path=JSON_PATH):
    """This function loads the settings json file."""
    with open(path, "r", encoding="utf-8") as json_file:
        return json.load(json_file)


def load_data(file_path: str) -> pd.DataFrame:
    """This function loads the data from Excel file."""
    if not isinstance(file_path, str):
        raise ValueError("The file path must be a string")
    if not file_path.endswith(".xlsx"):
        raise ValueError("The file path must end with .xlsx")

    try:
        df = pd.read_excel(file_path)
    except FileNotFoundError:
        return []
    return df


def sorted_by_date(df: pd.DataFrame, date_str: str) -> pd.DataFrame:
    """This function sorts the data by date and returns the sorted dataframe."""
    date = pd.to_datetime(date_str, format="%d.%m.%Y")

    df["Дата операции"] = pd.to_datetime(df["Дата операции"], format="%d.%m.%Y %H:%M:%S")
    return df[df["Дата операции"] <= date]


def get_greetings() -> str:
    """This function returns the greetings."""
    date_str = datetime.now().strftime("%d.%m.%Y %H:%M:%S")

    hour = datetime.strptime(date_str, "%d.%m.%Y %H:%M:%S").hour

    if 6 <= hour < 12:
        return "Доброе утро"
    elif 12 <= hour < 18:
        return "Добрый день"
    elif 18 <= hour < 24:
        return "Добрый вечер"
    else:
        return "Доброй ночи"


def get_card_information(df: pd.DataFrame):
    """This function returns the card information."""
    grouped_cards = df.groupby("Номер карты")["Сумма операции"].sum()

    return [
        {
            "last_digits": str(card)[-4:],
            "total_spent": round(total_amount, 2),
            "cashback": round(total_amount / -100, 2) if total_amount < 0 else 0,
        }
        for card, total_amount in grouped_cards.items()
    ]


def get_top_transaction(df: pd.DataFrame):
    """This function returns the top transactions."""
    df = df.copy()

    df["Дата операции"] = pd.to_datetime(df["Дата операции"], dayfirst=True)

    top_transactions = df.sort_values(by="Сумма операции", ascending=False).head(5)

    return [
        {
            "date": row["Дата операции"].strftime("%d.%m.%Y"),
            "amount": row["Сумма операции"],
            "category": row["Категория"],
            "description": row["Описание"],
        }
        for _, row in top_transactions.iterrows()
    ]


def get_currency_rates(currencies: list) -> list:
    """This function returns the currency rates."""
    if not currencies:
        return []

    url = f"https://v6.exchangerate-api.com/v6/{API_KEY_CURRENCIES}/latest/RUB"

    try:
        response = requests.get(url)
        data_json = response.json()

        return [
            {"currency": currency, "rate": round(1 / data_json.get("conversion_rates", {}).get(currency, 0), 2)}
            for currency in currencies
        ]
    except Exception as e:
        print("Currency API error:", e)
        return []


def get_stock_prices(stocks: list) -> list:
    """This function returns the stock prices."""
    if not stocks:
        return []

    stock_prices = []

    for stock in stocks:
        try:
            url = f"https://eodhd.com/api/real-time/{stock}?api_token={API_KEY_STOCKS}&fmt=json"
            stock_price = requests.get(url).json()

            stock_prices.append({"symbol": stock, "price": round(stock_price.get("close", 0), 2)})

        except Exception:
            return []

    return stock_prices


def total_amount(df: pd.DataFrame, expenses=True) -> float:
    """This function returns the total amount of expenses/incomes."""
    if expenses:
        amount = df[df["Сумма операции"] < 0].copy()
        return float(round(amount["Сумма операции"].sum() * -1, 2))
    else:
        amount = df[df["Сумма операции"] > 0].copy()
        return float(round(amount["Сумма операции"].sum(), 2))


def group_categories_expenses(df: pd.DataFrame) -> list:
    """This function groups the categories expenses."""
    expenses = df[df["Сумма операции"] < 0].copy()

    grouped_categories = expenses.groupby("Категория")["Сумма операции"].sum().sort_values(ascending=False)

    main_categories = grouped_categories.drop(["Переводы", "Наличные"], errors="ignore")

    top_7_categories = main_categories.head(7)
    other_sum = main_categories.iloc[7:].sum()

    main_result = [
        {"category": category, "amount": round(float(amount), 2)} for category, amount in top_7_categories.items()
    ]

    if other_sum < 0:
        main_result.append({"category": "Остальное", "amount": float(other_sum)})

    return main_result


def group_transfers_and_cash(df: pd.DataFrame) -> list:
    """This function groups the transfers and cash."""
    transfers_and_cash = df[df["Категория"].isin(["Наличные", "Переводы"])].copy()
    grouped_categories = transfers_and_cash.groupby("Категория")["Сумма операции"].sum().sort_values(ascending=False)

    transfers_and_cash_result = [
        {"category": category, "amount": float(amount)} for category, amount in grouped_categories.items()
    ]

    return transfers_and_cash_result


def group_categories_incomes(df: pd.DataFrame) -> list:
    """This function groups the categories incomes."""
    incomes = df[df["Сумма операции"] > 0].copy()

    grouped_categories = incomes.groupby("Категория")["Сумма операции"].sum().sort_values(ascending=False)

    main_categories = grouped_categories.drop(["Переводы", "Наличные"], errors="ignore")

    main_result = [{"category": category, "amount": float(amount)} for category, amount in main_categories.items()]

    return main_result
