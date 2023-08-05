import requests
from functools import wraps


class ExpectedKeyError(Exception):
    """
    Exception Class for dictionary keys that do not match what is expected from
    a requests.Response object that can be converted to json using .json().
    ...
    Attributes:
        found_keys: dict
        expected_keys: dict
        message: str
    """
    def __init__(self, found_keys, expected_keys, message="The requests.Response did not have the expected dictionary keys."):
        self.found_keys = found_keys
        self.expected_keys = expected_keys
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'{self.message}\n -> expected: {self.expected_keys} \n -> found: {self.found_keys}'


def validate_keys(expected_keys: list, suppress_exception_for_extra_found_keys: bool = True):
    """
    Decorator:
    Validates that keys found by calling .json() on a requests.response object match what is expected.
    ...
    Parameters:
        expected_keys: list of strings
        suppress_exception_for_extra_found_keys: bool
    Returns:
        requests.Response object
    """
    def inner(func):
        @wraps(func)
        def wrapper():
            response = func()
            try:
                response_data = response.json()
            except ValueError("requests.response did not return data that can be converted to json."):
                raise
            if isinstance(response_data, list):
                for entry in response_data:
                    found_keys = entry.keys()

                    if set(expected_keys) - found_keys:
                        raise ExpectedKeyError(found_keys=found_keys, expected_keys=expected_keys)
                    if found_keys - set(expected_keys) and not suppress_exception_for_extra_found_keys:
                        raise ExpectedKeyError(found_keys=found_keys, expected_keys=expected_keys)

                return response
            elif isinstance(response_data, dict):
                found_keys = response_data.keys()
                if set(expected_keys) - found_keys:
                    raise ExpectedKeyError(found_keys=found_keys, expected_keys=expected_keys)
                return response
        return wrapper
    return inner


def handle_http_error(func):
    """
    Decorator:
    Abstracts away handling of bad HTTP-status-codes
    by raising requests.HTTPError for non-200/300 responses.
    ...
    Parameters:
        func: function that returns requests.Response objects
    Returns:
        requests.Response object
    """
    @wraps(func)
    def wrapper():
        response = func()
        if response.ok:
            return response
        response.raise_for_status()
    return wrapper

