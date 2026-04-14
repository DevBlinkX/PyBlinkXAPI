# coding: utf-8
import pytest
import responses
import pyblinkxapi.exceptions as ex

import utils


def test_set_access_token(pyblinkxapi):
    """Check for token exception when invalid token is set."""
    pyblinkxapi.root = "https://smartapi.blinkx.in"
    pyblinkxapi.set_access_token("invalid_token")
    with pytest.raises(ex.TokenException):
        pyblinkxapi.positions()


@responses.activate
def test_positions(pyblinkxapi):
    """Test positions."""
    responses.add(
        responses.GET,
        "{0}{1}".format(pyblinkxapi.root, pyblinkxapi._routes["portfolio.positions"]),
        body=utils.get_response("portfolio.positions"),
        content_type="application/json"
    )
    positions = pyblinkxapi.positions()
    assert type(positions) == dict
    assert "day" in positions
    assert "net" in positions


@responses.activate
def test_holdings(pyblinkxapi):
    """Test holdings."""
    responses.add(
        responses.GET,
        "{0}{1}".format(pyblinkxapi.root, pyblinkxapi._routes["portfolio.holdings"]),
        body=utils.get_response("portfolio.holdings"),
        content_type="application/json"
    )
    holdings = pyblinkxapi.holdings()
    assert type(holdings) == list


@responses.activate
def test_auction_instruments(pyblinkxapi):
    """Test get_auction_instruments."""
    responses.add(
        responses.GET,
        "{0}{1}".format(pyblinkxapi.root, pyblinkxapi._routes["portfolio.holdings.auction"]),
        body=utils.get_response("portfolio.holdings.auction"),
        content_type="application/json"
    )
    auction_inst = pyblinkxapi.get_auction_instruments()
    assert type(auction_inst) == list


@responses.activate
def test_margins(pyblinkxapi):
    """Test margins."""
    responses.add(
        responses.GET,
        "{0}{1}".format(pyblinkxapi.root, pyblinkxapi._routes["user.margins"]),
        body=utils.get_response("user.margins"),
        content_type="application/json"
    )
    margins = pyblinkxapi.margins()
    assert type(margins) == dict
    assert pyblinkxapi.MARGIN_EQUITY in margins
    assert pyblinkxapi.MARGIN_COMMODITY in margins


@responses.activate
def test_profile(pyblinkxapi):
    """Test profile."""
    responses.add(
        responses.GET,
        "{0}{1}".format(pyblinkxapi.root, pyblinkxapi._routes["user.profile"]),
        body=utils.get_response("user.profile"),
        content_type="application/json"
    )
    profile = pyblinkxapi.profile()
    assert type(profile) == dict


@responses.activate
def test_orders(pyblinkxapi):
    """Test orders."""
    responses.add(
        responses.GET,
        "{0}{1}".format(pyblinkxapi.root, pyblinkxapi._routes["orders"]),
        body=utils.get_response("orders"),
        content_type="application/json"
    )
    orders = pyblinkxapi.orders()
    assert type(orders) == list


@responses.activate
def test_order_history(pyblinkxapi):
    """Test order history get."""
    url = pyblinkxapi._routes["order.info"].format(order_id="abc123")
    responses.add(
        responses.GET,
        "{0}{1}".format(pyblinkxapi.root, url),
        body=utils.get_response("order.info"),
        content_type="application/json"
    )
    trades = pyblinkxapi.order_history(order_id="abc123")
    assert type(trades) == list


@responses.activate
def test_trades(pyblinkxapi):
    """Test trades."""
    responses.add(
        responses.GET,
        "{0}{1}".format(pyblinkxapi.root, pyblinkxapi._routes["trades"]),
        body=utils.get_response("trades"),
        content_type="application/json"
    )
    trades = pyblinkxapi.trades()
    assert type(trades) == list


@responses.activate
def test_order_trades(pyblinkxapi):
    """Test order trades."""
    url = pyblinkxapi._routes["order.trades"].format(order_id="abc123")
    responses.add(
        responses.GET,
        "{0}{1}".format(pyblinkxapi.root, url),
        body=utils.get_response("trades"),
        content_type="application/json"
    )
    trades = pyblinkxapi.order_trades(order_id="abc123")
    assert type(trades) == list


@responses.activate
def test_instruments(pyblinkxapi):
    """Test instruments fetch."""
    responses.add(
        responses.GET,
        "{0}{1}".format(pyblinkxapi.root, pyblinkxapi._routes["market.instruments.all"]),
        body=utils.get_response("market.instruments.all"),
        content_type="text/csv"
    )
    trades = pyblinkxapi.instruments()
    assert type(trades) == list


@responses.activate
def test_instruments_exchangewise(pyblinkxapi):
    """Test instruments fetch."""
    responses.add(
        responses.GET,
        "{0}{1}".format(pyblinkxapi.root,
                        pyblinkxapi._routes["market.instruments"].format(exchange=pyblinkxapi.EXCHANGE_NSE)),
        body=utils.get_response("market.instruments"),
        content_type="text/csv"
    )
    trades = pyblinkxapi.instruments(exchange=pyblinkxapi.EXCHANGE_NSE)
    assert type(trades) == list


@responses.activate
def test_get_gtts(pyblinkxapi):
    """Test all gtts fetch."""
    responses.add(
        responses.GET,
        "{0}{1}".format(pyblinkxapi.root, pyblinkxapi._routes["gtt"]),
        body=utils.get_response("gtt"),
        content_type="application/json"
    )
    gtts = pyblinkxapi.get_gtts()
    assert type(gtts) == list


@responses.activate
def test_get_gtt(pyblinkxapi):
    """Test single gtt fetch."""
    responses.add(
        responses.GET,
        "{0}{1}".format(pyblinkxapi.root, pyblinkxapi._routes["gtt.info"].format(trigger_id=123)),
        body=utils.get_response("gtt.info"),
        content_type="application/json"
    )
    gtts = pyblinkxapi.get_gtt(123)
    print(gtts)
    assert gtts["id"] == 123


@responses.activate
def test_place_gtt(pyblinkxapi):
    """Test place gtt order."""
    responses.add(
        responses.POST,
        "{0}{1}".format(pyblinkxapi.root, pyblinkxapi._routes["gtt.place"]),
        body=utils.get_response("gtt.place"),
        content_type="application/json"
    )
    gtts = pyblinkxapi.place_gtt(
        trigger_type=pyblinkxapi.GTT_TYPE_SINGLE,
        tradingsymbol="INFY",
        exchange="NSE",
        trigger_values=[1],
        last_price=800,
        orders=[{
            "transaction_type": pyblinkxapi.TRANSACTION_TYPE_BUY,
            "quantity": 1,
            "order_type": pyblinkxapi.ORDER_TYPE_LIMIT,
            "product": pyblinkxapi.PRODUCT_CNC,
            "price": 1,
        }]
    )
    assert gtts["trigger_id"] == 123


@responses.activate
def test_modify_gtt(pyblinkxapi):
    """Test modify gtt order."""
    responses.add(
        responses.PUT,
        "{0}{1}".format(pyblinkxapi.root, pyblinkxapi._routes["gtt.modify"].format(trigger_id=123)),
        body=utils.get_response("gtt.modify"),
        content_type="application/json"
    )
    gtts = pyblinkxapi.modify_gtt(
        trigger_id=123,
        trigger_type=pyblinkxapi.GTT_TYPE_SINGLE,
        tradingsymbol="INFY",
        exchange="NSE",
        trigger_values=[1],
        last_price=800,
        orders=[{
            "transaction_type": pyblinkxapi.TRANSACTION_TYPE_BUY,
            "quantity": 1,
            "order_type": pyblinkxapi.ORDER_TYPE_LIMIT,
            "product": pyblinkxapi.PRODUCT_CNC,
            "price": 1,
        }]
    )
    assert gtts["trigger_id"] == 123


@responses.activate
def test_delete_gtt(pyblinkxapi):
    """Test delete gtt order."""
    responses.add(
        responses.DELETE,
        "{0}{1}".format(pyblinkxapi.root, pyblinkxapi._routes["gtt.delete"].format(trigger_id=123)),
        body=utils.get_response("gtt.delete"),
        content_type="application/json"
    )
    gtts = pyblinkxapi.delete_gtt(123)
    assert gtts["trigger_id"] == 123


@responses.activate
def test_order_margins(pyblinkxapi):
    """ Test order margins and charges """
    responses.add(
        responses.POST,
        "{0}{1}".format(pyblinkxapi.root, pyblinkxapi._routes["order.margins"]),
        body=utils.get_response("order.margins"),
        content_type="application/json"
    )
    order_param_single = [{
        "exchange": "NSE",
        "tradingsymbol": "INFY",
        "transaction_type": "BUY",
        "variety": "regular",
        "product": "MIS",
        "order_type": "MARKET",
        "quantity": 2
    }]

    margin_detail = pyblinkxapi.order_margins(order_param_single)
    assert margin_detail[0]['type'] == "equity"
    assert margin_detail[0]['total'] != 0
    assert margin_detail[0]['charges']['transaction_tax'] != 0
    assert margin_detail[0]['charges']['gst']['total'] != 0


@responses.activate
def test_basket_order_margins(pyblinkxapi):
    """ Test basket order margins and charges """
    responses.add(
        responses.POST,
        "{0}{1}".format(pyblinkxapi.root, pyblinkxapi._routes["order.margins.basket"]),
        body=utils.get_response("order.margins.basket"),
        content_type="application/json"
    )
    order_param_multi = [{
        "exchange": "NFO",
        "tradingsymbol": "NIFTY23JANFUT",
        "transaction_type": "BUY",
        "variety": "regular",
        "product": "MIS",
        "order_type": "MARKET",
        "quantity": 75
    },
        {
        "exchange": "NFO",
        "tradingsymbol": "NIFTY23JANFUT",
        "transaction_type": "BUY",
        "variety": "regular",
        "product": "MIS",
        "order_type": "MARKET",
        "quantity": 75
    }]

    margin_detail = pyblinkxapi.basket_order_margins(order_param_multi)
    assert margin_detail['orders'][0]['exposure'] != 0
    assert margin_detail['orders'][0]['type'] == "equity"
    assert margin_detail['orders'][0]['total'] != 0

@responses.activate
def test_virtual_contract_note(pyblinkxapi):
    """ Test virtual contract note charges """
    responses.add(
        responses.POST,
        "{0}{1}".format(pyblinkxapi.root, pyblinkxapi._routes["order.contract_note"]),
        body=utils.get_response("order.contract_note"),
        content_type="application/json"
    )

    order_book_params = [{
        "order_id": "111111111",
        "exchange": "NSE",
        "tradingsymbol": "SBIN",
        "transaction_type": "BUY",
        "variety": "regular",
        "product": "CNC",
        "order_type": "MARKET",
        "quantity": 1,
        "average_price": 560
    },
	{
        "order_id": "2222222222",
        "exchange": "MCX",
        "tradingsymbol": "GOLDPETAL23JULFUT",
        "transaction_type": "SELL",
        "variety": "regular",
        "product": "NRML",
        "order_type": "LIMIT",
        "quantity": 1,
        "average_price": 5862
    },
	{
        "order_id": "3333333333",
        "exchange": "NFO",
        "tradingsymbol": "NIFTY2371317900PE",
        "transaction_type": "BUY",
        "variety": "regular",
        "product": "NRML",
        "order_type": "LIMIT",
        "quantity": 100,
        "average_price": 1.5
    }]

    order_book_charges = pyblinkxapi.get_virtual_contract_note(order_book_params)
    assert order_book_charges[0]['charges']['transaction_tax_type'] == "stt"
    assert order_book_charges[0]['charges']['total'] != 0
    assert order_book_charges[1]['charges']['transaction_tax_type'] == "ctt"
    assert order_book_charges[1]['charges']['total'] != 0
