%module foo

%{
#include "foo.hpp"
%}

%ignore Foo::taco;
%include "foo.hpp"
