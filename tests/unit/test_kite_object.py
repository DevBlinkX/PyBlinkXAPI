# coding: utf-8
import pytest
from mock import patch
import responses
import requests

from pyblinkxapi import PyBlinkXAPI
import pyblinkxapi.exceptions as ex


def get_fake_token(self, route, params=None):
    return {
        "access_token": "TOKEN",
        "login_time": None
    }


def get_fake_delete(self, route, params=None):
    return {"message": "token invalidated"}


class TestPyBlinkXAPIObject:

    def test_login_url(self, pyblinkxapi):
        assert pyblinkxapi.login_url() == "https://login.blinkx.in/connect/login?api_key=<API-KEY>&v=3"

    def test_request_without_pooling(self, pyblinkxapi):
        assert isinstance(pyblinkxapi.reqsession, requests.Session) is True
        assert pyblinkxapi.reqsession.request is not None

    def test_request_pooling(self, pyblinkxapi_with_pooling):
        assert isinstance(pyblinkxapi_with_pooling.reqsession, requests.Session) is True
        assert pyblinkxapi_with_pooling.reqsession.request is not None
        http_adapter = pyblinkxapi_with_pooling.reqsession.adapters['https://']
        assert http_adapter._pool_maxsize == 10
        assert http_adapter._pool_connections == 20
        assert http_adapter._pool_block is False
        assert http_adapter.max_retries.total == 2

    @responses.activate
    def test_set_session_expiry_hook_meth(self, pyblinkxapi):

        def mock_hook():
            raise ex.TokenException("token expired it seems! please login again")

        pyblinkxapi.set_session_expiry_hook(mock_hook)

        # Now lets try raising TokenException
        responses.add(
            responses.GET,
            "{0}{1}".format(pyblinkxapi.root, pyblinkxapi._routes["portfolio.positions"]),
            body='{"error_type": "TokenException", "message": "Please login again"}',
            content_type="application/json",
            status=403
        )
        with pytest.raises(ex.TokenException) as exc:
            pyblinkxapi.positions()
            assert exc.message == "token expired it seems! please login again"

    def test_set_access_token_meth(self, pyblinkxapi):
        assert pyblinkxapi.access_token == "<ACCESS-TOKEN>"
        # Modify the access token now
        pyblinkxapi.set_access_token("<MY-ACCESS-TOKEN>")
        assert pyblinkxapi.access_token == "<MY-ACCESS-TOKEN>"
        # Change it back
        pyblinkxapi.set_access_token("<ACCESS-TOKEN>")

    @patch.object(PyBlinkXAPI, "_post", get_fake_token)
    def test_generate_session(self, pyblinkxapi):
        resp = pyblinkxapi.generate_session(
            request_token="<REQUEST-TOKEN>",
            api_secret="<API-SECRET>"
        )
        assert resp["access_token"] == "TOKEN"
        assert pyblinkxapi.access_token == "TOKEN"

        # Change it back
        pyblinkxapi.set_access_token("<ACCESS-TOKEN>")

    @patch.object(PyBlinkXAPI, "_delete", get_fake_delete)
    def test_invalidate_token(self, pyblinkxapi):
        resp = pyblinkxapi.invalidate_access_token(access_token="<ACCESS-TOKEN>")
        assert resp["message"] == "token invalidated"
