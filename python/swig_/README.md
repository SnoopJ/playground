# My SWIG sample gallery

This repository is meant to contain examples for tasks I've run into
while working with SWIG. To add a sample, copy the `template` and write
your problem into `foo.cpp, foo.hpp, foo.i`. Tests go in `test_foo.py`,
if you want to have them. 

## Make targets
* `make lib` compiles the `foo` executable
* `make wrap` compiles the SWIG bindings
* `make test` runs pytest
* `make` or `make all` does all of the above
