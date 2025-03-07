import json
import logging
from datetime import datetime

from src.external_api import get_currency_rate, get_s_p_500
from src.get_data import xlsx_data_conversion
from src.utils import (cashback_calculation, concat_card_data, filter_list_by_data, get_card_num, load_data,
                       top_five_transactions, total_expenses, welcome_message)

logger = logging.getLogger("views")
logger.setLevel(logging.DEBUG)
console_handler = logging.StreamHandler()
logger.addHandler(console_handler)
file_formatter = logging.Formatter("%(asctime)s %(levelname)s : %(message)s")
console_handler.setFormatter(file_formatter)

path_to_xlsx = "../data/operations.xlsx"


def main_page(user_data: str):
    """Функция возвращающая json-файл для Главной страницы"""
    logger.info("Формирование j-son файла для Главной")
    # Получение Приветственного сообщения
    welcome_message_str = welcome_message()

    # Получение Данных из файла xlsx
    data = xlsx_data_conversion(path_to_xlsx)

    # Перевод даты из одного формата в другой
    date_object = datetime.strptime(user_data, "%Y-%m-%d %H:%M:%S")
    date_str = date_object.strftime("%Y-%m-%d")

    # Фильтрация списка в диапазоне
    data = filter_list_by_data(data, end_date=date_str)

    # Получение номеров карт
    card_numbers = get_card_num(data)

    # Получение суммы трат по каждой карте
    total_exp = total_expenses(data, card_numbers)

    # Получение кэшбека по каждой карте
    cash_back = cashback_calculation(data, card_numbers)

    # Объединение словарей
    card_info_list = concat_card_data(total_exp, cash_back)

    # Получение топ пять трат
    top_five = top_five_transactions(data)

    # Получение курса валют
    current_currency = []
    user_settings = load_data()
    for el in user_settings["user_currencies"]:
        current_currency.append(get_currency_rate(el))

    # Получение стоимости акций
    stocks = get_s_p_500(user_settings["user_stocks"])
    result = {
        "greeting": welcome_message_str,
        "cards": card_info_list,
        "top_transactions": top_five,
        "currency_rates": current_currency,
        "stock_prices": stocks,
    }
    result = json.dumps(result, ensure_ascii=False)
    return result
