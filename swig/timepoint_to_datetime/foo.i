%module foo

%{
#include "foo.hpp"
%}

%typemap(out) std::chrono::steady_clock::time_point
{
    using namespace std::chrono;

    steady_clock::time_point *t = &$1;

    double conv = (float)(steady_clock::duration::period::num) / steady_clock::duration::period::den;

    steady_clock::duration dt = t->time_since_epoch();

    $result = PyFloat_FromDouble(dt.count() * conv);
}

%include "foo.hpp"
