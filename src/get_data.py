import logging

import pandas as pd

logger = logging.getLogger("get_data")
logger.setLevel(logging.DEBUG)
console_handler = logging.StreamHandler()
logger.addHandler(console_handler)
file_formatter = logging.Formatter("%(asctime)s %(levelname)s : %(message)s")
console_handler.setFormatter(file_formatter)


def xlsx_data_conversion(path) -> list:
    """Функция считывания xlsx-файлов"""
    xlsx_list = []
    try:
        logger.info("Считывание данных с файла")
        data = pd.read_excel(path)
        xlsx_list = data.to_dict(orient="records")
        xlsx_list = [row for row in xlsx_list if not any(pd.isna(value) for value in row.values())]
    except FileNotFoundError:
        logger.info("Файл не найден")
    except Exception as ex:
        logger.info(f"{ex}")
        xlsx_list = []
    finally:
        return xlsx_list
