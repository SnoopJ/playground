PYTHON_CFLAGS := $(shell python3-config --cflags --embed)
PYTHON_LDFLAGS := $(shell python3-config --ldflags --embed)
all: build

build:
	gcc -o main main.c $(PYTHON_CFLAGS) $(PYTHON_LDFLAGS)
