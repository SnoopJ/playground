Example of instrumenting a Cython extension module with `gcov`

```
$ ls
Makefile  main.pyx  mymod.pyx
$ make
python3.8 -m cython -3 mymod.pyx
gcc -O1 -fPIC --coverage -Wall -I/usr/include/python3.8 -c -o mymod.o mymod.c
gcc -shared mymod.o -fprofile-arcs -lgcov -lpython3.8 -o mymod.so
python3.8 -m cython -3 --embed main.pyx
gcc -O1 -fPIC --coverage -Wall -I/usr/include/python3.8 -c -o main.o main.c
gcc main.o -fprofile-arcs -lpython3.8 -lgcov -o main
$ ls *.gcda  # nothing has been run yet, no coverage data exists
ls: cannot access '*.gcda': No such file or directory
$ python3.8 -c "import mymod"  # importing the extension module generates coverage data for
$ ls *.gcda
mymod.gcda
$ gcov mymod.gcda
File 'mymod.c'
Lines executed:34.72% of 216
Creating 'mymod.c.gcov'

File '/usr/include/python3.8/object.h'
Lines executed:40.00% of 5
Creating 'object.h.gcov'
$ rm *.gcda && ./main  # executing the generated entrypoint generates coverage for both the entrypoint and the extension module
$ ls *.gcda
main.gcda  mymod.gcda
```
