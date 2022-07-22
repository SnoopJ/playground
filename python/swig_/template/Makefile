PYTHON_INCLUDE := $(shell python3 -c "from sysconfig import get_path; print(get_path('include'))")
all: lib wrap test

lib:
	g++ -std=c++17 -fPIC -c foo.cpp
	g++ -std=c++17 -fPIC foo.o -o foo

wrap: generate_wrapper build_wrapper

generate_wrapper:
	swig -python -c++ foo.i

build_wrapper:
	g++ -std=c++17 -fPIC -c -I$(PYTHON_INCLUDE) foo_wrap.cxx
	g++ -std=c++17 -shared foo.o foo_wrap.o -o _foo.so

test:
	pytest -s --tb=line test_foo.py

clean:
	rm -fr __pycache__
	rm -f foo \
		  foo.o \
		  foo_wrap.cxx \
		  foo_wrap.o \
		  _foo.so \
		  foo.py
