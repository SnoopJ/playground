%module test

%{
#include "test.hpp"
#include <iostream>
%}

/* sanity check: let's map returned ints in the original file to floats */
%typemap(out) int
{
    std::cout << "Hello from int typemap\n";
    $result = PyFloat_FromDouble((double)$1);
}

/* Sanity check: can I turn a vector of ints into a list? */
%typemap(out) std::vector<int>
{
    std::cout << "Hello from vector<int> typemap\n";
    size_t sz = ($1).size();
    $result = PyList_New(sz);
    for (int i = 0; i < sz; i++)
    {
        PyList_SetItem($result, i, PyInt_FromLong((long)($1).at(i)));
    }
}


/* Sanity check: turn an unordered_map<std::string, int> into a dictionary */
%typemap(out) std::unordered_map<std::string, int>
{
    std::cout << "Hello from umap typemap\n";
    PyObject* d = PyDict_New();
    for (auto &val : $1)
    {
        auto k = PyUnicode_FromString(val.first.c_str());
        auto v = PyInt_FromLong((long)val.second);
        PyDict_SetItem(d, k, v);
    }
    $result = d;
}

%typemap(out) std::unordered_map<std::string, MyObj>
{
    std::cout << "Hello from umap_myobj typemap\n";
    PyObject* d = PyDict_New();
    for (auto &val : $1)
    {
        auto k = PyUnicode_FromString(val.first.c_str());
        auto v = PyInt_FromLong((long)val.second);
        PyDict_SetItem(d, k, v);
    }
    $result = d;
}

int foo();
std::vector<int> do_the_thing();
std::unordered_map<std::string, int> foo_the_thing();
std::unordered_map<std::string, MyObj> umap_myobj();
