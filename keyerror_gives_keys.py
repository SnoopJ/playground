"""
A doodle inspired by 8 March 2021 discussion on the Boston Python slack about
how it'd be nice to just see the keys available in an object when you fail to
index something.

This code is specific to dicts, but the approach could probably be generalized
to handle other mapping types.

Written for Python 3.9

Sample output:

$ python3.9 keyerror_gives_keys.py
Traceback (most recent call last):
  File "/home/snoopjedi/playground/keyerror_gives_keys.py", line 131, in <module>
    (wrongdict + d
KeyError: 'baz'

--- DICT KEY HELPER ---
Keys for d:
---
foo     wiux    onh     mei     nfkp    fyx     mqcdf   ktnz    hlg     ftzdg
fibg    twbkf   als     kgxsf   zpesw   cpk     ibhpn   fou     maxg    kphvf
jugr    xlu     wanoz   whqva   szku    wjyl    mhvog   zyp     kdna    ejabd
zceng   rpm     grhn    imr     jhvoy   atq     hrg     srtu    zoc     tsgxw
tsw     nascv   muc     vidw    hifu    sibud   dys     zdtva   qsz     feuj
ybftq   fpcem   nuw     sbu     qrsuz   caq     tckd    pbax    afjx    zsdy
ojkmw   uin     qeswh   yncsj   kiaj    swq     kosae   oyr     edasy   uvb
hcv     skoew   wznvg   jvue    xflnu   ktq     cjxg    nrw     rbhxk   qds
bekc    fbcj    ouja    zwy     pcxe    igha    jlzpa   hli     azd     pyso
svlw    orv     eatz    mdon    soehk   mlpaz   gab     rwtz    jefw    vpy
dhj     322     453     496     999     224     70      526     889     882
314     433     134     147     1020    699     135     946     319     118
613     71      321     18      444     952     790     835     945     383
845     603     727     647     46      814     961     750     286     878
442     615     127
---

"""
import ast
import dis
import sys
import textwrap
import traceback
from types import TracebackType
from typing import Any, Sequence

from pprint import pprint


class KeyHelperException(Exception):
    pass


def gimmekeys(exctype: type[Exception], value: Exception, tb: TracebackType):
    """Exception handler """
    # first, whatever normally happens (usually printing the traceback)
    result = sys.__excepthook__(exctype, value, tb)
    # NOTE: this line wouldn't play nice with any other custom excepthooks,
    # because it assumes it should just call the builtin

    # then, our custom logic
    if issubclass(exctype, KeyError):
        print("\n--- DICT KEY HELPER ---")
        try:
            _report_keys(exctype, value, tb)
        except KeyHelperException as exc:
            print(*exc.args)

    return result


def _report_keys(exctype: type[KeyError], value: KeyError, tb: TracebackType) -> bool:
    """Try to report the keys in the object associated with the failing indexing operation"""
    def _fail(msg: str):
        raise KeyHelperException(msg)
    frame = tb.tb_frame
    lastop = tb.tb_lasti
    code = frame.f_code

    instrs = list(dis.get_instructions(code))
    # find the index of the opcode that failed
    instr_num, failing_op = next((num, i) for num, i in enumerate(instrs) if i.offset == tb.tb_lasti)
    prev = instrs[instr_num-1]  # hopefully an instruction that just pushed a key
    pprev = instrs[instr_num-2]  # hopefully an instruction that just pushed a name associated with a target object
    if (failing_op.opname != "BINARY_SUBSCR" or not all(op.opname.startswith("LOAD_") for op in [pprev, prev])):
        _fail(f"Only know how to handle a BINARY_SUBSCR preceded by two LOAD_* ops, got: {pprev.opname}, {prev.opname}, {failing_op.opname}")
    key, target = prev, pprev

    if target.opname != "LOAD_NAME": _fail(f"only know how to handle LOAD_NAME targets for BINARY_SUBSCR, got: {target.opname=} at {target.offset=}")

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
        **{''.join(random.sample(string.ascii_lowercase, k=random.randint(3, 5))): -1 for _ in range(100)},
        **{k: -1 for k in random.sample(range(1024), k=42)}
        }

# a syntactically-pathological indexing operation that raises a KeyError
(wrongdict + d
        [
        "baz"

        ]
        )

# these examples will NOT work, but shouldn't fail any harder than the KeyError would have:

# {1: 2}[42]  # indexing a dict literal
# x="z"; d = {"foo": "bar"}; d["ba" + x]  # indexing with an expression
