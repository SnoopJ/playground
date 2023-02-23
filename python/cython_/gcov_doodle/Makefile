all: mymod main

clean:
	rm -f main *.gcno *.o *.gcda *.so *.c *.gcov

main:
	python3.8 -m cython -3 --embed main.pyx
	gcc -O1 -fPIC --coverage -Wall -I/usr/include/python3.8 -c -o main.o main.c
	gcc main.o -fprofile-arcs -lpython3.8 -lgcov -o main

mymod:
	python3.8 -m cython -3 mymod.pyx
	gcc -O1 -fPIC --coverage -Wall -I/usr/include/python3.8 -c -o mymod.o mymod.c
	gcc -shared mymod.o -fprofile-arcs -lgcov -lpython3.8 -o mymod.so
