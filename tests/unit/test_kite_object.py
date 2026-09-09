# coding: utf-8
import pytest
from mock import patch
import responses
import requests

from pyjmproapi import PyJmproAPI
import pyjmproapi.exceptions as ex


def get_fake_token(self, route, params=None):
    return {
        "access_token": "TOKEN",
        "login_time": None
    }


def get_fake_delete(self, route, params=None):
    return {"message": "token invalidated"}


class TestPyJmproAPIObject:

    def test_login_url(self, pyjmproapi):
        assert pyjmproapi.login_url() == "https://mobuadeh.jmpro.in/login/connect/login?api_key=<API-KEY>&v=3"

    def test_request_without_pooling(self, pyjmproapi):
        assert isinstance(pyjmproapi.reqsession, requests.Session) is True
        assert pyjmproapi.reqsession.request is not None

    def test_request_pooling(self, pyjmproapi_with_pooling):
        assert isinstance(pyjmproapi_with_pooling.reqsession, requests.Session) is True
        assert pyjmproapi_with_pooling.reqsession.request is not None
        http_adapter = pyjmproapi_with_pooling.reqsession.adapters['https://']
        assert http_adapter._pool_maxsize == 10
        assert http_adapter._pool_connections == 20
        assert http_adapter._pool_block is False
        assert http_adapter.max_retries.total == 2

    @responses.activate
    def test_set_session_expiry_hook_meth(self, pyjmproapi):

        def mock_hook():
            raise ex.TokenException("token expired it seems! please login again")

        pyjmproapi.set_session_expiry_hook(mock_hook)

        # Now lets try raising TokenException
        responses.add(
            responses.GET,
            "{0}{1}".format(pyjmproapi.root, pyjmproapi._routes["portfolio.positions"]),
            body='{"error_type": "TokenException", "message": "Please login again"}',
            content_type="application/json",
            status=403
        )
        with pytest.raises(ex.TokenException) as exc:
            pyjmproapi.positions()
            assert exc.message == "token expired it seems! please login again"

    def test_set_access_token_meth(self, pyjmproapi):
        assert pyjmproapi.access_token == "<ACCESS-TOKEN>"
        # Modify the access token now
        pyjmproapi.set_access_token("<MY-ACCESS-TOKEN>")
        assert pyjmproapi.access_token == "<MY-ACCESS-TOKEN>"
        # Change it back
        pyjmproapi.set_access_token("<ACCESS-TOKEN>")

    @patch.object(PyJmproAPI, "_post", get_fake_token)
    def test_generate_session(self, pyjmproapi):
        resp = pyjmproapi.generate_session(
            request_token="<REQUEST-TOKEN>",
            api_secret="<API-SECRET>"
        )
        assert resp["access_token"] == "TOKEN"
        assert pyjmproapi.access_token == "TOKEN"

        # Change it back
        pyjmproapi.set_access_token("<ACCESS-TOKEN>")

    @patch.object(PyJmproAPI, "_delete", get_fake_delete)
    def test_invalidate_token(self, pyjmproapi):
        resp = pyjmproapi.invalidate_access_token(access_token="<ACCESS-TOKEN>")
        assert resp["message"] == "token invalidated"
