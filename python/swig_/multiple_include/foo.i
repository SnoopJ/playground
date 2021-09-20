%module foo

%{
#include "bar.hpp"
#include "baz.hpp"
%}

// wrap these in other files that will have a common dependency on numpy
%include "bar.i"
%include "baz.i"
