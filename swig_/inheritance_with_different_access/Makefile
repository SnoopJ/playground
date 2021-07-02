PYTHON_INCLUDE := $(shell python3 -c "from sysconfig import get_path; print(get_path('include'))")

all: lib wrap test

lib:
    @echo "\n========================="
    @echo "Compiling CXX object lib.o"
    @echo "=========================\n"
    g++ -fPIC -c lib.cpp

swig:
    @echo "\n========================="
    @echo "Running SWIG against lib.i"
    @echo "=========================\n"
    swig -python -c++ lib.i

wrap: lib swig
    @echo "\n========================="
    @echo "Compiling lib_wrap.cxx"
    @echo "=========================\n"
    g++ -fPIC -c -I$(PYTHON_INCLUDE) lib_wrap.cxx

    @echo "\n========================="
    @echo "Linking _lib.so"
    @echo "=========================\n"
    g++ -shared lib.o lib_wrap.o -o _lib.so

test:
    @echo "\n========================="
    @echo "Invoking pytest"
    @echo "=========================\n"
    python3 -m pytest -vvv .

clean:
    rm -fr __pycache__
    rm -f \
        lib.py \
        _lib.so \
        lib.o \
        lib_wrap.o \
        lib_wrap.cxx \
