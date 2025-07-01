An example showing off the use of a `logging.LoggerAdapter` to offer a way to delay the handling
of logging events

```
$ python3 -m app
2023-07-07 19:07:21,247 [INFO    ] [MainThread (140461611902784)] __init__.main(+L30 ): Hello after configuration
$ python3 -m app --delay
2023-07-07 19:07:23,633 [INFO    ] [MainThread (139859232663360)] __init__.main(+L30 ): This logger has no handlers at call time, but the message will be deferred until there are some
2023-07-07 19:07:23,634 [INFO    ] [MainThread (139859232663360)] __init__.main(+L30 ): Hello after configuration
```
