%module foo

%{
#include "foo.hpp"
%}

%typemap(in) Foo {
  $1 = Foo(-1);
}

%typemap(in) int {
  $1 = PyInt_AsLong($input);
}

%include foo.hpp
