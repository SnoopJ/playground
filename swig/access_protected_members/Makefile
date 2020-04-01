all: lib wrap test

lib:
	g++ -fPIC -c foo.cpp
	g++ -fPIC foo.o -o foo

wrap:
	swig -python -c++ foo.i
	g++ -fPIC -c -I/home/jgerity/.pyenv/versions/3.6.9/include/python3.6m foo_wrap.cxx
	g++ -shared foo_wrap.o foo.o -o _foo.so

test:
	pytest --tb=line test_foo.py

clean:
	rm -fr __pycache__
	rm -f foo \
              foo.o \
	      foo_wrap.cxx \
	      foo_wrap.o \
	      _foo.so \
	      foo.py
