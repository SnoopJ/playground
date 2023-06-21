This example shows off how to use ASGI middleware to handle exceptions that
occur while serving an application route, in a way that is aware of the
particular route that caused the exception. In this case, the handling is
limited to mapping the exception to an error code and recording the route that
caused the exception, but in more complex applications, the handling can adapt
to the particular route or `response_model` associated with the exception.


### Sample output

```
$ python3 -m uvicorn app:app
INFO:     Started server process [3713884]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
Using response class AnvilResponse for error response
INFO:     127.0.0.1:47664 - "POST /anvil HTTP/1.1" 500 Internal Server Error
Using response class TNTResponse for error response
INFO:     127.0.0.1:47666 - "POST /tnt HTTP/1.1" 500 Internal Server Error
Using response class AnvilResponse for error response
INFO:     127.0.0.1:47668 - "POST /anvil HTTP/1.1" 500 Internal Server Error
Using response class TNTResponse for error response
INFO:     127.0.0.1:47670 - "POST /tnt HTTP/1.1" 500 Internal Server Error
Using response class AnvilResponse for error response
INFO:     127.0.0.1:47672 - "POST /anvil HTTP/1.1" 500 Internal Server Error
Using response class TNTResponse for error response
INFO:     127.0.0.1:47674 - "POST /tnt HTTP/1.1" 500 Internal Server Error
INFO:     127.0.0.1:47676 - "POST /anvil HTTP/1.1" 200 OK
INFO:     127.0.0.1:47678 - "POST /tnt HTTP/1.1" 200 OK
```

```
$ python3 client.py
anvil response: HTTP 500 {'sfx': 'BONK!', 'flattened': True, 'exploded': False, 'error_info': {'error_code': 'ACME_EXCEPTION', 'route': '/anvil'}}
TNT response:   HTTP 500 {'sfx': 'KABOOM!', 'flattened': False, 'exploded': True, 'error_info': {'error_code': 'ACME_EXCEPTION', 'route': '/tnt'}}
---

anvil response: HTTP 500 {'sfx': 'BONK!', 'flattened': True, 'exploded': False, 'error_info': {'error_code': 'ANVIL_ERROR', 'route': '/anvil'}}
TNT response:   HTTP 500 {'sfx': 'KABOOM!', 'flattened': False, 'exploded': True, 'error_info': {'error_code': 'TNT_ERROR', 'route': '/tnt'}}
---

anvil response: HTTP 500 {'sfx': 'BONK!', 'flattened': True, 'exploded': False, 'error_info': {'error_code': 'GENERAL_ERROR', 'route': '/anvil'}}
TNT response:   HTTP 500 {'sfx': 'KABOOM!', 'flattened': False, 'exploded': True, 'error_info': {'error_code': 'GENERAL_ERROR', 'route': '/tnt'}}
---

anvil response: HTTP 200 {'sfx': 'BANG!', 'flattened': True, 'exploded': False, 'error_info': None}
TNT response:   HTTP 200 {'sfx': 'KABLOOEY!', 'flattened': False, 'exploded': True, 'error_info': None}
---

```
