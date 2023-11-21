all: broken-bundle patched-bundle

clean:
	rm -fr \
		build/ \
		dist/

broken-bundle:
	DISABLE_SOURCE_TRANSFORM=1 python3 -m PyInstaller app.spec

patched-bundle:
	python3 -m PyInstaller app.spec
