from functools import partial

class Application:
    def __init__(self):
        self._registry = dict()

    def _do_register(self, func, key, metadata):
        self._registry[key] = { "func": func, "metadata": metadata }
        return func

    def register(self, key, metadata=None):
        if metadata is None:
            metadata = dict()

        if callable(key):  # user did @app.register
            func = key
            key = func.__name__
            return self._do_register(func, key, metadata)
        else:  # user did @app.register(key, [metadata])
            return partial(self._do_register, key=key, metadata=metadata)

app1 = Application()
app2 = Application()

def show_registries(*apps):
    for app in apps:
        print(f"{app._registry=}")

show_registries(app1, app2)

@app1.register
def f(x):
    return x**2

@app2.register
def g(x):
    return x + 1

@app1.register("foo", metadata={"message": "Beware the Jabberwock, my son"})
def h(x, y):
    return 2*(x + y)

@app2.register("foo")
def j(x, y):
    return 3*(x - y)

show_registries(app1, app2)
