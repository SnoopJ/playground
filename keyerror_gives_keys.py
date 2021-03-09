"""
A doodle inspired by 8 March 2021 discussion on the Boston Python slack about
how it'd be nice to just see the keys available in an object when you fail to
index something.

This code is specific to dicts, but the approach could probably be generalized
to handle other mapping types.

Written for Python 3.9
"""
import ast
import dis
import sys
import textwrap
import traceback
from types import TracebackType
from typing import Any, Sequence

from pprint import pprint


def gimmekeys(exctype: type[Exception], value: Exception, tb: TracebackType):
    """Exception handler """
    # first, whatever normally happens (usually printing the traceback)
    result = sys.__excepthook__(exctype, value, tb)
    # NOTE: this line wouldn't play nice with any other custom excepthooks,
    # because it assumes it should just call the builtin

    # then, our custom logic
    if issubclass(exctype, KeyError):
        print("\n--- DICT KEY HELPER ---")
        _report_keys(exctype, value, tb)

    return result


def _report_keys(exctype: type[KeyError], value: KeyError, tb: TracebackType) -> bool:
    """Try to report the keys in the object associated with the failing indexing operation"""
    def _fail(msg: str):
        print(msg)
        return False
    frame = tb.tb_frame
    lastop = tb.tb_lasti
    code = frame.f_code

    instrs = list(dis.get_instructions(code))
    # find the index of the opcode that failed
    instr_num, failing_op = next((num, i) for num, i in enumerate(instrs) if i.offset == tb.tb_lasti)
    if failing_op.opname != "BINARY_SUBSCR": _fail(f"Sorry, only know how to handle exceptions raised from a BINARY_SUBSCR opcode, got {failing_op.opname=}")

    key = instrs[instr_num-1]  # top of stack (TOS) is whatever the key is
    target = instrs[instr_num-2]  # TOS-1 is the target
    if target.opname != "LOAD_NAME": _fail(f"Sorry, only know how to handle LOAD_NAME targets for BINARY_SUBSCR, got: {target.opname=} at {target.offset=}")

    tbexc = traceback.TracebackException.from_exception(value, capture_locals=True)
    varz = tbexc.stack[0].locals
    objname = target.argval
    objsrc = varz[objname]

    MAXLEN = 1 << 20  # allow up to ~1 MB of dict literal
    if len(objsrc) <= MAXLEN:
        obj = ast.literal_eval(objsrc)
        try:
            _maybe_report_keys(obj, name=objname)
        except Exception as exc:
            _fail(f"Exception {exc=} while trying to get keys from object of {type(obj)=}")
    else:
        _fail(f"Object exceeds {MAXLEN=} characters, skipping...")

    return True


def _maybe_report_keys(obj: Any, name: str):
    """If the given object is a dict, print out its keys"""
    if isinstance(obj, dict):
        keys = textwrap.fill('\t'.join(map(str, obj.keys())), width=80)  # make a nice 80-wide tab-aligned table
        print(f"Keys for {name}:")
        print("---")
        print(keys)
        print("---\n")


sys.excepthook = gimmekeys  # install our custom hook, which will run for all unhandled KeyErrors

### ---
### Hypothetical program that raises an unhandled KeyError
### ---

import random
import string

wrongdict = {k:v for k,v in (random.sample(range(1024), k=2) for _ in range(100))}
d = {
        "foo": "bar",
        **{''.join(random.sample(string.ascii_lowercase, k=random.randint(3, 5))): -1 for _ in range(100)}
        }

# a syntactically-pathological indexing operation that raises a KeyError
(wrongdict + d
        [
        "baz"

        ]
        )
