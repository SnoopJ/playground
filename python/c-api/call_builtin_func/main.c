/*
 * This program demonstrates how to call `bin(1234)` using the CPython C API
 * Based on a question asked in #python on the Libera.chat IRC network on 14 Oct 2022
 */

#include "Python.h"

// NOTE: it is unconventional to do this NULL check with a macro in normal
// C-API usage, but it makes this program more legible
#define NULLCHECK(x) \
    if (x == NULL) { \
        PyErr_SetString(PyExc_RuntimeError, "Got NULL value"); \
        goto err; \
    }

int
main()
{
    Py_Initialize();

    PyObject *builtins, *binfunc, *num, *args, *result;
    builtins = binfunc = num = args = result = NULL;

    // Get the `bin` builtin object by first getting a dictionary, then indexing into it
    builtins = PyEval_GetBuiltins();
    NULLCHECK(builtins);
    binfunc = PyDict_GetItemString(builtins, "bin");
    NULLCHECK(binfunc);

    num = PyLong_FromLong(1234);
    NULLCHECK(num);

    // NOTE: the previous step and this one could be combined into Py_BuildValue("(i)", 1234) but
    // this example is structured assuming that the user would want to call bin() for some object
    // that came from another part of the program
    args = Py_BuildValue("(O)", num);
    NULLCHECK(args);

    // this line along with the previous definitions is equivalent to running `bin(1234)` in Python
    result = PyObject_CallObject(binfunc, args);
    NULLCHECK(result);

    // add on a newline for pretty output
    result = PyUnicode_Concat(result, Py_BuildValue("s", "\n"));
    NULLCHECK(result);

    // finally, display the result
    PyObject_Print(result, stdout, Py_PRINT_RAW);

    return 0;

err:
    PyErr_Print();

    // decrement any lingering references
    Py_XDECREF(builtins);
    Py_XDECREF(binfunc);
    Py_XDECREF(num);
    Py_XDECREF(args);
    Py_XDECREF(result);

    exit(1);
}
