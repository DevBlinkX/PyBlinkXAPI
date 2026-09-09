# coding: utf-8
import pytest
import responses
import pyjmproapi.exceptions as ex

import utils


def test_set_access_token(pyjmproapi):
    """Check for token exception when invalid token is set."""
    pyjmproapi.root = "https://api.jmpro.in"
    pyjmproapi.set_access_token("invalid_token")
    with pytest.raises(ex.TokenException):
        pyjmproapi.positions()


@responses.activate
def test_positions(pyjmproapi):
    """Test positions."""
    responses.add(
        responses.GET,
        "{0}{1}".format(pyjmproapi.root, pyjmproapi._routes["portfolio.positions"]),
        body=utils.get_response("portfolio.positions"),
        content_type="application/json"
    )
    positions = pyjmproapi.positions()
    assert type(positions) == dict
    assert "day" in positions
    assert "net" in positions


@responses.activate
def test_holdings(pyjmproapi):
    """Test holdings."""
    responses.add(
        responses.GET,
        "{0}{1}".format(pyjmproapi.root, pyjmproapi._routes["portfolio.holdings"]),
        body=utils.get_response("portfolio.holdings"),
        content_type="application/json"
    )
    holdings = pyjmproapi.holdings()
    assert type(holdings) == list


@responses.activate
def test_auction_instruments(pyjmproapi):
    """Test get_auction_instruments."""
    responses.add(
        responses.GET,
        "{0}{1}".format(pyjmproapi.root, pyjmproapi._routes["portfolio.holdings.auction"]),
        body=utils.get_response("portfolio.holdings.auction"),
        content_type="application/json"
    )
    auction_inst = pyjmproapi.get_auction_instruments()
    assert type(auction_inst) == list


@responses.activate
def test_margins(pyjmproapi):
    """Test margins."""
    responses.add(
        responses.GET,
        "{0}{1}".format(pyjmproapi.root, pyjmproapi._routes["user.margins"]),
        body=utils.get_response("user.margins"),
        content_type="application/json"
    )
    margins = pyjmproapi.margins()
    assert type(margins) == dict
    assert pyjmproapi.MARGIN_EQUITY in margins
    assert pyjmproapi.MARGIN_COMMODITY in margins


@responses.activate
def test_profile(pyjmproapi):
    """Test profile."""
    responses.add(
        responses.GET,
        "{0}{1}".format(pyjmproapi.root, pyjmproapi._routes["user.profile"]),
        body=utils.get_response("user.profile"),
        content_type="application/json"
    )
    profile = pyjmproapi.profile()
    assert type(profile) == dict


@responses.activate
def test_orders(pyjmproapi):
    """Test orders."""
    responses.add(
        responses.GET,
        "{0}{1}".format(pyjmproapi.root, pyjmproapi._routes["orders"]),
        body=utils.get_response("orders"),
        content_type="application/json"
    )
    orders = pyjmproapi.orders()
    assert type(orders) == list


@responses.activate
def test_order_history(pyjmproapi):
    """Test order history get."""
    url = pyjmproapi._routes["order.info"].format(order_id="abc123")
    responses.add(
        responses.GET,
        "{0}{1}".format(pyjmproapi.root, url),
        body=utils.get_response("order.info"),
        content_type="application/json"
    )
    trades = pyjmproapi.order_history(order_id="abc123")
    assert type(trades) == list


@responses.activate
def test_trades(pyjmproapi):
    """Test trades."""
    responses.add(
        responses.GET,
        "{0}{1}".format(pyjmproapi.root, pyjmproapi._routes["trades"]),
        body=utils.get_response("trades"),
        content_type="application/json"
    )
    trades = pyjmproapi.trades()
    assert type(trades) == list


@responses.activate
def test_order_trades(pyjmproapi):
    """Test order trades."""
    url = pyjmproapi._routes["order.trades"].format(order_id="abc123")
    responses.add(
        responses.GET,
        "{0}{1}".format(pyjmproapi.root, url),
        body=utils.get_response("trades"),
        content_type="application/json"
    )
    trades = pyjmproapi.order_trades(order_id="abc123")
    assert type(trades) == list


@responses.activate
def test_instruments(pyjmproapi):
    """Test instruments fetch."""
    responses.add(
        responses.GET,
        "{0}{1}".format(pyjmproapi.root, pyjmproapi._routes["market.instruments.all"]),
        body=utils.get_response("market.instruments.all"),
        content_type="text/csv"
    )
    trades = pyjmproapi.instruments()
    assert type(trades) == list


@responses.activate
def test_instruments_exchangewise(pyjmproapi):
    """Test instruments fetch."""
    responses.add(
        responses.GET,
        "{0}{1}".format(pyjmproapi.root,
                        pyjmproapi._routes["market.instruments"].format(exchange=pyjmproapi.EXCHANGE_NSE)),
        body=utils.get_response("market.instruments"),
        content_type="text/csv"
    )
    trades = pyjmproapi.instruments(exchange=pyjmproapi.EXCHANGE_NSE)
    assert type(trades) == list


@responses.activate
def test_get_gtts(pyjmproapi):
    """Test all gtts fetch."""
    responses.add(
        responses.GET,
        "{0}{1}".format(pyjmproapi.root, pyjmproapi._routes["gtt"]),
        body=utils.get_response("gtt"),
        content_type="application/json"
    )
    gtts = pyjmproapi.get_gtts()
    assert type(gtts) == list


@responses.activate
def test_get_gtt(pyjmproapi):
    """Test single gtt fetch."""
    responses.add(
        responses.GET,
        "{0}{1}".format(pyjmproapi.root, pyjmproapi._routes["gtt.info"].format(trigger_id=123)),
        body=utils.get_response("gtt.info"),
        content_type="application/json"
    )
    gtts = pyjmproapi.get_gtt(123)
    print(gtts)
    assert gtts["id"] == 123


@responses.activate
def test_place_gtt(pyjmproapi):
    """Test place gtt order."""
    responses.add(
        responses.POST,
        "{0}{1}".format(pyjmproapi.root, pyjmproapi._routes["gtt.place"]),
        body=utils.get_response("gtt.place"),
        content_type="application/json"
    )
    gtts = pyjmproapi.place_gtt(
        trigger_type=pyjmproapi.GTT_TYPE_SINGLE,
        tradingsymbol="INFY",
        exchange="NSE",
        trigger_values=[1],
        last_price=800,
        orders=[{
            "transaction_type": pyjmproapi.TRANSACTION_TYPE_BUY,
            "quantity": 1,
            "order_type": pyjmproapi.ORDER_TYPE_LIMIT,
            "product": pyjmproapi.PRODUCT_CNC,
            "price": 1,
        }]
    )
    assert gtts["trigger_id"] == 123


@responses.activate
def test_modify_gtt(pyjmproapi):
    """Test modify gtt order."""
    responses.add(
        responses.PUT,
        "{0}{1}".format(pyjmproapi.root, pyjmproapi._routes["gtt.modify"].format(trigger_id=123)),
        body=utils.get_response("gtt.modify"),
        content_type="application/json"
    )
    gtts = pyjmproapi.modify_gtt(
        trigger_id=123,
        trigger_type=pyjmproapi.GTT_TYPE_SINGLE,
        tradingsymbol="INFY",
        exchange="NSE",
        trigger_values=[1],
        last_price=800,
        orders=[{
            "transaction_type": pyjmproapi.TRANSACTION_TYPE_BUY,
            "quantity": 1,
            "order_type": pyjmproapi.ORDER_TYPE_LIMIT,
            "product": pyjmproapi.PRODUCT_CNC,
            "price": 1,
        }]
    )
    assert gtts["trigger_id"] == 123


@responses.activate
def test_delete_gtt(pyjmproapi):
    """Test delete gtt order."""
    responses.add(
        responses.DELETE,
        "{0}{1}".format(pyjmproapi.root, pyjmproapi._routes["gtt.delete"].format(trigger_id=123)),
        body=utils.get_response("gtt.delete"),
        content_type="application/json"
    )
    gtts = pyjmproapi.delete_gtt(123)
    assert gtts["trigger_id"] == 123


@responses.activate
def test_order_margins(pyjmproapi):
    """ Test order margins and charges """
    responses.add(
        responses.POST,
        "{0}{1}".format(pyjmproapi.root, pyjmproapi._routes["order.margins"]),
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

    margin_detail = pyjmproapi.order_margins(order_param_single)
    assert margin_detail[0]['type'] == "equity"
    assert margin_detail[0]['total'] != 0
    assert margin_detail[0]['charges']['transaction_tax'] != 0
    assert margin_detail[0]['charges']['gst']['total'] != 0


@responses.activate
def test_basket_order_margins(pyjmproapi):
    """ Test basket order margins and charges """
    responses.add(
        responses.POST,
        "{0}{1}".format(pyjmproapi.root, pyjmproapi._routes["order.margins.basket"]),
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

    margin_detail = pyjmproapi.basket_order_margins(order_param_multi)
    assert margin_detail['orders'][0]['exposure'] != 0
    assert margin_detail['orders'][0]['type'] == "equity"
    assert margin_detail['orders'][0]['total'] != 0

@responses.activate
def test_virtual_contract_note(pyjmproapi):
    """ Test virtual contract note charges """
    responses.add(
        responses.POST,
        "{0}{1}".format(pyjmproapi.root, pyjmproapi._routes["order.contract_note"]),
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

    order_book_charges = pyjmproapi.get_virtual_contract_note(order_book_params)
    assert order_book_charges[0]['charges']['transaction_tax_type'] == "stt"
    assert order_book_charges[0]['charges']['total'] != 0
    assert order_book_charges[1]['charges']['transaction_tax_type'] == "ctt"
    assert order_book_charges[1]['charges']['total'] != 0
