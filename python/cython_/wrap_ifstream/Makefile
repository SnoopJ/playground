# Python 3.8 here because apparently there's a bug in 3.9 that makes the pytest part of this fail?
# https://bugs.python.org/issue43155
PYINCLUDE := $(shell python3.8 -c 'import sysconfig; print(sysconfig.get_config_var("INCLUDEPY"))')

all: lib test

clean:
	rm -f foo_wrap.cpp foo.so

cython:
	cython -3 -I$PWD foo.pyx -o foo_wrap.cpp

lib: cython
	g++ -fPIC -shared -I${PYINCLUDE} -I${PWD} foo_wrap.cpp -o foo.so

test:
	pytest test_foo.py
