from src.services import (
    investment_bank,
    person_name_search,
    phone_number_search,
    simple_search,
    top_cashback_categories,
)


def test_top_cashback_categories():
    data = [
        {"Дата операции": "10.12.2021", "Сумма операции": -1000, "Категория": "Еда"},
        {"Дата операции": "11.12.2021", "Сумма операции": -500, "Категория": "Транспорт"},
        {"Дата операции": "10.11.2021", "Сумма операции": -1000, "Категория": "Еда"},
    ]

    result = top_cashback_categories(data, 2021, 12)

    assert result["Еда"] == 10.0
    assert result["Транспорт"] == 5.0


def test_top_categories_empty():
    result = top_cashback_categories([], 2021, 12)
    assert result == {}


def test_top_categories_wrong_month():
    data = [{"Дата операции": "10.11.2021", "Сумма операции": -1000, "Категория": "Еда"}]
    result = top_cashback_categories(data, 2021, 12)
    assert result == {}


def test_investment_bank():
    transactions = [
        {"Дата операции": "10.12.2021", "Сумма операции": -120},
        {"Дата операции": "11.12.2021", "Сумма операции": -170},
        {"Дата операции": "10.11.2021", "Сумма операции": -200},
    ]

    result = investment_bank("2021-12", transactions, 50)

    assert result == 30 + 30


def test_investment_bank_empty():
    result = investment_bank("2021-12", [], 50)
    assert result == 0


def test_simple_search():
    data = [{"Категория": "Переводы", "Описание": "Иван П."}, {"Категория": "Переводы", "Описание": "ООО Ромашка"}]

    result = simple_search(data, "РОМАШКА")
    assert len(result) == 1


def test_phone_number_search():
    data = [{"Описание": "МТС +7 921 123-45-67"}, {"Описание": "Без номера"}]

    result = phone_number_search(data)
    assert len(result) == 1


def test_person_name_search():
    data = [{"Категория": "Переводы", "Описание": "Иван П."}, {"Категория": "Переводы", "Описание": "ООО Ромашка"}]

    result = person_name_search(data)
    assert len(result) == 1
