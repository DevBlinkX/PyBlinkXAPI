import logging
from pyjmproapi import PyJmproAPI

logging.basicConfig(level=logging.DEBUG)

jmpro = PyJmproAPI(api_key="API KEY")

# Redirect the user to the login url obtained
# from jmpro.login_url(), and receive the request_token
# from the registered redirect url after the login flow.
# Once you have the request_token, obtain the access_token
# as follows.

# data = jmpro.generate_session("API KEY", api_secret="API Secret")
# jmpro.set_access_token(data["access_token"])
# print("Access Token : "+data["access_token"])

# jmpro.set_access_token("API KEY")

print(jmpro.login_url())
# Place an order
try:

    with open("output.txt", "w") as f:
        # print("Profile:   ",file=f)
        # print(jmpro.profile(),file=f)

        # print("Margins:   ",file=f)
        # print(jmpro.margins(),file=f)

        print(jmpro.place_order(variety=jmpro.VARIETY_REGULAR,
        exchange=jmpro.EXCHANGE_BSE,
        tradingsymbol="RELIANCE",
        transaction_type=jmpro.TRANSACTION_TYPE_BUY,
        quantity=1,
        product=jmpro.PRODUCT_CNC,
        price=3000,
        order_type=jmpro.ORDER_TYPE_MARKET,validity=jmpro.VALIDITY_DAY),file=f)

        # print("Modify Order",file=f)
        # print(jmpro.modify_order(variety=jmpro.VARIETY_REGULAR,order_id="251103000000062",order_type=jmpro.ORDER_TYPE_LIMIT,quantity=20,validity=jmpro.VALIDITY_DAY), file=f)

        # print("Cancel Order: %s",jmpro.cancel_order(jmpro.VARIETY_REGULAR,"251103000000062"))

        print("Order:   ",file=f)
        print(jmpro.orders(), file=f)

    #     print("Get order by id:",file=f)
    #     print(jmpro.order_history("251103000000062"),file=f)

        # print("Trade", file=f)
        # print(jmpro.trades(),file=f)

    #     print("Holdings",file=f)
    #     print(jmpro.holdings(),file=f)

    #     print("Position",file=f)
    #     print(jmpro.positions(),file=f)

    #     print("Modify Position",file=f) #Not available
    #     print(jmpro.convert_position(),file=f)

    #     print("Instruments:   ",file=f)
        # print(jmpro.instruments(),file=f)

        # print("Instruments with exchange:   ",file=f)
        # print(jmpro.instruments(exchange="NSE"),file=f)




except Exception as e:
    logging.info("Order placement failed: {}".format(e))

# Fetch all orders
# jmpro.orders()

# Get instruments
# jmpro.instruments()

# Fetch option chain
# jmpro.option_chain(
#     exchange="NFO",
#     underlying="NIFTY",
#     expiry="2026-02-26"
# )

# Fetch option chain expiry dates
# jmpro.option_chain_expiry(
#     exchange="NFO",
#     underlying="NIFTY"
# )
