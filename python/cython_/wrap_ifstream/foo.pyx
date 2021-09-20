# cython: c_string_type=unicode, c_string_encoding=utf8
# the above declaration gives us nice decoding to str "for free", but there are edge cases
# see the Cython manual for the complete story: https://cython.readthedocs.io/en/latest/src/tutorial/strings.html
from foo_decl cimport ifstream
from libcpp.string cimport string

def load_wrap(fn):
    # NOTE: I'm being lazy here and just hard-coding some buffer sizes...
    cdef char[512] result
    ifstream(fn).read(result, 511)
    return result
