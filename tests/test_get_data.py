from unittest.mock import patch, mock_open

from src.get_data import xlsx_data_conversion


@patch("builtins.open", new_callable=mock_open, read_data="")
def test_xlsx_empty_file(mock_file) -> None:

    data = xlsx_data_conversion("data/operations.xlsx")

    assert data == []


@patch("builtins.open", new_callable=mock_open, read_data='{"amount": 3598919}')
def test_xlsx_not_a_list(mock_file):

    data = xlsx_data_conversion("data/operations.xlsx")

    assert data == []


@patch("builtins.open", side_effect=FileNotFoundError)
def test_xlsx_file_not_found(mock_file) -> None:

    data = xlsx_data_conversion("data/operations.xlsx")

    assert data == []