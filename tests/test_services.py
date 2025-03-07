import json

from src.services import get_bank_operations


def test_get_bank_operations():
    dict_list = [
        {"Категория": "Супермаркеты", "Описание": "Колхоз"},
        {"Категория": "Переводы", "Описание": "Константин Л."},
        {"Категория": "Каршеринг", "Описание": "Ситидрайв"},
        {"Категория": "Фастфуд", "Описание": "IP Nelikaev"},
    ]
    search_str = "Фастфуд"
    expected_result = [{"Категория": "Фастфуд", "Описание": "IP Nelikaev"}]
    result = get_bank_operations(dict_list, search_str)
    assert json.loads(result) == expected_result


def test_get_bank_operations_empty_list():
    dict_list = []
    search_str = "Фастфуд"
    expected_result = []
    result = get_bank_operations(dict_list, search_str)
    assert json.loads(result) == expected_result
