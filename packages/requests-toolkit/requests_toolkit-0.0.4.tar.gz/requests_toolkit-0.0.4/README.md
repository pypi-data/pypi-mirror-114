<h1>The Requests-Toolkit</h1>
<p>A collection of decorators and other tools for handling
common patterns when working with the python requests package.
</p>

## Installation
```bash
$ pip install requests_toolkit
```

## Developers
To run tests you must install the extra dev tools
from setup.py
```bash
$ pip install -e .[dev]
```

To run tests
```bash
$ python -m pytest
```

## Usage
All decorators will return a requests.Response object.</br></br>
Example usage:</br></br>
<b>validate_keys:</b> expected data must specify the required keys and structure.
    suppress_exception_for_extra_found_keys has default value True, which means that
    the response can contain extra keys not expected without throwing exception.
    But an exception will always be thrown for missing expected keys.</br></br>
<b>handle_http_error:</b> returns requests.Response except when throw_exception=True a requests.HTTPError
```python
from requests_toolkit.json_tools import (handle_http_error, validate_keys)
import requests

@handle_http_error(throw_exception=True)
@validate_keys(expected_data={"key1": "", "key2": [{"key3": ""}]}, suppress_exception_for_extra_found_keys=False)
def make_http_request():
    return requests.get(url="https://myurl.com/api/json")
```
