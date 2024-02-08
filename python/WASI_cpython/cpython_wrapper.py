import os
import sys
from pathlib import Path

import wasmtime
from wasmtime import Config, Engine, Linker, Module, Store, WasiConfig


HERE = Path(__file__).parent
CPYTHON_WASM = HERE.joinpath("python.wasm")

GUEST_PREFIX = Path("/opt", "CPython-WASI")

# NOTE:User is required to provide a CPython stdlib, the pure-Python stuff in the repo is sufficient
try:
    CPYTHON_STDLIB_HOST = Path(os.environ["CPYTHON_STDLIB"])
except LookupError:
    raise ValueError("Define the CPYTHON_STDLIB environment variable with the path to the CPython standard library") from None
CPYTHON_STDLIB_GUEST = Path(GUEST_PREFIX, "wasm-site-packages")

SYSCONFIGDATA_HOST = HERE.joinpath("lib.wasi-wasm32-3.13")
SYSCONFIGDATA_GUEST = Path(GUEST_PREFIX, "sysconfigdata")

GUEST_PYTHONPATH = ":".join([str(CPYTHON_STDLIB_GUEST), str(SYSCONFIGDATA_GUEST)])

# "Fuel" is `wasmtime` jargon for a resource that is consumed by the execution of
# WASM instructions, approximately 1 fuel per instruction. It has appreciable
# overhead, but it is a pretty reliable mechanism for placing a limit on the
# amount of execution done in the guest
# https://docs.wasmtime.dev/api/wasmtime/struct.Store.html#method.set_fuel
INITIAL_FUEL = int(os.environ.get("INITIAL_FUEL", 1_000_000_000))


def _initialize_wasm(*argv, initial_fuel: int = 0):
    consume_fuel = initial_fuel > 0

    wasm_cfg = Config()
    # This example will work without enabling the cache, but the startup time
    # will be substantial, from 2-12 seconds to print the version in my testing
    wasm_cfg.cache = True
    wasm_cfg.wasm_threads = True
    wasm_cfg.consume_fuel = consume_fuel

    wasi_cfg = WasiConfig()
    wasi_cfg.inherit_stdin()
    wasi_cfg.inherit_stdout()
    wasi_cfg.inherit_stderr()
    wasi_cfg.preopen_dir(str(CPYTHON_STDLIB_HOST), str(CPYTHON_STDLIB_GUEST))
    wasi_cfg.preopen_dir(str(SYSCONFIGDATA_HOST), str(SYSCONFIGDATA_GUEST))
    wasi_cfg.env = [
        ("PYTHONPATH", GUEST_PYTHONPATH),
    ]
    wasi_cfg.argv = (str(GUEST_PREFIX.joinpath("python.wasm")), *argv)

    engine = Engine(wasm_cfg)

    linker = Linker(engine)
    linker.define_wasi()

    store = Store(engine)
    store.set_wasi(wasi_cfg)
    if consume_fuel:
        store.set_fuel(initial_fuel)

    module = Module.from_file(engine, str(CPYTHON_WASM))

    instance = linker.instantiate(store, module)

    return instance, store


def report_fuel(store: Store, initial_fuel: int):
    if initial_fuel > 0:
        remaining = store.get_fuel()
        consumed = initial_fuel - remaining
        print(f"Fuel remaining: {remaining}", file=sys.stderr)
        print(f"Initial fuel was {INITIAL_FUEL}", file=sys.stderr)
        print(f"Consumed {100*consumed/INITIAL_FUEL:.1f}% of available fuel")


def main():
    initial_fuel = INITIAL_FUEL

    try:
        instance, store = _initialize_wasm(*sys.argv[1:], initial_fuel=INITIAL_FUEL)
        instance.exports(store)["_start"](store)
        if initial_fuel > 0:
            report_fuel(store, initial_fuel=initial_fuel)
    except wasmtime.Trap as exc:
        msg = exc.message.splitlines()[-1].strip()
        print(f"wasmtime instance terminated with WASM trap: {msg!r}")
        if initial_fuel > 0:
            report_fuel(store, initial_fuel=initial_fuel)
        sys.exit(2)
    except Exception as exc:
        print(f"wasmtime instance terminated with an exception: {exc!r}")
        sys.exit(1)


if __name__ == "__main__":
    main()
