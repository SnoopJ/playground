PYTHON_CFLAGS := $(shell python3.9-config --cflags --embed)
PYTHON_LDFLAGS := $(shell python3.9-config --ldflags --embed)
all: build

build:
	gcc -c $(PYTHON_CFLAGS) -O0 main.c
	gcc -o main main.o $(PYTHON_LDFLAGS) -O0

clean:
	rm main main.o
