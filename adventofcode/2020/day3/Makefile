all: build exec

build:
	g++-9 -std=c++17 -fPIC solution.cpp -o solution

exec:
	./solution input.txt

random:
	python3 generate_grid.py > test.txt
	./solution test.txt

clean:
	rm -f solution
	rm -f test.txt
