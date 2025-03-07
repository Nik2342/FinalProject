from unittest.mock import mock_open, patch

from src.utils import (cashback_calculation, concat_card_data, filter_list_by_data, get_card_num, load_data,
                       top_five_transactions, total_expenses)

data = [
    {
        "Дата операции": "29.12.2021 22:32:24",
        "Дата платежа": "30.12.2021",
        "Номер карты": "*4556",
        "Статус": "OK",
        "Сумма операции": -1411.4,
        "Валюта операции": "RUB",
        "Сумма платежа": -1411.4,
        "Валюта платежа": "RUB",
        "Кэшбэк": 70.0,
        "Категория": "Ж/д билеты",
        "MCC": 4112.0,
        "Описание": "РЖД",
        "Бонусы (включая кэшбэк)": 70,
        "Округление на инвесткопилку": 0,
        "Сумма операции с округлением": 1411.4,
    },
    {
        "Дата операции": "29.12.2021 22:28:47",
        "Дата платежа": "30.12.2021",
        "Номер карты": "*4556",
        "Статус": "OK",
        "Сумма операции": -1411.4,
        "Валюта операции": "RUB",
        "Сумма платежа": -1411.4,
        "Валюта платежа": "RUB",
        "Кэшбэк": 70.0,
        "Категория": "Ж/д билеты",
        "MCC": 4112.0,
        "Описание": "РЖД",
        "Бонусы (включая кэшбэк)": 70,
        "Округление на инвесткопилку": 0,
        "Сумма операции с округлением": 1411.4,
    },
    {
        "Дата операции": "07.12.2021 14:02:27",
        "Дата платежа": "07.12.2021",
        "Номер карты": "*4556",
        "Статус": "OK",
        "Сумма операции": -837.9,
        "Валюта операции": "RUB",
        "Сумма платежа": -837.9,
        "Валюта платежа": "RUB",
        "Кэшбэк": 41.0,
        "Категория": "Ж/д билеты",
        "MCC": 4112.0,
        "Описание": "РЖД",
        "Бонусы (включая кэшбэк)": 41,
        "Округление на инвесткопилку": 0,
        "Сумма операции с округлением": 837.9,
    },
]
list_cards = ["4556", "1234"]


def test_without_data():
    result = filter_list_by_data(data)
    assert len(result) == 0


def test_only_start():
    result = filter_list_by_data(data, "2021-12-08")
    assert len(result) == 2


def test_only_end():
    result = filter_list_by_data(data, end_date="2024-01-01")
    assert len(result) == 0


# Тесты get_card_num
def test_get_card_num_nw():
    result = get_card_num(data)
    assert result == ["4556"]


def test_get_card_num_empty_list():
    result = get_card_num([])
    assert result == []


# Тесты total_expenses
def test_total_expenses_nw():
    result = total_expenses(data, list_cards)
    assert result == {"4556": 3660.7}


def test_total_expenses_empty_list():
    result = total_expenses([], [])
    assert result == {}


# Тесты cashback_calculation
def test_cashback_calculation():
    result = cashback_calculation(data, list_cards)
    assert result == {"4556": 36.0}


def test_cashback_calculation_empty():
    result = cashback_calculation([], [])
    assert result == {}


# Тесты concat_card_data
def test_concat_card_data():
    expenses = {"4556": 3660.7}
    cashback = {"4556": 36.0}
    result = concat_card_data(expenses, cashback)
    assert result == [{"cashback": 36.0, "last_digits": "4556", "total_spent": 3660.7}]


def test_concat_card_data_empty():
    expenses = {}
    cashback = {}
    result = concat_card_data(expenses, cashback)
    assert result == []


# Тесты top_five_transactions


def test_top_five_transactions():
    result = top_five_transactions(data)
    assert result == [
        {"amount": -1411.4, "category": "Ж/д билеты", "date": "30.12.2021", "description": "РЖД"},
        {"amount": -1411.4, "category": "Ж/д билеты", "date": "30.12.2021", "description": "РЖД"},
        {"amount": -837.9, "category": "Ж/д билеты", "date": "07.12.2021", "description": "РЖД"},
    ]


def test_top_five_transactions_empty():
    result = top_five_transactions([])
    assert result == []


# Тесты load
@patch("builtins.open", new_callable=mock_open, read_data='{"key": "value"}')
def test_load_data(mock_file):
    expected_data = {"key": "value"}
    result = load_data("path.json")
    assert result == expected_data
    mock_file.assert_called_once_with("path.json", "r")
