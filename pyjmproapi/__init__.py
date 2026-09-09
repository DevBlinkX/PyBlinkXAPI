# -*- coding: utf-8 -*-
"""
JMPRO Trading API client for Python -- [api.jmpro.in](https://api.jmpro.in).

JMPRO / JM Financial (c) 2026

License
-------
PyJmproAPI Python library is licensed under the MIT License

The library
-----------
JMPRO Trading API is a set of REST-like APIs that expose
many capabilities required to build a complete
investment and trading platform. Execute orders in
real time, manage user portfolio, stream live market
data (WebSockets), and more, with the simple HTTP API collection.

This module provides an easy to use abstraction over the HTTP APIs.
The HTTP calls have been converted to methods and their JSON responses
are returned as native Python structures, for example, dicts, lists, bools etc.
See the **[JMPRO Trading API documentation](https://api.jmpro.in/docs)**
for the complete list of APIs, supported parameters and values, and response formats.

Getting started
---------------
    #!python
    import logging
    from pyjmproapi import PyJmproAPI

    logging.basicConfig(level=logging.DEBUG)

    jmpro = PyJmproAPI(api_key="your_api_key")

    # Redirect the user to the login url obtained
    # from jmpro.login_url(), and receive the request_token
    # from the registered redirect url after the login flow.
    # Once you have the request_token, obtain the access_token
    # as follows.

    data = jmpro.generate_session("request_token_here", api_secret="your_secret")
    jmpro.set_access_token(data["access_token"])

    # Place an order
    try:
        order_id = jmpro.place_order(variety=jmpro.VARIETY_REGULAR,
                                     tradingsymbol="INFY",
                                     exchange=jmpro.EXCHANGE_NSE,
                                     transaction_type=jmpro.TRANSACTION_TYPE_BUY,
                                     quantity=1,
                                     order_type=jmpro.ORDER_TYPE_MARKET,
                                     product=jmpro.PRODUCT_CNC,
                                     validity=jmpro.VALIDITY_DAY)

        logging.info("Order placed. ID is: {}".format(order_id))
    except Exception as e:
        logging.info("Order placement failed: {}".format(e.message))

    # Fetch all orders
    jmpro.orders()

    # Get instruments
    jmpro.instruments()

    # Fetch option chain
    jmpro.option_chain(
        exchange="NFO",
        underlying="NIFTY",
        expiry="2026-03-26"
    )

A typical web application
-------------------------
In a typical web application where a new instance of
views, controllers etc. are created per incoming HTTP
request, you will need to initialise a new instance of
Jmpro client per request as well. This is because each
individual instance represents a single user that's
authenticated, unlike an **admin** API where you may
use one instance to manage many users.

Hence, in your web application, typically:

- You will initialise an instance of the Jmpro client
- Redirect the user to the `login_url()`
- At the redirect url endpoint, obtain the
`request_token` from the query parameters
- Initialise a new instance of Jmpro client,
use `generate_session()` to obtain the `access_token`
along with authenticated user data
- Store this response in a session and use the
stored `access_token` and initialise instances
of Jmpro client for subsequent API calls.

Exceptions
----------
JMPRO Trading API client saves you the hassle of detecting API errors
by looking at HTTP codes or JSON error responses. Instead,
it raises aptly named **[exceptions](exceptions.m.html)** that you can catch.
"""

from __future__ import unicode_literals, absolute_import

from pyjmproapi import exceptions
from pyjmproapi.connect import PyJmproAPI
from pyjmproapi.ticker import JmproTicker

__all__ = ["PyJmproAPI", "JmproTicker", "exceptions"]
