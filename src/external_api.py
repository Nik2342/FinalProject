import logging
import os

import requests
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("API_KEY")

logger = logging.getLogger("external_api")
logger.setLevel(logging.DEBUG)
console_handler = logging.StreamHandler()
logger.addHandler(console_handler)
file_formatter = logging.Formatter("%(asctime)s %(levelname)s : %(message)s")
console_handler.setFormatter(file_formatter)


def get_currency_rate(currency_code):
    """Функция для получения валюты"""
    logger.info("Получение курса валюты")
    url = "https://www.cbr-xml-daily.ru//daily_json.js"
    response = requests.get(url)
    data = response.json()
    currency_data = data["Valute"].get(currency_code)
    return {
        "currency_code": currency_code,
        "rate": currency_data["Value"],
    }


def get_s_p_500(stocks):
    """Функция для получения информации об акциях"""
    logger.info("Получение стоймости акций")
    result = []
    sorted_result = []
    url = "http://api.marketstack.com/v1/eod"
    querystring = {
        "access_key": {API_KEY},
        "symbols": "AAPL,AMZN,GOOGL,MSFT,TSLA",
        "limit": "5",
    }
    response = requests.get(url, params=querystring)
    data = response.json()
    for el in data["data"]:
        result.append({"stock": el["symbol"], "price": el["close"]})
    sorted_result = sorted(result, key=lambda x: x.get("stock"))
    return sorted_result
