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

# Place single-leg gtt order
try:
    order_single = [{
        "exchange":"NSE",
        "tradingsymbol": "SBIN",
        "transaction_type": jmpro.TRANSACTION_TYPE_BUY,
        "quantity": 1,
        "order_type": "LIMIT",
        "product": "CNC",
        "price": 470,
    }]
    single_gtt = jmpro.place_gtt(trigger_type=jmpro.GTT_TYPE_SINGLE, tradingsymbol="SBIN", exchange="NSE", trigger_values=[470], last_price=473, orders=order_single)
    logging.info("single leg gtt order trigger_id : {}".format(single_gtt['trigger_id']))
except Exception as e:
    logging.info("Error placing single leg gtt order: {}".format(e))


# Place two-leg(OCO) gtt order
try:
    order_oco = [{
        "exchange":"NSE",
        "tradingsymbol": "SBIN",
        "transaction_type": jmpro.TRANSACTION_TYPE_SELL,
        "quantity": 1,
        "order_type": "LIMIT",
        "product": "CNC",
        "price": 470
        },{
        "exchange":"NSE",
        "tradingsymbol": "SBIN",
        "transaction_type": jmpro.TRANSACTION_TYPE_SELL,
        "quantity": 1,
        "order_type": "LIMIT",
        "product": "CNC",
        "price": 480
    }]
    gtt_oco = jmpro.place_gtt(trigger_type=jmpro.GTT_TYPE_OCO, tradingsymbol="SBIN", exchange="NSE", trigger_values=[470,480], last_price=473, orders=order_oco)
    logging.info("GTT OCO trigger_id : {}".format(gtt_oco['trigger_id']))
except Exception as e:
    logging.info("Error placing gtt oco order: {}".format(e))
