# The JMPRO Trading API Python client - v1

The official Python client library for the [JMPRO Trading API](https://api.jmpro.in) trading platform by JM Financial.

`pyjmproapi` provides a clean, Pythonic interface to interact with the JMPRO trading APIs. It covers REST-based order placement, portfolio and account management, market data retrieval, GTT (Good Till Triggered) orders, option chains, and real-time WebSocket streaming via the `JmproTicker` component.

## Installation

Install via pip:

```
pip install pyjmproapi
```

Or install from source:

```
python setup.py install
```

## Usage

```python
from pyjmproapi import PyJmproAPI

# Initialize the client
jmpro = PyJmproAPI(api_key="your_api_key")

# Generate a login URL for the user
print(jmpro.login_url())

# After the user logs in and you receive a request_token:
data = jmpro.generate_session(
    request_token="obtained_request_token",
    api_secret="your_api_secret"
)

# Set the access token
jmpro.set_access_token(data["access_token"])

# Fetch user profile
print(jmpro.profile())

# Place an order
order_id = jmpro.place_order(
    variety=jmpro.VARIETY_REGULAR,
    exchange=jmpro.EXCHANGE_NSE,
    tradingsymbol="INFY",
    transaction_type=jmpro.TRANSACTION_TYPE_BUY,
    quantity=1,
    product=jmpro.PRODUCT_CNC,
    order_type=jmpro.ORDER_TYPE_MARKET
)
print("Order placed:", order_id)

# Fetch positions and holdings
print(jmpro.positions())
print(jmpro.holdings())

# Get option chain data
options = jmpro.option_chain(
    exchange="NFO",
    underlying="NIFTY",
    expiry="2025-01-30"
)
print(options)
```

## WebSocket Streaming

```python
from pyjmproapi import JmproTicker

kws = JmproTicker("your_api_key", "public_token", "user_id")

def on_ticks(ws, ticks):
    print("Ticks:", ticks)

def on_connect(ws, response):
    ws.subscribe([256265, 264969])  # NIFTY 50, NIFTY BANK
    ws.set_mode(ws.MODE_FULL, [256265, 264969])

kws.on_ticks = on_ticks
kws.on_connect = on_connect
kws.connect()
```

## API Methods

### Session & Authentication

| Method | Description |
|--------|-------------|
| `login_url()` | Get the login URL for user authentication |
| `generate_session(request_token, api_secret)` | Generate user session with request token |
| `set_access_token(access_token)` | Set the access token manually |
| `invalidate_access_token(access_token)` | Invalidate/logout the current session |

### User

| Method | Description |
|--------|-------------|
| `profile()` | Get user profile details |
| `margins(segment=None)` | Get account margins |

### Orders

| Method | Description |
|--------|-------------|
| `place_order(variety, ...)` | Place a new order |
| `modify_order(variety, order_id, ...)` | Modify a pending order |
| `cancel_order(variety, order_id, ...)` | Cancel a pending order |
| `orders()` | Get list of all orders |
| `order_history(order_id)` | Get history of a specific order |
| `trades()` | Get list of all trades |
| `order_trades(order_id)` | Get trades for a specific order |

### Portfolio

| Method | Description |
|--------|-------------|
| `holdings()` | Get holdings |
| `positions()` | Get positions |
| `convert_position(...)` | Convert position product type |
| `get_auction_instruments()` | Get auction instrument list |

### Market Data

| Method | Description |
|--------|-------------|
| `instruments(exchange=None)` | Get tradable instruments list |
| `historical_data(instrument_token, from_date, to_date, interval, ...)` | Get historical OHLCV data |
| `quote(instruments)` | Get full quote for instruments |
| `ohlc(instruments)` | Get OHLC data for instruments |
| `ltp(instruments)` | Get last traded price |

### GTT (Good Till Triggered)

| Method | Description |
|--------|-------------|
| `get_gtts()` | Get list of all GTT triggers |
| `get_gtt(trigger_id)` | Get a specific GTT trigger |
| `place_gtt(...)` | Place a new GTT order |
| `modify_gtt(trigger_id, ...)` | Modify an existing GTT |
| `delete_gtt(trigger_id)` | Delete a GTT trigger |

### Option Chain (JMPRO-specific)

| Method | Description |
|--------|-------------|
| `option_chain(exchange, underlying, expiry, ...)` | Get option chain data |
| `option_chain_expiry(exchange, underlying)` | Get available expiry dates |

### Margins & Charges

| Method | Description |
|--------|-------------|
| `order_margins(params)` | Get order margin requirements |
| `basket_order_margins(params)` | Get basket order margins with benefit |
| `get_virtual_contract_note(params)` | Get virtual contract note charges |

### Reports (JMPRO-specific)

| Method | Description |
|--------|-------------|
| `ledger(from_date, to_date)` | Get ledger entries |
| `trade_history(from_date, to_date, page)` | Get historical trade data |

## Constants

The SDK provides named constants for commonly used values:

```python
# Exchanges
jmpro.EXCHANGE_NSE, jmpro.EXCHANGE_BSE, jmpro.EXCHANGE_NFO
jmpro.EXCHANGE_CDS, jmpro.EXCHANGE_BFO, jmpro.EXCHANGE_MCX, jmpro.EXCHANGE_BCD

# Products
jmpro.PRODUCT_MIS, jmpro.PRODUCT_CNC, jmpro.PRODUCT_NRML

# Order types
jmpro.ORDER_TYPE_MARKET, jmpro.ORDER_TYPE_LIMIT
jmpro.ORDER_TYPE_SLM, jmpro.ORDER_TYPE_SL

# Varieties
jmpro.VARIETY_REGULAR, jmpro.VARIETY_AMO, jmpro.VARIETY_CO, jmpro.VARIETY_ICEBERG

# Transaction types
jmpro.TRANSACTION_TYPE_BUY, jmpro.TRANSACTION_TYPE_SELL

# Validity
jmpro.VALIDITY_DAY, jmpro.VALIDITY_IOC, jmpro.VALIDITY_TTL

# GTT types
jmpro.GTT_TYPE_OCO, jmpro.GTT_TYPE_SINGLE
```

## Running Tests

```
pip install -r dev_requirements.txt
pytest tests/unit/
```

## Examples

See the `examples/` directory for complete working samples including:

- `simple.py` — Basic API usage (orders, positions, option chain)
- `flask_app.py` — Flask web app integration with OAuth login flow
- `gtt_order.py` — GTT order placement
- `order_margins.py` — Order margin calculations
- `ticker.py` — Real-time WebSocket streaming
- `threaded_ticker.py` — Background ticker with threading

## License

MIT License. See `LICENSE` for details.

## Links

- **JMPRO Trading API Documentation**: [https://api.jmpro.in/docs](https://api.jmpro.in/docs)
- **JM Financial Website**: [https://jmpro.in](https://jmpro.in)
