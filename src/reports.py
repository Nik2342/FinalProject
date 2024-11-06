import logging
from datetime import datetime, timedelta
from functools import wraps
from typing import Any, Callable, Optional

import pandas as pd

logger = logging.getLogger("reports")
logger.setLevel(logging.DEBUG)
console_handler = logging.StreamHandler()
logger.addHandler(console_handler)
file_formatter = logging.Formatter("%(asctime)s %(levelname)s : %(message)s")
console_handler.setFormatter(file_formatter)


def spending_by_category(transactions: pd.DataFrame, category: str, date: Optional[str] = None) -> pd.DataFrame:
    """Функция возвращающая общие траты по категориям"""
    logger.info("Проверка указана ли дата пользователем")
    if date is None:
        date_from = datetime.now() - timedelta(days=90)
        date_to = datetime.now()
    else:
        date = datetime.strptime(date, "%d.%m.%Y")
        date_from = date - timedelta(days=90)
        date_to = datetime.now()
    logger.info("Получение данных")
    xlsx_list = transactions.to_dict(orient="records")
    xlsx_list = [row for row in xlsx_list if not any(pd.isna(value) for value in row.values())]
    logger.info("Сортировка данных")
    converted_list = [
        el for el in xlsx_list if date_from <= datetime.strptime(el.get("Дата платежа"), "%d.%m.%Y") <= date_to
    ]
    result = []
    for el in converted_list:
        if el.get("Категория") is None:
            continue
        else:
            if el["Категория"] == category:
                result.append({"Сумма операции": el["Сумма операции"], "Описание": el["Описание"]})
    result = pd.DataFrame(result)
    return result


def log(filename: str = None) -> Callable:
    """Декоратор, для логирования функции"""
    if filename is None:
        filename = "log.txt"

    def wrapper(func: Callable) -> Callable:
        @wraps(func)
        def inner(*args: Any, **kwargs: Any) -> Any:
            result = None
            try:
                result = func(*args, **kwargs)
                with open(filename, "a", encoding="utf-8") as file:
                    file.write(f"{func.__name__} {result}\n")
            except Exception as e:
                with open(filename, "a", encoding="utf-8") as file:
                    file.write(f"{func.__name__} error: {e}. Input: {args} {kwargs}\n")
                raise e

            return result

        return inner

    return wrapper
