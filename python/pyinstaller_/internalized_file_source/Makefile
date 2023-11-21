all: bundle patched-bundle

clean:
	rm -fr \
		build/ \
		dist/ \
		staging/ \
		transformed/

transform_source:
	mkdir -p transformed/
	python3 transform_source.py libapp.py > transformed/libapp.py

staging:
	mkdir -p staging/

bundle: staging
	cp libapp.py main.py staging/
	env -C staging/\
		python3 -m PyInstaller \
			--distpath ../dist \
			--workpath ../build \
			--name app \
			libapp.py \
			main.py

patched-bundle: staging transform_source
	cp patch.py transformed/libapp.py main.py staging/
	env -C staging/\
		python3 -m PyInstaller \
			--distpath ../dist \
			--workpath ../build \
			--name app_patched \
			patch.py \
			libapp.py \
			main.py
