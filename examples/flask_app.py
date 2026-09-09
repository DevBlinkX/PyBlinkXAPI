###############################################################################
#
# The MIT License (MIT)
#
# Copyright (c) JMPRO / JM Financial (India)
#
# This is simple Flask based webapp to generate access token and get basic
# account info like holdings and order.
#
# To run this you need JMPRO Trading API python client and Flask webserver
#
#   pip install Flask
#   pip install pyjmproapi
#
#   python examples/flask_app.py
###############################################################################
import os
import json
import logging
from datetime import date, datetime
from decimal import Decimal

from flask import Flask, request, jsonify, session
from pyjmproapi import PyJmproAPI

logging.basicConfig(level=logging.DEBUG)

# Base settings
PORT = 5010
HOST = "127.0.0.1"


def serializer(obj): return isinstance(obj, (date, datetime, Decimal)) and str(obj)  # noqa


# JMPRO Connect App settings. Go to https://api.jmpro.in
# to create an app if you don't have one.
jmpro_api_key = "jmpro_api_key"
jmpro_api_secret = "jmpro_api_secret"

# Create a redirect url
redirect_url = "http://{host}:{port}/login".format(host=HOST, port=PORT)

# Login url
login_url = "https://login.jmpro.in/connect/login?api_key={api_key}".format(api_key=jmpro_api_key)

# Jmpro connect console url
console_url = "https://api.jmpro.in/apps/{api_key}".format(api_key=jmpro_api_key)

# App
app = Flask(__name__)
app.secret_key = os.urandom(24)

# Templates
index_template = """
    <div>Make sure your app with api_key - <b>{api_key}</b> has set redirect to <b>{redirect_url}</b>.</div>
    <div>If not you can set it from your <a href="{console_url}">JMPRO Trading API developer console here</a>.</div>
    <a href="{login_url}"><h1>Login to generate access token.</h1></a>"""

login_template = """
    <h2 style="color: green">Success</h2>
    <div>Access token: <b>{access_token}</b></div>
    <h4>User login data</h4>
    <pre>{user_data}</pre>
    <a target="_blank" href="/holdings.json"><h4>Fetch user holdings</h4></a>
    <a target="_blank" href="/orders.json"><h4>Fetch user orders</h4></a>
    <a target="_blank" href="https://api.jmpro.in/docs"><h4>Check JMPRO Trading API docs for other calls.</h4></a>"""


def get_jmpro_client():
    """Returns a Jmpro client object
    """
    jmpro = PyJmproAPI(api_key=jmpro_api_key)
    if "access_token" in session:
        jmpro.set_access_token(session["access_token"])
    return jmpro


@app.route("/")
def index():
    return index_template.format(
        api_key=jmpro_api_key,
        redirect_url=redirect_url,
        console_url=console_url,
        login_url=login_url
    )


@app.route("/login")
def login():
    request_token = request.args.get("request_token")

    if not request_token:
        return """
            <span style="color: red">
                Error while generating request token.
            </span>
            <a href='/'>Try again.<a>"""

    jmpro = get_jmpro_client()
    data = jmpro.generate_session(request_token, api_secret=jmpro_api_secret)
    session["access_token"] = data["access_token"]

    return login_template.format(
        access_token=data["access_token"],
        user_data=json.dumps(
            data,
            indent=4,
            sort_keys=True,
            default=serializer
        )
    )


@app.route("/holdings.json")
def holdings():
    jmpro = get_jmpro_client()
    return jsonify(holdings=jmpro.holdings())


@app.route("/orders.json")
def orders():
    jmpro = get_jmpro_client()
    return jsonify(orders=jmpro.orders())


if __name__ == "__main__":
    logging.info("Starting server: http://{host}:{port}".format(host=HOST, port=PORT))
    app.run(host=HOST, port=PORT, debug=True)
