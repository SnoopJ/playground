# Running the WASI build of CPython from Python

This sample demonstrates how to run the WASI build of CPython in the `wasmtime`
runtime using the Python API instead of the commandline.

The use-case that inspired me to write it is the desire to operate a chat-bot
with the ability to evaluate Python source code from users in a "safe" way. The
isolation that WASI can provide from the host system makes this build an
attractive choice, although **this example is incomplete should be considered
unsafe** for the purpose of isolation.

## Demonstration

```
$ export CPYTHON_STDLIB=/home/snoopjedi/repos/cpython/Lib

$ python3 cpython_wrapper.py -c 'import sys; print(f"Hello world! This is CPython running on platform {sys.platform!r}"); print(sys.version)'
Could not find platform independent libraries <prefix>
Could not find platform dependent libraries <exec_prefix>
Hello world! This is CPython running on platform 'wasi'
3.13.0a3+ (heads/main-dirty:3f71c416c0, Feb  7 2024, 01:28:01) [Clang 16.0.0 ]
Fuel remaining: 926157685
Initial fuel was 1000000000
Consumed 7.4% of available fuel

$ python3 cpython_wrapper.py -c 'print(sum(n for n in range(500_000)))'  # demonstrate program that uses appreciable fraction of available fuel
Could not find platform independent libraries <prefix>
Could not find platform dependent libraries <exec_prefix>
124999750000
Fuel remaining: 97367358
Initial fuel was 1000000000
Consumed 90.3% of available fuel

$ python3 cpython_wrapper.py -c 'print(sum(n for n in range(1_000_000)))'  # demonstrate program that exceeds default fuel limit
Could not find platform independent libraries <prefix>
Could not find platform dependent libraries <exec_prefix>
wasmtime instance terminated with WASM trap: 'wasm trap: all fuel consumed by WebAssembly'
Fuel remaining: 0
Initial fuel was 1000000000
Consumed 100.0% of available fuel

$ INITIAL_FUEL=10_000_000_000 python3 cpython_wrapper.py -c "print(sum(n for n in range(1_000_000)))"  # increase fuel limit, program runs to completion
Could not find platform independent libraries <prefix>
Could not find platform dependent libraries <exec_prefix>
499999500000
Fuel remaining: 8229451158
Initial fuel was 10000000000
Consumed 17.7% of available fuel

$ INITIAL_FUEL=-1 python3 cpython_wrapper.py -c "print(sum(n for n in range(1_000_000)))"  # fuel limit disabled, program runs to completion
Could not find platform independent libraries <prefix>
Could not find platform dependent libraries <exec_prefix>
499999500000
```

(NOTE: the `Could not find platform…` errors above are a known upstream issue, but
are benign for the purposes of this demo)

## Running

* Run the CPython WASI build. Brett Cannon has written a [helpful guide](https://github.com/python/devguide/pull/1273)
to doing this.

* Place the `python.wasm` file and `lib.wasi-wasm32-3.13` directory generated
by the WASI build alongside `cpython_wrapper.py`

* Modify `cpython_wrapper.py` and define `CPYTHON_STDLIB_HOST` to point to a
copy of the CPython standard library on your host system. This probably can
point to the `Lib/` of the CPython you used for the first step.

* Invoke `cpython_wrapper.py`, passing arguments as if you were invoking CPython
(because you are!)
  * If you would like to run a file in the guest Python, you need to modify
    `cpython_wrapper.py` to call `wasi_cfg.preopen_dir()` to "mount" a host
    directory into the guest, and pass the path to the target file _in the guest_.

## Tips

* The default `INITIAL_FUEL` value chosen is extremely arbitrary, you may want to adjust
it up or down by setting the `INITIAL_FUEL` environment variable. The value corresponds
_approximately_ to [the number of WASM instructions evaluated](https://docs.wasmtime.dev/api/wasmtime/struct.Store.html#method.set_fuel).
  * You can also set `INITIAL_FUEL = -1` to disable the constraint entirely
