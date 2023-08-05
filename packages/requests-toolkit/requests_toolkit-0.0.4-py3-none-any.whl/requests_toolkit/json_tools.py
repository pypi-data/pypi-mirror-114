import requests
from functools import wraps


class ExpectedKeyError(Exception):
    """
    Exception Class for dictionary keys that do not match what is expected from
    a requests.Response object that can be converted to requests_toolkit using .requests_toolkit().
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

def traverse_json(response_data: list or dict, expected_data: list or dict, suppress_exception_for_extra_found_keys: bool):
    if isinstance(expected_data, list):
        for index, element in enumerate(expected_data):
            if isinstance(element, dict):
                found_keys = response_data[index].keys()
                expected_keys = element.keys()
                if set(expected_keys) - found_keys:
                    raise ExpectedKeyError(found_keys=found_keys, expected_keys=expected_keys)
                if found_keys - set(expected_keys) and not suppress_exception_for_extra_found_keys:
                    raise ExpectedKeyError(found_keys=found_keys, expected_keys=expected_keys)
                return traverse_json(
                    response_data=response_data[index],
                    expected_data=expected_data[index],
                    suppress_exception_for_extra_found_keys=suppress_exception_for_extra_found_keys
                )
            else:
                return True
    elif isinstance(expected_data, dict):
        found_keys = response_data.keys()
        expected_keys = expected_data.keys()
        if set(expected_keys) - found_keys:
            raise ExpectedKeyError(found_keys=found_keys, expected_keys=expected_keys)
        for key in expected_keys:
            return traverse_json(
                response_data=response_data[key],
                expected_data=expected_data[key],
                suppress_exception_for_extra_found_keys=suppress_exception_for_extra_found_keys
            )
    return True



def validate_keys(expected_data: list or dict, suppress_exception_for_extra_found_keys: bool = True):
    """
    Decorator:
    Validates that keys found by calling .requests_toolkit() on a requests.response object match what is expected.
    ...
    Parameters:
        expected_keys: list of strings
        suppress_exception_for_extra_found_keys: bool -> setting False enforces exact match of found keys and expected keys.
    Returns:
        requests.Response object
    """
    def inner(func):
        @wraps(func)
        def wrapper():
            response = func()
            traverse_json(
                response_data=response.json(),
                expected_data=expected_data,
                suppress_exception_for_extra_found_keys=suppress_exception_for_extra_found_keys
            )
            return response
        return wrapper
    return inner


def handle_http_error(throw_exception: bool = True):
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
    def inner(func):
        @wraps(func)
        def wrapper():
            response = func()
            if not response.ok and throw_exception:
                response.raise_for_status()
            return response
        return wrapper
    return inner
