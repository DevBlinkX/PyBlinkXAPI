# coding: utf-8
import pytest
from mock import patch
import responses
import requests

from blinkxconnect import BlinkXConnect
import blinkxconnect.exceptions as ex


def get_fake_token(self, route, params=None):
    return {
        "access_token": "TOKEN",
        "login_time": None
    }


def get_fake_delete(self, route, params=None):
    return {"message": "token invalidated"}


class TestBlinkXConnectObject:

    def test_login_url(self, blinkxconnect):
        assert blinkxconnect.login_url() == "https://login.blinkx.in/connect/login?api_key=<API-KEY>&v=3"

    def test_request_without_pooling(self, blinkxconnect):
        assert isinstance(blinkxconnect.reqsession, requests.Session) is True
        assert blinkxconnect.reqsession.request is not None

    def test_request_pooling(self, blinkxconnect_with_pooling):
        assert isinstance(blinkxconnect_with_pooling.reqsession, requests.Session) is True
        assert blinkxconnect_with_pooling.reqsession.request is not None
        http_adapter = blinkxconnect_with_pooling.reqsession.adapters['https://']
        assert http_adapter._pool_maxsize == 10
        assert http_adapter._pool_connections == 20
        assert http_adapter._pool_block is False
        assert http_adapter.max_retries.total == 2

    @responses.activate
    def test_set_session_expiry_hook_meth(self, blinkxconnect):

        def mock_hook():
            raise ex.TokenException("token expired it seems! please login again")

        blinkxconnect.set_session_expiry_hook(mock_hook)

        # Now lets try raising TokenException
        responses.add(
            responses.GET,
            "{0}{1}".format(blinkxconnect.root, blinkxconnect._routes["portfolio.positions"]),
            body='{"error_type": "TokenException", "message": "Please login again"}',
            content_type="application/json",
            status=403
        )
        with pytest.raises(ex.TokenException) as exc:
            blinkxconnect.positions()
            assert exc.message == "token expired it seems! please login again"

    def test_set_access_token_meth(self, blinkxconnect):
        assert blinkxconnect.access_token == "<ACCESS-TOKEN>"
        # Modify the access token now
        blinkxconnect.set_access_token("<MY-ACCESS-TOKEN>")
        assert blinkxconnect.access_token == "<MY-ACCESS-TOKEN>"
        # Change it back
        blinkxconnect.set_access_token("<ACCESS-TOKEN>")

    @patch.object(BlinkXConnect, "_post", get_fake_token)
    def test_generate_session(self, blinkxconnect):
        resp = blinkxconnect.generate_session(
            request_token="<REQUEST-TOKEN>",
            api_secret="<API-SECRET>"
        )
        assert resp["access_token"] == "TOKEN"
        assert blinkxconnect.access_token == "TOKEN"

        # Change it back
        blinkxconnect.set_access_token("<ACCESS-TOKEN>")

    @patch.object(BlinkXConnect, "_delete", get_fake_delete)
    def test_invalidate_token(self, blinkxconnect):
        resp = blinkxconnect.invalidate_access_token(access_token="<ACCESS-TOKEN>")
        assert resp["message"] == "token invalidated"
