import unittest
from unittest.mock import *
import pytest
import requests


from requests_toolkit import (validate_keys, handle_http_error, ExpectedKeyError)
import requests_toolkit


class TestToolkit(unittest.TestCase):
    class MockRequestsResponse:
        def __init__(self, status_code: int, data: list or dict):
            self.status_code = status_code
            self.data = data
            if self.status_code in (200, 300):
                self.ok = True
            elif self.status_code in (400, 500):
                self.ok = False

        def json(self):
            return self.data

    def test_handle_http_error_200_response(self):
        @handle_http_error
        def make_request():
            response = requests.Response()
            response.status_code = 200
            return response
        assert isinstance(make_request(), type(requests.Response()))

    def test_handle_http_error_400_response_raises_exception(self):
        @handle_http_error
        def make_request():
            response = requests.Response()
            response.status_code = 400
            return response
        with pytest.raises(Exception):
            make_request()

    def test_validate_keys_match_returns_response(self):
        @validate_keys(expected_keys=["key1", "key2"])
        def make_request():
            return TestToolkit.MockRequestsResponse(status_code=200, data=[{"key1": "data1", "key2": "data2"}])
        make_request()

    def test_validate_keys_missing_key_raises_exception(self):
        @validate_keys(expected_keys=["key1", "key2"])
        def make_request():
            return TestToolkit.MockRequestsResponse(status_code=200, data=[{"key1": "data1"}])
        with pytest.raises(ExpectedKeyError):
            make_request()

    def test_validate_keys_extra_found_key_raises_exception(self):
        @validate_keys(expected_keys=["key1", "key2"], suppress_exception_for_extra_found_keys=False)
        def make_request():
            return TestToolkit.MockRequestsResponse(status_code=200, data=[{"key1": "data1", "key2": "data2", "key3": "data3"}])
        with pytest.raises(ExpectedKeyError):
            make_request()

    def test_validate_keys_extra_found_key_exception_suppressed(self):
        @validate_keys(expected_keys=["key1", "key2"])
        def make_request():
            return TestToolkit.MockRequestsResponse(status_code=200, data=[{"key1": "data1", "key2": "data2", "key3": "data3"}])
        make_request()

    def test_validate_keys_no_keys_raises_exception(self):
        @validate_keys(expected_keys=["key1", "key2"])
        def make_request():
            return TestToolkit.MockRequestsResponse(status_code=200, data=[{}])
        with pytest.raises(ExpectedKeyError):
            make_request()
