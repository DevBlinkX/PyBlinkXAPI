import logging
from blinkxconnect import BlinkXConnect

logging.basicConfig(level=logging.DEBUG)

blinkx = BlinkXConnect(api_key="JJjqBs1qlKwPS8cdIo8wABQdbRQw97ok")

# Redirect the user to the login url obtained
# from blinkx.login_url(), and receive the request_token
# from the registered redirect url after the login flow.
# Once you have the request_token, obtain the access_token
# as follows.

# data = blinkx.generate_session("XdIrK7ojY7YjOzsEcCkZ6MzvbZvxBbLe", api_secret="IQxVQT2XDOSvNQIgz1jTv7nFT2RWqpHf6XNruvLkPgjqaXZBRhe1xbK8v7227Pje")
# blinkx.set_access_token(data["access_token"])
# print("Access Token : "+data["access_token"])

# blinkx.set_access_token("dfTfFN1UQZxzS9HqRWmU1mmsADtSXu9P")

print(blinkx.login_url())
# Place an order
try:

    with open("output.txt", "w") as f:
        # print("Profile:   ",file=f)
        # print(blinkx.profile(),file=f)

        # print("Margins:   ",file=f)
        # print(blinkx.margins(),file=f)

        # print(blinkx.place_order(variety=blinkx.VARIETY_REGULAR,
        # exchange=blinkx.EXCHANGE_BSE,
        # tradingsymbol="RELIANCE",
        # transaction_type=blinkx.TRANSACTION_TYPE_BUY,
        # quantity=1,
        # product=blinkx.PRODUCT_CNC,
        # price=3000,
        # order_type=blinkx.ORDER_TYPE_MARKET,validity=blinkx.VALIDITY_DAY),file=f)

        # print("Modify Order",file=f)
        # print(blinkx.modify_order(variety=blinkx.VARIETY_REGULAR,order_id="251103000000062",order_type=blinkx.ORDER_TYPE_LIMIT,quantity=20,validity=blinkx.VALIDITY_DAY), file=f)

        # print("Cancel Order: %s",blinkx.cancel_order(blinkx.VARIETY_REGULAR,"251103000000062"))

        print("Order:   ",file=f)
        print(blinkx.orders(), file=f)

    #     print("Get order by id:",file=f)
    #     print(blinkx.order_history("251103000000062"),file=f)

        # print("Trade", file=f)
        # print(blinkx.trades(),file=f)

    #     print("Holdings",file=f)
    #     print(blinkx.holdings(),file=f)

    #     print("Position",file=f)
    #     print(blinkx.positions(),file=f)

    #     print("Modify Position",file=f) #Not available
    #     print(blinkx.convert_position(),file=f)

    #     print("Instruments:   ",file=f)
        # print(blinkx.instruments(),file=f)

        # print("Instruments with exchange:   ",file=f)
        # print(blinkx.instruments(exchange="NSE"),file=f)




except Exception as e:
    logging.info("Order placement failed: {}".format(e))

# Fetch all orders
# blinkx.orders()

# Get instruments
# blinkx.instruments()

# Fetch option chain
# blinkx.option_chain(
#     exchange="NFO",
#     underlying="NIFTY",
#     expiry="2026-02-26"
# )

# Fetch option chain expiry dates
# blinkx.option_chain_expiry(
#     exchange="NFO",
#     underlying="NIFTY"
# )
