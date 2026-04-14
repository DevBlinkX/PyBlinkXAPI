# coding: utf-8

"""Pytest config."""
import os
import sys
import pytest
from pyblinkxapi import PyBlinkXAPI, BlinkXTicker

sys.path.append(os.path.join(os.path.dirname(__file__), '../helpers'))


@pytest.fixture()
def pyblinkxapi():
    """Init BlinkX connect object."""
    blinkx = PyBlinkXAPI(api_key='<API-KEY>', access_token='<ACCESS-TOKEN>')
    blinkx.root = 'http://blinkx_api_test'
    return blinkx


@pytest.fixture()
def pyblinkxapi_with_pooling():
    """Init BlinkX connect object with pooling."""
    blinkx = PyBlinkXAPI(
        api_key="<API-KEY>",
        access_token="<ACCESS-TOKEN>",
        pool={
            "pool_connections": 20,
            "pool_maxsize": 10,
            "max_retries": 2,
            "pool_block": False
        }
    )
    return blinkx


@pytest.fixture()
def blinkxticker():
    """Init BlinkX ticker object."""
    kws = BlinkXTicker("<API-KEY>", "<PUB-TOKEN>", "<USER-ID>", debug=True, reconnect=False)
    kws.socket_url = "ws://127.0.0.1:9000?api_key=<API-KEY>?&user_id=<USER-ID>&public_token=<PUBLIC-TOKEN>"
    return kws


@pytest.fixture()
def protocol():
    from autobahn.test import FakeTransport
    from pyblinkxapi.ticker import BlinkXTickerClientProtocol,\
        BlinkXTickerClientFactory

    t = FakeTransport()
    f = BlinkXTickerClientFactory()
    p = BlinkXTickerClientProtocol()
    p.factory = f
    p.transport = t

    p._connectionMade()
    p.state = p.STATE_OPEN
    p.websocket_version = 18
    return p
