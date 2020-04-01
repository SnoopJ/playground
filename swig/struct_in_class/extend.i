%module extend

%{
#include "extend.hpp"
%}

%feature("flatnested", "1");

%include "extend.hpp"

