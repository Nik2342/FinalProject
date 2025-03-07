import json
import logging
import re

logger = logging.getLogger("services")
logger.setLevel(logging.DEBUG)
console_handler = logging.StreamHandler()
logger.addHandler(console_handler)
file_formatter = logging.Formatter("%(asctime)s %(levelname)s : %(message)s")
console_handler.setFormatter(file_formatter)


def get_bank_operations(dict_list: list, search_str: str) -> str:
    """Функция для фильтрации списка транзакций по строке поиска"""
    logger.info("Фильтрация списка транзакций по строке, заданной пользователем")
    result = []
    pattern = re.compile(search_str, re.IGNORECASE)
    for el in dict_list:
        category = el.get("Категория")
        description = el.get("Описание")
        if pattern.search(description) or pattern.search(category):
            result.append(el)
    result = json.dumps(result, ensure_ascii=False)
    return result
