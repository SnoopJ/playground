all:
	swig -python -c++ extend.i
	g++ -fPIC -c extend.cpp
	g++ -fPIC -c -I/home/jgerity/.pyenv/versions/3.6.9/include/python3.6m extend_wrap.cxx
	g++ -shared extend.o extend_wrap.o -o _extend.so
