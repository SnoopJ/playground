all:
	swig -python -c++ acme.i
	g++ -fPIC -c acme.cpp
	g++ -fPIC -c -I/usr/include/python3.8 acme_wrap.cxx
	g++ -shared acme.o acme_wrap.o -o _acme.so
