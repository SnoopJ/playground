#include <stdio.h>
#include "Python.h"


int main()
{
    // not necessary for *this* program, but will be useful when inspecting these
    // objects in gdb; in particular, PyLong_AsLong() will segfault without this init
    Py_Initialize();

    PyTupleObject* tup = (PyTupleObject*)PyTuple_New(2);
    PyTuple_SET_ITEM(tup, 0, PyLong_FromLong(111));
    PyTuple_SET_ITEM(tup, 1, PyLong_FromLong(222));

    PyListObject* lst = (PyListObject*)PyList_New(2);
    PyList_SET_ITEM(lst, 0, PyLong_FromLong(333));
    PyList_SET_ITEM(lst, 1, PyLong_FromLong(444));

    // As far as C sizeof() is concerned, these objects differ in size by
    // sizeof(Py_ssize_t) (=8 bytes) because of the `allocated` member in PyListObject
    // which is not part of PyTupleObject
    printf("C sizes:\n---\n");
    printf("sizeof(PyTupleObject) = %ld\n", sizeof(PyTupleObject));
    printf("sizeof(PyListObject) = %ld\n", sizeof(PyListObject));

    printf("\n");

    // As far as Python's sys.getsizeof() is concerned, these objects differ in size
    // by an additional sizeof(PyObject**) (=8 bytes) because PyListObject's `ob_item`
    // member points to some other memory, and the pointer that keeps track of this
    // indirection costs this much.
    //
    // NOTE: the sizes reported by Python also account for the size of the 'extra' data
    // associated with each struct and the garbage collector's "preheader"
    // (2*sizeof(PyObject*) = 16 bytes as of 3.9), so the most relevant thing to this
    // exploration is the DIFFERENCE between these values
    printf("Python sizes:\n---\n");
    printf("sizeof(tup) = %ld\n", _PySys_GetSizeOf((PyObject*)tup));
    printf("sizeof(lst) = %ld\n", _PySys_GetSizeOf((PyObject*)lst));

    // To put it another way: the data 'in' an instance of PyTupleObject is
    // referred to by a sequence of pointers at the struct, and the struct's `ob_item`
    // is the location of the first pointer. But a PyListObject refers to its data
    // by a sequence of pointers stored somewhere else, and has to store a pointer
    // to that location
    return 0;
}
