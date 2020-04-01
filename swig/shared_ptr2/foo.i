%module foo

%include <std_shared_ptr.i>

%{
#include <iostream>
#include "foo.hpp"
%}

%typemap(in) std::shared_ptr<FooInt> {
  if (PyInt_Check($input)) { // we got an integer
    auto thenum = FooInt(PyInt_AsLong($input));
    $1 = std::make_shared<FooInt>(thenum);
  } else { // we got something else, throw it back in the user's face
    PyErr_SetString(PyExc_TypeError, "Expected int");
    SWIG_fail;
  }
}

%include foo.hpp
