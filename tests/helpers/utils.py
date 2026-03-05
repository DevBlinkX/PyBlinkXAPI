# coding: utf-8
import os
import json

# Mock responses path
responses_path = {
    "base": "../mock_responses/",
    "user.profile": "profile.json",
    "user.margins": "margins.json",

    "orders": "orders.json",
    "trades": "trades.json",
    "order.info": "order_info.json",
    "order.trades": "order_trades.json",

    "portfolio.positions": "positions.json",
    "portfolio.holdings": "holdings.json",
    "portfolio.holdings.auction": "auctions_list.json",

    "market.instruments": "instruments_nse.csv",
    "market.instruments.all": "instruments_all.csv",
    "market.historical": "historical_minute.json",

    "market.quote": "quote.json",
    "market.quote.ohlc": "ohlc.json",
    "market.quote.ltp": "ltp.json",

    "gtt": "gtt_get_orders.json",
    "gtt.place": "gtt_place_order.json",
    "gtt.info": "gtt_get_order.json",
    "gtt.modify": "gtt_modify_order.json",
    "gtt.delete": "gtt_delete_order.json",

    # Order margin & charges
    "order.margins": "order_margins.json",
    "order.margins.basket": "basket_margins.json",
    "order.contract_note": "virtual_contract_note.json"
}


def full_path(rel_path):
    """return the full path of given rel_path."""
    return os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            rel_path
        )
    )


def get_response(key):
    """Get mock response based on route."""
    path = full_path(responses_path["base"] + responses_path[key])
    return open(path, "r").read()


def get_json_response(key):
    """Get json mock response based on route."""
    return json.loads(get_response(key))


def assert_responses(inp, sample):
    """Check if all keys given as a list is there in input."""
    if type(sample) in [list, dict]:
        assert type(inp) == type(sample)

    if type(inp) == list and len(inp) > 0:
        assert_responses(inp[0], sample[0])

    if type(sample) == dict:
        for key in sample.keys():
            assert_responses(inp[key], sample[key])


def merge_dicts(x, y):
    z = x.copy()
    z.update(y)
    return z
