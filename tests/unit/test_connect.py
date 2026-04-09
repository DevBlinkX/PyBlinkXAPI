# coding: utf-8
import pytest
import responses
import blinkxtradingapi.exceptions as ex

import utils


def test_set_access_token(blinkxtradingapi):
    """Check for token exception when invalid token is set."""
    blinkxtradingapi.root = "https://smartapi.blinkx.in"
    blinkxtradingapi.set_access_token("invalid_token")
    with pytest.raises(ex.TokenException):
        blinkxtradingapi.positions()


@responses.activate
def test_positions(blinkxtradingapi):
    """Test positions."""
    responses.add(
        responses.GET,
        "{0}{1}".format(blinkxtradingapi.root, blinkxtradingapi._routes["portfolio.positions"]),
        body=utils.get_response("portfolio.positions"),
        content_type="application/json"
    )
    positions = blinkxtradingapi.positions()
    assert type(positions) == dict
    assert "day" in positions
    assert "net" in positions


@responses.activate
def test_holdings(blinkxtradingapi):
    """Test holdings."""
    responses.add(
        responses.GET,
        "{0}{1}".format(blinkxtradingapi.root, blinkxtradingapi._routes["portfolio.holdings"]),
        body=utils.get_response("portfolio.holdings"),
        content_type="application/json"
    )
    holdings = blinkxtradingapi.holdings()
    assert type(holdings) == list


@responses.activate
def test_auction_instruments(blinkxtradingapi):
    """Test get_auction_instruments."""
    responses.add(
        responses.GET,
        "{0}{1}".format(blinkxtradingapi.root, blinkxtradingapi._routes["portfolio.holdings.auction"]),
        body=utils.get_response("portfolio.holdings.auction"),
        content_type="application/json"
    )
    auction_inst = blinkxtradingapi.get_auction_instruments()
    assert type(auction_inst) == list


@responses.activate
def test_margins(blinkxtradingapi):
    """Test margins."""
    responses.add(
        responses.GET,
        "{0}{1}".format(blinkxtradingapi.root, blinkxtradingapi._routes["user.margins"]),
        body=utils.get_response("user.margins"),
        content_type="application/json"
    )
    margins = blinkxtradingapi.margins()
    assert type(margins) == dict
    assert blinkxtradingapi.MARGIN_EQUITY in margins
    assert blinkxtradingapi.MARGIN_COMMODITY in margins


@responses.activate
def test_profile(blinkxtradingapi):
    """Test profile."""
    responses.add(
        responses.GET,
        "{0}{1}".format(blinkxtradingapi.root, blinkxtradingapi._routes["user.profile"]),
        body=utils.get_response("user.profile"),
        content_type="application/json"
    )
    profile = blinkxtradingapi.profile()
    assert type(profile) == dict


@responses.activate
def test_orders(blinkxtradingapi):
    """Test orders."""
    responses.add(
        responses.GET,
        "{0}{1}".format(blinkxtradingapi.root, blinkxtradingapi._routes["orders"]),
        body=utils.get_response("orders"),
        content_type="application/json"
    )
    orders = blinkxtradingapi.orders()
    assert type(orders) == list


@responses.activate
def test_order_history(blinkxtradingapi):
    """Test order history get."""
    url = blinkxtradingapi._routes["order.info"].format(order_id="abc123")
    responses.add(
        responses.GET,
        "{0}{1}".format(blinkxtradingapi.root, url),
        body=utils.get_response("order.info"),
        content_type="application/json"
    )
    trades = blinkxtradingapi.order_history(order_id="abc123")
    assert type(trades) == list


@responses.activate
def test_trades(blinkxtradingapi):
    """Test trades."""
    responses.add(
        responses.GET,
        "{0}{1}".format(blinkxtradingapi.root, blinkxtradingapi._routes["trades"]),
        body=utils.get_response("trades"),
        content_type="application/json"
    )
    trades = blinkxtradingapi.trades()
    assert type(trades) == list


@responses.activate
def test_order_trades(blinkxtradingapi):
    """Test order trades."""
    url = blinkxtradingapi._routes["order.trades"].format(order_id="abc123")
    responses.add(
        responses.GET,
        "{0}{1}".format(blinkxtradingapi.root, url),
        body=utils.get_response("trades"),
        content_type="application/json"
    )
    trades = blinkxtradingapi.order_trades(order_id="abc123")
    assert type(trades) == list


@responses.activate
def test_instruments(blinkxtradingapi):
    """Test instruments fetch."""
    responses.add(
        responses.GET,
        "{0}{1}".format(blinkxtradingapi.root, blinkxtradingapi._routes["market.instruments.all"]),
        body=utils.get_response("market.instruments.all"),
        content_type="text/csv"
    )
    trades = blinkxtradingapi.instruments()
    assert type(trades) == list


@responses.activate
def test_instruments_exchangewise(blinkxtradingapi):
    """Test instruments fetch."""
    responses.add(
        responses.GET,
        "{0}{1}".format(blinkxtradingapi.root,
                        blinkxtradingapi._routes["market.instruments"].format(exchange=blinkxtradingapi.EXCHANGE_NSE)),
        body=utils.get_response("market.instruments"),
        content_type="text/csv"
    )
    trades = blinkxtradingapi.instruments(exchange=blinkxtradingapi.EXCHANGE_NSE)
    assert type(trades) == list


@responses.activate
def test_get_gtts(blinkxtradingapi):
    """Test all gtts fetch."""
    responses.add(
        responses.GET,
        "{0}{1}".format(blinkxtradingapi.root, blinkxtradingapi._routes["gtt"]),
        body=utils.get_response("gtt"),
        content_type="application/json"
    )
    gtts = blinkxtradingapi.get_gtts()
    assert type(gtts) == list


@responses.activate
def test_get_gtt(blinkxtradingapi):
    """Test single gtt fetch."""
    responses.add(
        responses.GET,
        "{0}{1}".format(blinkxtradingapi.root, blinkxtradingapi._routes["gtt.info"].format(trigger_id=123)),
        body=utils.get_response("gtt.info"),
        content_type="application/json"
    )
    gtts = blinkxtradingapi.get_gtt(123)
    print(gtts)
    assert gtts["id"] == 123


@responses.activate
def test_place_gtt(blinkxtradingapi):
    """Test place gtt order."""
    responses.add(
        responses.POST,
        "{0}{1}".format(blinkxtradingapi.root, blinkxtradingapi._routes["gtt.place"]),
        body=utils.get_response("gtt.place"),
        content_type="application/json"
    )
    gtts = blinkxtradingapi.place_gtt(
        trigger_type=blinkxtradingapi.GTT_TYPE_SINGLE,
        tradingsymbol="INFY",
        exchange="NSE",
        trigger_values=[1],
        last_price=800,
        orders=[{
            "transaction_type": blinkxtradingapi.TRANSACTION_TYPE_BUY,
            "quantity": 1,
            "order_type": blinkxtradingapi.ORDER_TYPE_LIMIT,
            "product": blinkxtradingapi.PRODUCT_CNC,
            "price": 1,
        }]
    )
    assert gtts["trigger_id"] == 123


@responses.activate
def test_modify_gtt(blinkxtradingapi):
    """Test modify gtt order."""
    responses.add(
        responses.PUT,
        "{0}{1}".format(blinkxtradingapi.root, blinkxtradingapi._routes["gtt.modify"].format(trigger_id=123)),
        body=utils.get_response("gtt.modify"),
        content_type="application/json"
    )
    gtts = blinkxtradingapi.modify_gtt(
        trigger_id=123,
        trigger_type=blinkxtradingapi.GTT_TYPE_SINGLE,
        tradingsymbol="INFY",
        exchange="NSE",
        trigger_values=[1],
        last_price=800,
        orders=[{
            "transaction_type": blinkxtradingapi.TRANSACTION_TYPE_BUY,
            "quantity": 1,
            "order_type": blinkxtradingapi.ORDER_TYPE_LIMIT,
            "product": blinkxtradingapi.PRODUCT_CNC,
            "price": 1,
        }]
    )
    assert gtts["trigger_id"] == 123


@responses.activate
def test_delete_gtt(blinkxtradingapi):
    """Test delete gtt order."""
    responses.add(
        responses.DELETE,
        "{0}{1}".format(blinkxtradingapi.root, blinkxtradingapi._routes["gtt.delete"].format(trigger_id=123)),
        body=utils.get_response("gtt.delete"),
        content_type="application/json"
    )
    gtts = blinkxtradingapi.delete_gtt(123)
    assert gtts["trigger_id"] == 123


@responses.activate
def test_order_margins(blinkxtradingapi):
    """ Test order margins and charges """
    responses.add(
        responses.POST,
        "{0}{1}".format(blinkxtradingapi.root, blinkxtradingapi._routes["order.margins"]),
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

    margin_detail = blinkxtradingapi.order_margins(order_param_single)
    assert margin_detail[0]['type'] == "equity"
    assert margin_detail[0]['total'] != 0
    assert margin_detail[0]['charges']['transaction_tax'] != 0
    assert margin_detail[0]['charges']['gst']['total'] != 0


@responses.activate
def test_basket_order_margins(blinkxtradingapi):
    """ Test basket order margins and charges """
    responses.add(
        responses.POST,
        "{0}{1}".format(blinkxtradingapi.root, blinkxtradingapi._routes["order.margins.basket"]),
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

    margin_detail = blinkxtradingapi.basket_order_margins(order_param_multi)
    assert margin_detail['orders'][0]['exposure'] != 0
    assert margin_detail['orders'][0]['type'] == "equity"
    assert margin_detail['orders'][0]['total'] != 0

@responses.activate
def test_virtual_contract_note(blinkxtradingapi):
    """ Test virtual contract note charges """
    responses.add(
        responses.POST,
        "{0}{1}".format(blinkxtradingapi.root, blinkxtradingapi._routes["order.contract_note"]),
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

    order_book_charges = blinkxtradingapi.get_virtual_contract_note(order_book_params)
    assert order_book_charges[0]['charges']['transaction_tax_type'] == "stt"
    assert order_book_charges[0]['charges']['total'] != 0
    assert order_book_charges[1]['charges']['transaction_tax_type'] == "ctt"
    assert order_book_charges[1]['charges']['total'] != 0
