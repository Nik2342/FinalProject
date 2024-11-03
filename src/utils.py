import datetime
import json
import logging


logger = logging.getLogger("utils")
logger.setLevel(logging.DEBUG)
console_handler = logging.StreamHandler()
logger.addHandler(console_handler)
file_formatter = logging.Formatter("%(asctime)s %(levelname)s : %(message)s")
console_handler.setFormatter(file_formatter)


def welcome_message() -> str:
    """Функция приветствия"""
    welcome_message_str = ""
    logger.info("Получение даты")
    current_hour = datetime.datetime.now().hour
    logger.info("Выбор приветствия по условию")
    if 4 <= current_hour < 10:
        welcome_message_str = "Доброе утро"
    if 10 <= current_hour < 16:
        welcome_message_str = "Добрый день"
    if 16 <= current_hour < 22:
        welcome_message_str = "Добрый вечер"
    if 22 <= current_hour < 24 or 0 <= current_hour < 4:
        welcome_message_str = "Доброй ночи"
    return welcome_message_str


def filter_list_by_data(list_dict, start_date=None, end_date=None):
    """Функия фильтрации списка словарей в определенном диапазоне времени"""
    logger.info("Проверка:Задана ли начальная дата пользователем")
    if start_date is None:
        logger.info("Установка начальной даты, если пользователь не задал")
        start_date = datetime.datetime(datetime.datetime.now().year, datetime.datetime.now().month, 1).date()
    else:
        logger.info("Установка начальной даты, заданной пользователем")
        start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d").date()

    logger.info("Проверка:Задана ли конечная дата пользователем")
    if end_date is None:
        logger.info("Установка конечной даты, если пользователь не задал")
        end_date = datetime.datetime.now().date()
    else:
        logger.info("Установка конечной даты, заданной пользователем")
        end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d").date()
    filtered_data = []
    logger.info("Сортировка данных по заданным датам")
    for x in list_dict:
        if "Дата операции" in x:
            try:
                operation_date = datetime.datetime.strptime(x["Дата операции"], "%d.%m.%Y %H:%M:%S").date()
                if start_date <= operation_date <= end_date:
                    filtered_data.append(x)
            except ValueError:
                logger.error(f"Неверный формат даты для записи: {x}")
                print(f"Неверный формат даты для записи: {x}")

    return filtered_data


def get_card_num(list_dict: list) -> list:
    """Функция получения номера карты"""
    result = []
    logger.info("Получение номера карты")
    for el in list_dict:
        if el["Номер карты"][1:] not in result:
            result.append(el["Номер карты"][1:])
    return result


def total_expenses(list_dict: list, list_card: list) -> dict:
    """Функция для подсчета трат по картам"""
    result = 0.0
    result_dict = {}
    logger.info("Подсчеты трат по картам")
    for el in list_dict:
        card_number = el["Номер карты"][1:]
        amount = float(el["Сумма операции"])
        if card_number not in list_card:
            result_dict[card_number] = 0.0
            if amount < 0.0:
                result += amount
            result_dict[card_number] = result
        else:
            if amount < 0.0:
                result += amount
            result_dict[card_number] = result
    logger.info("Изменение знака значений в словаре")
    for key in result_dict:
        result_dict[key] = round(result_dict[key] * -1, 1)
    return result_dict


def cashback_calculation(list_dict: list, list_card: list) -> dict:
    """Функция для подсчета кэшбека по картам"""
    result = 0
    result_dict = {}
    logger.info("Подсчеты кэшбека по картам")
    for el in list_dict:
        card_number = el["Номер карты"][1:]
        value = float(el["Сумма операции"]) * -1
        if card_number not in list_card:
            result_dict[card_number] = 0.0
            if value > 100.0:
                result += value // 100
            result_dict[card_number] = result
        else:
            if value > 100.0:
                result += value // 100
            result_dict[card_number] = result
    return result_dict


def concat_card_data(exp_dict: dict, cashb_dict: dict) -> list:
    """Функция возвращающая итоговый список со словарями карт"""
    result = []
    logger.info("Создание итогового словаря")
    for key in exp_dict.keys():
        result.append({"last_digits": key, "total_spent": exp_dict[key], "cashback": cashb_dict.get(key)})
    return result


def top_five_transactions(list_dict: list) -> list:
    """Функция для сортировки топ 5 операций"""
    logger.info("Сортировка данных по сумме операции")
    filtred_list = sorted(list_dict, key=lambda x: abs(x.get("Сумма операции")), reverse=True)
    i = 0
    result = []
    logger.info("Получение топ-5 транзакций")
    for el in filtred_list:
        if i < 5:
            result.append(
                {
                    "date": el["Дата платежа"],
                    "amount": el["Сумма операции"],
                    "category": el["Категория"],
                    "description": el["Описание"],
                }
            )
            i += 1
    return result


def load_data(path):
    """Функция получения данных с json-файла"""
    logger.info("Получение данных с json-файла")
    with open(path, "r") as file:
        data = json.load(file)
    return data
