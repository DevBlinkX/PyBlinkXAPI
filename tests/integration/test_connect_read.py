# coding: utf-8

import pytest
from mock import Mock
import utils
import time
import datetime
import warnings
import pyblinkxapi.exceptions as ex


def test_request_pool():
    from pyblinkxapi import PyBlinkXAPI
    pool = {
        "pool_connections": 10,
        "pool_maxsize": 10,
        "max_retries": 0,
        "pool_block": False
    }

    blinkx = PyBlinkXAPI(api_key="random", access_token="random", pool=pool)

    with pytest.raises(ex.TokenException):
        blinkx.orders()


def test_set_access_token(pyblinkxapi):
    """Check for token exception when invalid token is set."""
    pyblinkxapi.set_access_token("invalid_token")
    with pytest.raises(ex.TokenException):
        pyblinkxapi.positions()


def test_set_session_expiry_hook(pyblinkxapi):
    """Test token exception callback"""
    with pytest.raises(TypeError):
        pyblinkxapi.set_session_expiry_hook(123)

    callback = Mock()
    pyblinkxapi.set_session_expiry_hook(callback)
    pyblinkxapi.set_access_token("some_invalid_token")
    with pytest.raises(ex.TokenException):
        pyblinkxapi.orders()
    callback.assert_called_with()


def test_positions(pyblinkxapi):
    """Test positions."""
    positions = pyblinkxapi.positions()
    mock_resp = utils.get_json_response("portfolio.positions")["data"]
    utils.assert_responses(positions, mock_resp)


def test_holdings(pyblinkxapi):
    """Test holdings."""
    holdings = pyblinkxapi.holdings()
    mock_resp = utils.get_json_response("portfolio.holdings")["data"]
    utils.assert_responses(holdings, mock_resp)


def test_auction_instruments(pyblinkxapi):
    """ Test get_auction_instruments """
    auction_inst = pyblinkxapi.get_auction_instruments()
    mock_resp = utils.get_json_response("portfolio.holdings.auction")["data"]
    utils.assert_responses(auction_inst, mock_resp)


def test_margins(pyblinkxapi):
    """Test margins."""
    margins = pyblinkxapi.margins()
    mock_resp = utils.get_json_response("user.margins")["data"]
    utils.assert_responses(margins, mock_resp)


def test_orders(pyblinkxapi):
    """Test orders get."""
    orders = pyblinkxapi.orders()
    assert type(orders) == list


def test_order_history(pyblinkxapi):
    """Test individual order get."""
    orders = pyblinkxapi.orders()

    if len(orders) == 0:
        warnings.warn(UserWarning("Order info: Couldn't perform individual order test since orderbook is empty."))
        return

    order = pyblinkxapi.order_history(order_id=orders[0]["order_id"])

    mock_resp = utils.get_json_response("order.info")["data"]
    utils.assert_responses(order, mock_resp)


def test_trades(pyblinkxapi):
    """Test trades."""
    trades = pyblinkxapi.trades()
    mock_resp = utils.get_json_response("trades")["data"]
    utils.assert_responses(trades, mock_resp)


def test_order_trades(pyblinkxapi):
    """Test individual order get."""
    trades = pyblinkxapi.trades()

    if len(trades) == 0:
        warnings.warn(UserWarning("Trades: Couldn't perform individual order test since trades is empty."))
        return

    order_trades = pyblinkxapi.order_trades(order_id=trades[0]["order_id"])

    mock_resp = utils.get_json_response("order.trades")["data"]
    utils.assert_responses(order_trades, mock_resp)


def test_all_instruments(pyblinkxapi):
    """Test instruments fetch."""
    instruments = pyblinkxapi.instruments()
    mock_resp = pyblinkxapi._parse_instruments(utils.get_response("market.instruments"))
    utils.assert_responses(instruments, mock_resp)


def test_exchange_instruments(pyblinkxapi):
    """Test instruments fetch."""
    instruments = pyblinkxapi.instruments(exchange=pyblinkxapi.EXCHANGE_NSE)
    mock_resp = pyblinkxapi._parse_instruments(utils.get_response("market.instruments"))
    utils.assert_responses(instruments, mock_resp)


# Historical API tests
######################

@pytest.mark.parametrize("max_interval,candle_interval", [
    (30, "minute"),
    (365, "hour"),
    (2000, "day"),
    (90, "3minute"),
    (90, "5minute"),
    (90, "10minute"),
    (180, "15minute"),
    (180, "30minute"),
    (365, "60minute")
], ids=[
    "minute",
    "hour",
    "day",
    "3minute",
    "5minute",
    "10minute",
    "15minute",
    "30minute",
    "60minute",
])
def test_historical_data_intervals(max_interval, candle_interval, pyblinkxapi):
    """Test historical data for each intervals"""
    instrument_token = 256265
    to_date = datetime.datetime.now()
    diff = int(max_interval / 3)

    from_date = (to_date - datetime.timedelta(days=diff))

    data = pyblinkxapi.historical_data(instrument_token, from_date, to_date, candle_interval)
    mock_resp = pyblinkxapi._format_historical(utils.get_json_response("market.historical")["data"])
    utils.assert_responses(data, mock_resp)

    from_date = (to_date - datetime.timedelta(days=(max_interval + 1)))
    with pytest.raises(ex.InputException):
        pyblinkxapi.historical_data(instrument_token, from_date, to_date, candle_interval)


def test_quote(pyblinkxapi):
    """Test quote."""
    instruments = ["NSE:INFY"]

    time.sleep(1.1)
    quote = pyblinkxapi.quote(instruments)
    mock_resp = utils.get_json_response("market.quote")["data"]
    utils.assert_responses(quote, mock_resp)

    time.sleep(1.1)
    quote = pyblinkxapi.quote(*instruments)
    mock_resp = utils.get_json_response("market.quote")["data"]
    utils.assert_responses(quote, mock_resp)


def test_quote_ohlc(pyblinkxapi):
    """Test ohlc."""
    instruments = ["NSE:INFY"]

    time.sleep(1.1)
    ohlc = pyblinkxapi.ohlc(instruments)
    mock_resp = utils.get_json_response("market.quote.ohlc")["data"]
    utils.assert_responses(ohlc, mock_resp)

    time.sleep(1.1)
    ohlc = pyblinkxapi.ohlc(*instruments)
    mock_resp = utils.get_json_response("market.quote.ohlc")["data"]
    utils.assert_responses(ohlc, mock_resp)


def test_quote_ltp(pyblinkxapi):
    """Test ltp."""
    instruments = ["NSE:INFY"]

    time.sleep(1.1)
    ltp = pyblinkxapi.ltp(instruments)
    mock_resp = utils.get_json_response("market.quote.ltp")["data"]
    utils.assert_responses(ltp, mock_resp)

    time.sleep(1.1)
    ltp = pyblinkxapi.ltp(*instruments)
    mock_resp = utils.get_json_response("market.quote.ltp")["data"]
    utils.assert_responses(ltp, mock_resp)
