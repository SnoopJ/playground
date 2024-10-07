from cffi import FFI


# Invoked at package build time via setup.py
ffi = FFI()
src = r"""
#include <stdio.h>

void cffihello(void) {
    printf("hello from cffi\n");
}

"""

ffi.set_source("cffiwhat._cffiwhat_c", src)
ffi.cdef("""
void cffihello(void);
""")


