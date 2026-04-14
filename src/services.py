import re
from collections import defaultdict
from datetime import datetime
from typing import Any, Dict, List, DefaultDict


def top_cashback_categories(data: List[Dict[str, Any]], year: int, month: int) -> Dict[str, float]:
    """This function groups the cashback per category."""
    result: DefaultDict[str, float] = defaultdict(float)

    try:
        for transaction in data:
            date = datetime.strptime(transaction["Дата операции"], "%d.%m.%Y")

            if date.year != year or date.month != month:
                continue

            amount = transaction.get("Сумма операции", 0)

            if amount >= 0:
                continue

            category = transaction.get("Категория", "Неизвестно")

            cashback = (amount * -1) / 100

            result[category] += cashback

        return {category: round(amount, 2) for category, amount in result.items()}

    except Exception:
        return {}


def investment_bank(month: str, transactions: List[Dict[str, Any]], limit: int) -> float:
    """This function calculates the investment amount."""
    total_amount = 0

    for transaction in transactions:
        date = datetime.strptime(transaction["Дата операции"], "%d.%m.%Y")

        if date.strftime("%Y-%m") != month:
            continue

        amount = transaction["Сумма операции"]

        if amount >= 0:
            continue

        rounded_amount = ((amount * -1 // limit) + 1) * limit
        total_amount += rounded_amount - (amount * -1)

    return round(total_amount, 2)


def simple_search(transactions: List[Dict[str, Any]], search_str: str) -> List[Dict[str, Any]]:
    """This function searches for a specific search string."""
    return [
        transaction
        for transaction in transactions
        if search_str.lower() in (transaction.get("Описание", "")).lower()
        or search_str.lower() in (transaction.get("Категория", "")).lower()
    ]


def phone_number_search(transactions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """This function searches for a specific phone number."""
    pattern = re.compile(r"\+7\s?\d{3}[\s-]?\d{2,3}[\s-]?\d{2}[\s-]?\d{2}")
    return [transaction for transaction in transactions if pattern.search(transaction.get("Описание", ""))]


def person_name_search(transactions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """This function searches for a specific person name."""
    pattern = re.compile(r"[А-ЯЁ][а-яё]+\s[А-ЯЁ]\.")

    return [
        transaction
        for transaction in transactions
        if transaction.get("Категория") == "Переводы" and pattern.search(transaction.get("Описание", ""))
    ]
