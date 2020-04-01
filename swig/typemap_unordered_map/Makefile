all:
	swig -python -c++ test.i
	g++ -fPIC -c test.cpp
	g++ -fPIC -c -I/home/jgerity/.pyenv/versions/3.6.9/include/python3.6m test_wrap.cxx
	g++ -shared test.o test_wrap.o -o _test.so
