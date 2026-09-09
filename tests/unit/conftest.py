# coding: utf-8

"""Pytest config."""
import os
import sys
import pytest
from pyjmproapi import PyJmproAPI, JmproTicker

sys.path.append(os.path.join(os.path.dirname(__file__), '../helpers'))


@pytest.fixture()
def pyjmproapi():
    """Init Jmpro connect object."""
    jmpro = PyJmproAPI(api_key='<API-KEY>', access_token='<ACCESS-TOKEN>')
    jmpro.root = 'http://jmpro_api_test'
    return jmpro


@pytest.fixture()
def pyblinkxapi(pyjmproapi):
    """Alias fixture for backward compatibility."""
    return pyjmproapi


@pytest.fixture()
def pyjmproapi_with_pooling():
    """Init Jmpro connect object with pooling."""
    jmpro = PyJmproAPI(
        api_key="<API-KEY>",
        access_token="<ACCESS-TOKEN>",
        pool={
            "pool_connections": 20,
            "pool_maxsize": 10,
            "max_retries": 2,
            "pool_block": False
        }
    )
    return jmpro


@pytest.fixture()
def pyblinkxapi_with_pooling(pyjmproapi_with_pooling):
    """Alias fixture for backward compatibility."""
    return pyjmproapi_with_pooling


@pytest.fixture()
def jmproticker():
    """Init Jmpro ticker object."""
    kws = JmproTicker("<API-KEY>", "<PUB-TOKEN>", "<USER-ID>", debug=True, reconnect=False)
    kws.socket_url = "ws://127.0.0.1:9000?api_key=<API-KEY>?&user_id=<USER-ID>&public_token=<PUBLIC-TOKEN>"
    return kws


@pytest.fixture()
def blinkxticker(jmproticker):
    """Alias fixture for backward compatibility."""
    return jmproticker


@pytest.fixture()
def protocol():
    from autobahn.test import FakeTransport
    from pyjmproapi.ticker import JmproTickerClientProtocol,\
        JmproTickerClientFactory

    t = FakeTransport()
    f = JmproTickerClientFactory()
    p = JmproTickerClientProtocol()
    p.factory = f
    p.transport = t

    p._connectionMade()
    p.state = p.STATE_OPEN
    p.websocket_version = 18
    return p
