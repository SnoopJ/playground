/*
 *
 * This is an example program of how to provision an embedded CPython's __main__
 * with some attributes (some of which are imports from elsewhere) before calling
 * into the interactive console. Based on a question in Libera #python on 20 July, 2022
 *
 * */
#define PY_SSIZE_T_CLEAN
#include <Python.h>

// NOTE: these are naughty macros, but I am lazy and these checks clutter this example anyway
#define CHECK(x) \
    if (x == NULL) { \
        fprintf(stderr, "bad value '%s'\n", #x); \
        exit(1); \
    }

#define CHECK_VAL(x,val) \
    if (x != val) { \
        fprintf(stderr, "bad value '%s' (expected %s)\n", #x, #val); \
        exit(1); \
    }


int
main(int argc, char *argv[])
{
    int err;
    wchar_t *program;
    PyObject *mainmod, *globals, *tmpmod, *tmpmod_d,
             *code, *console, *result, *cls, *interact;

    program = Py_DecodeLocale(argv[0], NULL);
    if (program == NULL) {
        fprintf(stderr, "Fatal error: cannot decode argv[0]\n");
        exit(1);
    }
    Py_SetProgramName(program);  /* optional but recommended */
    Py_Initialize();

    mainmod = PyImport_ImportModule("__main__");
    CHECK(mainmod);

    globals = PyModule_GetDict(mainmod);
    CHECK(globals);

    Py_XDECREF(mainmod);

    // Setting a value directly in the module
    err = PyDict_SetItemString(globals, "x", Py_BuildValue("i", 42));
    CHECK_VAL(err, 0);

    // I was VERY mistaken about how PyImport_ImportModuleEx() works with the locals/globals
    // arguments given. The result is still a module object that needs to be unpacked into
    // the desired namespace if there is one.
    tmpmod = PyImport_ImportModuleEx("pathlib", NULL, NULL, Py_BuildValue("[s]", "Path"));
    CHECK(tmpmod);

    tmpmod_d = PyModule_GetDict(tmpmod);
    CHECK(tmpmod);

    err = PyDict_Update(globals, tmpmod_d);
    CHECK_VAL(err, 0);
    Py_XDECREF(tmpmod);
    Py_XDECREF(tmpmod_d);

    code = PyImport_ImportModule("code");
    CHECK(code);

    cls = PyObject_GetAttrString(code, "InteractiveConsole");
    CHECK(cls);
    Py_XDECREF(code);

    console = PyObject_CallOneArg(cls, globals);
    CHECK(console);
    Py_XDECREF(cls);

    interact = PyObject_GetAttrString(console, "interact");
    CHECK(interact);

    result = PyObject_CallNoArgs(interact);
    CHECK(result);
    Py_XDECREF(interact);
    Py_XDECREF(result);

    if (Py_FinalizeEx() < 0) {
        exit(120);
    }
    PyMem_RawFree(program);
    return 0;
}
