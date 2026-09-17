all: bundle


clean:
	rm -fr build/ dist/


bundle:
	python3 -m PyInstaller --noconfirm app.spec
	mkdir dist/app/vendor
