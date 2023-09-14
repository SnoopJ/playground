SHELL := /bin/bash
HERE:=$(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))


bundle:
	python3 -m PyInstaller --noconfirm main.spec

test-bundle:
	WITH_TESTS=1 python3 -m PyInstaller --noconfirm main.spec
	cp -r $(HERE)/tests ./dist/main/

test: test-bundle
	./dist/main/run_tests
