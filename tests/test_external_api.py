from unittest.mock import patch

from src.external_api import get_currency_rate, get_s_p_500


@patch("src.external_api.requests.get")
def test_get_currency_rate_usd(mock_currency):
    currency_code = "USD"
    mock_response = {"Valute": {"USD": {"Value": 90.0}, "EUR": {"Value": 100.0}}}
    mock_currency.return_value.status_code = 200
    mock_currency.return_value.json.return_value = mock_response
    result = get_currency_rate(currency_code)
    assert result == {"currency_code": currency_code, "rate": 90.0}


@patch("src.external_api.requests.get")
def test_get_currency_rate_eur(mock_currency):
    currency_code = "EUR"
    mock_response = {"Valute": {"USD": {"Value": 90.0}, "EUR": {"Value": 100.0}}}
    mock_currency.return_value.status_code = 200
    mock_currency.return_value.json.return_value = mock_response
    result = get_currency_rate(currency_code)
    assert result == {"currency_code": currency_code, "rate": 100.0}


@patch("src.external_api.requests.get")
def test_get_s_p_500(mock_s_p):
    mock_response = {
        "data": [
            {"symbol": "AAPL", "close": 150.0},
            {"symbol": "AMZN", "close": 3200.0},
            {"symbol": "GOOGL", "close": 2800.0},
            {"symbol": "MSFT", "close": 299.0},
            {"symbol": "TSLA", "close": 800.0},
        ]
    }
    mock_s_p.return_value.status_code = 200
    mock_s_p.return_value.json.return_value = mock_response
    result = get_s_p_500(["AAPL", "AMZN", "GOOGL", "MSFT", "TSLA"])
    assert result == [
        {"stock": "AAPL", "price": 150.0},
        {"stock": "AMZN", "price": 3200.0},
        {"stock": "GOOGL", "price": 2800.0},
        {"stock": "MSFT", "price": 299.0},
        {"stock": "TSLA", "price": 800.0},
    ]
