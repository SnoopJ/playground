PYTHON_CFLAGS := $(shell python3-config --cflags --embed)
PYTHON_LDFLAGS := $(shell python3-config --ldflags --embed)
all: build

build:
	gcc -c $(PYTHON_CFLAGS) main.c
	gcc -o main main.o $(PYTHON_LDFLAGS)
