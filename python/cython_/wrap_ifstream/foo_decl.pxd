# distutils: language = c++
from libc.stdint cimport *
from libcpp.string cimport string


cdef extern from "<fstream>" namespace "std":
    cdef cppclass istream:
        # we don't need any details from this STL class
        pass

    cdef cppclass ifstream:
        ifstream(const string& filename) except +
        istream read(char*, int count) except +


cdef extern from "foo.hpp":
    ifstream load(const string& fn)
