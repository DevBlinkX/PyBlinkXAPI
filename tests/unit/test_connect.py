# coding: utf-8
import pytest
import responses
import blinkxconnect.exceptions as ex

import utils


def test_set_access_token(blinkxconnect):
    """Check for token exception when invalid token is set."""
    blinkxconnect.root = "https://smartapi.blinkx.in"
    blinkxconnect.set_access_token("invalid_token")
    with pytest.raises(ex.TokenException):
        blinkxconnect.positions()


@responses.activate
def test_positions(blinkxconnect):
    """Test positions."""
    responses.add(
        responses.GET,
        "{0}{1}".format(blinkxconnect.root, blinkxconnect._routes["portfolio.positions"]),
        body=utils.get_response("portfolio.positions"),
        content_type="application/json"
    )
    positions = blinkxconnect.positions()
    assert type(positions) == dict
    assert "day" in positions
    assert "net" in positions


@responses.activate
def test_holdings(blinkxconnect):
    """Test holdings."""
    responses.add(
        responses.GET,
        "{0}{1}".format(blinkxconnect.root, blinkxconnect._routes["portfolio.holdings"]),
        body=utils.get_response("portfolio.holdings"),
        content_type="application/json"
    )
    holdings = blinkxconnect.holdings()
    assert type(holdings) == list


@responses.activate
def test_auction_instruments(blinkxconnect):
    """Test get_auction_instruments."""
    responses.add(
        responses.GET,
        "{0}{1}".format(blinkxconnect.root, blinkxconnect._routes["portfolio.holdings.auction"]),
        body=utils.get_response("portfolio.holdings.auction"),
        content_type="application/json"
    )
    auction_inst = blinkxconnect.get_auction_instruments()
    assert type(auction_inst) == list


@responses.activate
def test_margins(blinkxconnect):
    """Test margins."""
    responses.add(
        responses.GET,
        "{0}{1}".format(blinkxconnect.root, blinkxconnect._routes["user.margins"]),
        body=utils.get_response("user.margins"),
        content_type="application/json"
    )
    margins = blinkxconnect.margins()
    assert type(margins) == dict
    assert blinkxconnect.MARGIN_EQUITY in margins
    assert blinkxconnect.MARGIN_COMMODITY in margins


@responses.activate
def test_profile(blinkxconnect):
    """Test profile."""
    responses.add(
        responses.GET,
        "{0}{1}".format(blinkxconnect.root, blinkxconnect._routes["user.profile"]),
        body=utils.get_response("user.profile"),
        content_type="application/json"
    )
    profile = blinkxconnect.profile()
    assert type(profile) == dict


@responses.activate
def test_orders(blinkxconnect):
    """Test orders."""
    responses.add(
        responses.GET,
        "{0}{1}".format(blinkxconnect.root, blinkxconnect._routes["orders"]),
        body=utils.get_response("orders"),
        content_type="application/json"
    )
    orders = blinkxconnect.orders()
    assert type(orders) == list


@responses.activate
def test_order_history(blinkxconnect):
    """Test order history get."""
    url = blinkxconnect._routes["order.info"].format(order_id="abc123")
    responses.add(
        responses.GET,
        "{0}{1}".format(blinkxconnect.root, url),
        body=utils.get_response("order.info"),
        content_type="application/json"
    )
    trades = blinkxconnect.order_history(order_id="abc123")
    assert type(trades) == list


@responses.activate
def test_trades(blinkxconnect):
    """Test trades."""
    responses.add(
        responses.GET,
        "{0}{1}".format(blinkxconnect.root, blinkxconnect._routes["trades"]),
        body=utils.get_response("trades"),
        content_type="application/json"
    )
    trades = blinkxconnect.trades()
    assert type(trades) == list


@responses.activate
def test_order_trades(blinkxconnect):
    """Test order trades."""
    url = blinkxconnect._routes["order.trades"].format(order_id="abc123")
    responses.add(
        responses.GET,
        "{0}{1}".format(blinkxconnect.root, url),
        body=utils.get_response("trades"),
        content_type="application/json"
    )
    trades = blinkxconnect.order_trades(order_id="abc123")
    assert type(trades) == list


@responses.activate
def test_instruments(blinkxconnect):
    """Test instruments fetch."""
    responses.add(
        responses.GET,
        "{0}{1}".format(blinkxconnect.root, blinkxconnect._routes["market.instruments.all"]),
        body=utils.get_response("market.instruments.all"),
        content_type="text/csv"
    )
    trades = blinkxconnect.instruments()
    assert type(trades) == list


@responses.activate
def test_instruments_exchangewise(blinkxconnect):
    """Test instruments fetch."""
    responses.add(
        responses.GET,
        "{0}{1}".format(blinkxconnect.root,
                        blinkxconnect._routes["market.instruments"].format(exchange=blinkxconnect.EXCHANGE_NSE)),
        body=utils.get_response("market.instruments"),
        content_type="text/csv"
    )
    trades = blinkxconnect.instruments(exchange=blinkxconnect.EXCHANGE_NSE)
    assert type(trades) == list


@responses.activate
def test_get_gtts(blinkxconnect):
    """Test all gtts fetch."""
    responses.add(
        responses.GET,
        "{0}{1}".format(blinkxconnect.root, blinkxconnect._routes["gtt"]),
        body=utils.get_response("gtt"),
        content_type="application/json"
    )
    gtts = blinkxconnect.get_gtts()
    assert type(gtts) == list


@responses.activate
def test_get_gtt(blinkxconnect):
    """Test single gtt fetch."""
    responses.add(
        responses.GET,
        "{0}{1}".format(blinkxconnect.root, blinkxconnect._routes["gtt.info"].format(trigger_id=123)),
        body=utils.get_response("gtt.info"),
        content_type="application/json"
    )
    gtts = blinkxconnect.get_gtt(123)
    print(gtts)
    assert gtts["id"] == 123


@responses.activate
def test_place_gtt(blinkxconnect):
    """Test place gtt order."""
    responses.add(
        responses.POST,
        "{0}{1}".format(blinkxconnect.root, blinkxconnect._routes["gtt.place"]),
        body=utils.get_response("gtt.place"),
        content_type="application/json"
    )
    gtts = blinkxconnect.place_gtt(
        trigger_type=blinkxconnect.GTT_TYPE_SINGLE,
        tradingsymbol="INFY",
        exchange="NSE",
        trigger_values=[1],
        last_price=800,
        orders=[{
            "transaction_type": blinkxconnect.TRANSACTION_TYPE_BUY,
            "quantity": 1,
            "order_type": blinkxconnect.ORDER_TYPE_LIMIT,
            "product": blinkxconnect.PRODUCT_CNC,
            "price": 1,
        }]
    )
    assert gtts["trigger_id"] == 123


@responses.activate
def test_modify_gtt(blinkxconnect):
    """Test modify gtt order."""
    responses.add(
        responses.PUT,
        "{0}{1}".format(blinkxconnect.root, blinkxconnect._routes["gtt.modify"].format(trigger_id=123)),
        body=utils.get_response("gtt.modify"),
        content_type="application/json"
    )
    gtts = blinkxconnect.modify_gtt(
        trigger_id=123,
        trigger_type=blinkxconnect.GTT_TYPE_SINGLE,
        tradingsymbol="INFY",
        exchange="NSE",
        trigger_values=[1],
        last_price=800,
        orders=[{
            "transaction_type": blinkxconnect.TRANSACTION_TYPE_BUY,
            "quantity": 1,
            "order_type": blinkxconnect.ORDER_TYPE_LIMIT,
            "product": blinkxconnect.PRODUCT_CNC,
            "price": 1,
        }]
    )
    assert gtts["trigger_id"] == 123


@responses.activate
def test_delete_gtt(blinkxconnect):
    """Test delete gtt order."""
    responses.add(
        responses.DELETE,
        "{0}{1}".format(blinkxconnect.root, blinkxconnect._routes["gtt.delete"].format(trigger_id=123)),
        body=utils.get_response("gtt.delete"),
        content_type="application/json"
    )
    gtts = blinkxconnect.delete_gtt(123)
    assert gtts["trigger_id"] == 123


@responses.activate
def test_order_margins(blinkxconnect):
    """ Test order margins and charges """
    responses.add(
        responses.POST,
        "{0}{1}".format(blinkxconnect.root, blinkxconnect._routes["order.margins"]),
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

    margin_detail = blinkxconnect.order_margins(order_param_single)
    assert margin_detail[0]['type'] == "equity"
    assert margin_detail[0]['total'] != 0
    assert margin_detail[0]['charges']['transaction_tax'] != 0
    assert margin_detail[0]['charges']['gst']['total'] != 0


@responses.activate
def test_basket_order_margins(blinkxconnect):
    """ Test basket order margins and charges """
    responses.add(
        responses.POST,
        "{0}{1}".format(blinkxconnect.root, blinkxconnect._routes["order.margins.basket"]),
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

    margin_detail = blinkxconnect.basket_order_margins(order_param_multi)
    assert margin_detail['orders'][0]['exposure'] != 0
    assert margin_detail['orders'][0]['type'] == "equity"
    assert margin_detail['orders'][0]['total'] != 0

@responses.activate
def test_virtual_contract_note(blinkxconnect):
    """ Test virtual contract note charges """
    responses.add(
        responses.POST,
        "{0}{1}".format(blinkxconnect.root, blinkxconnect._routes["order.contract_note"]),
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

    order_book_charges = blinkxconnect.get_virtual_contract_note(order_book_params)
    assert order_book_charges[0]['charges']['transaction_tax_type'] == "stt"
    assert order_book_charges[0]['charges']['total'] != 0
    assert order_book_charges[1]['charges']['transaction_tax_type'] == "ctt"
    assert order_book_charges[1]['charges']['total'] != 0
