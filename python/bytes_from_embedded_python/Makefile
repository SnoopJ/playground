all: program test

# These compile flags are for the Ubuntu 20.04 system I originally ran this sample on
program:
	g++ -o main main.cpp -lm -std=c++11 -O3 -I/usr/include/python3.8/ -lpython3.8

test:
	./main 'b"hello world!"'
