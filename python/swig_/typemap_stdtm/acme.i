%module acme

%{
#include "acme.hpp"
%}

// Interoperability between std::tm <-> datetime.datetime
%{
#include <ctime>
#include <datetime.h>
%}

%typemap(typecheck) std::tm
{
    PyDateTime_IMPORT;
    $1 = PyDateTime_Check($input) || PyDate_Check($input);
}

%typemap(in) std::tm
{
    PyDateTime_IMPORT;
    PyDateTime_DateTime* obj = (PyDateTime_DateTime*)$input;

    std::tm t{};
    t.tm_mday = PyDateTime_GET_DAY(obj);
    t.tm_mon = PyDateTime_GET_MONTH(obj);
    t.tm_year = PyDateTime_GET_YEAR(obj) - 1900;

    if (PyDateTime_Check(obj))
    {
        t.tm_sec = PyDateTime_DATE_GET_SECOND(obj);
        t.tm_min = PyDateTime_DATE_GET_MINUTE(obj);
        t.tm_hour = PyDateTime_DATE_GET_HOUR(obj);
    }
    else
    {
        t.tm_sec = 0;
        t.tm_min = 0;
        t.tm_hour = 0;
    }

    $1 = t;
}

%typemap(out) std::tm
{
    PyDateTime_IMPORT;
    $result = PyDateTime_FromDateAndTime(
        $1.tm_year,
        $1.tm_mon,
        $1.tm_mday,
        $1.tm_hour,
        $1.tm_min,
        $1.tm_sec,
        0  // microseconds, which std::tm does not represent
    );
}

%include "acme.hpp"
