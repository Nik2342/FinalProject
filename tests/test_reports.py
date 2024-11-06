from unittest.mock import mock_open, patch

from src.reports import log


@log("test_log.txt")
def my_function(x):
    return x**2


@patch("builtins.open", new_callable=mock_open)
def test_log_decorator(mocked_open):
    result = my_function(5)
    assert result == 25
    mocked_open.assert_any_call("test_log.txt", "a", encoding="utf-8")
    mocked_open().write.assert_any_call("my_function 25\n")
