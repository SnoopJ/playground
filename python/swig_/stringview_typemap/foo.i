%module foo

%{
#include <string_view>
#include "foo.hpp"
%}

%typemap(in) std::string_view
{
// NOTE:20210413:PyUnicode_READY will be removed in 3.12, see https://docs.python.org/3.10/c-api/unicode.html#c.PyUnicode_READY
#if PY_VERSION_HEX < 0x03120000
    if(PyUnicode_READY($input) != 0) {
        SWIG_exception_fail(SWIG_RuntimeError, "cannot ensure unicode object is canonical");
    }
#endif
    Py_ssize_t* size;
    const char* data = PyUnicode_AsUTF8AndSize($input, size);
    $1 = std::string(data, *size);
}

%typemap(freearg) std::string_view {}  // no cleanup needed, we only use the stack

// NOTE:20210413:This assumes UTF-8 encoding
%typemap(out) std::string_view
{
    PyErr_WarnEx(PyExc_UserWarning, "Making a copy of a view, changes to the underlying string will NOT be visible", 1);
    $result = PyUnicode_FromStringAndSize($1.data(), $1.size());
}

%include "foo.hpp"
