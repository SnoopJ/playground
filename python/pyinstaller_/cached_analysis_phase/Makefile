build:
	@echo "---"
	@echo "Building original bundle"
	@echo "---"
	@echo
	@cp main.py.orig main.py
	@python3 -m PyInstaller \
		--clean \
		--noconfirm \
		main.spec

build-modified:
	@echo "---"
	@echo "Building modified bundle"
	@echo "---"
	@echo
	@cp main.py.mod main.py
	@PYI_ANALYSIS_CACHE=1 \
		python3 -m PyInstaller \
			--clean \
			--noconfirm \
			main.spec

run: build
	@echo "---"
	@echo "Running original bundle"
	@echo "---"
	@echo
	./dist/main/main

run-modified: build-modified
	@echo "---"
	@echo "Running modified bundle"
	@echo "---"
	@echo
	./dist/main/main

.PHONY: build build-modified run run-modified
