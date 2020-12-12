all: build exec

sample: build exec_sample

build:
	g++-9 -Wall -std=c++17 -fPIC solution.cpp -o solution

exec:
	./solution input.txt

exec_sample:
	./solution sample_input.txt

clean:
	rm -f solution
