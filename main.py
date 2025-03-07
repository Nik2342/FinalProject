import pandas as pd

from src.get_data import xlsx_data_conversion
from src.reports import spending_by_category
from src.services import get_bank_operations
from src.views import main_page


path_to_xlsx = "data/operations.xlsx"


def all_func():
    """Основная функция"""

    user_str = input("Введите дату в формате '%Y-%m-%d %H:%M:%S'\n")
    print(main_page(user_str))

    user_search_str = input("Введите слово для поиска\n")
    data = xlsx_data_conversion(path_to_xlsx)
    print(get_bank_operations(data, user_search_str))

    user_search_str = input("Введите название категории\n")
    data = pd.DataFrame(data)
    _user_date = input("Введите дату(опционально, если даты нет введите None)")
    print(spending_by_category(data,user_search_str))
