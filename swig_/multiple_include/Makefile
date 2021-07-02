all: lib wrap test

lib:
	g++ -fPIC -c bar.cpp baz.cpp

wrap:
	swig -python -c++ foo.i
	g++ -fPIC -c -I/home/jgerity/.pyenv/versions/3.6.9/include/python3.6m -I/home/jgerity/py3.6/lib/python3.6/site-packages/numpy/core/include foo_wrap.cxx
	g++ -shared bar.o baz.o foo_wrap.o -o _foo.so

test:
	pytest --tb=line test_foo.py

clean:
	rm -fr __pycache__
	rm -f *.o \
	      *_wrap.cxx \
	      *_wrap.o \
	      _*.so \
	      foo.py
