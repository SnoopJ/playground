all: wrap test

wrap:
	swig -python -c++ foo.i
	g++ -fPIC -c foo.cpp
	g++ -fPIC -c -I/home/jgerity/.pyenv/versions/3.6.9/include/python3.6m foo_wrap.cxx
	g++ -shared foo.o foo_wrap.o -o _foo.so

test:
	pytest --tb=line test.py
