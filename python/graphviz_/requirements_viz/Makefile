.PHONY: render

all: target-requirements.txt render

target-requirements.txt: target-requirements.in
	pip-compile -v -o target-requirements.txt target-requirements.in

render: target-requirements.txt
	python3 render_requirements.py target-requirements.txt
