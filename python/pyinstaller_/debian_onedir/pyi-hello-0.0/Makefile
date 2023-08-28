all: bundle

build-venv:
	python3 -m venv build_venv
	build_venv/bin/python3 -m pip install PyInstaller \

bundle: build-venv
	build_venv/bin/python3 -m PyInstaller \
		--clean \
		--noconfirm \
		--name pyi-hello \
		--strip \
		main.py

install:
	# this is pretty clunky and probably isn't the Right Way to do it, I'm sure there are sins here
	mkdir -p $(DESTDIR)/opt/pyi-hello $(DESTDIR)/usr/bin
	# I know for sure that Debian doesn't like /opt/ but my use-case demands it
	env -C dist/ find ./pyi-hello/ -type f -exec install -vD {} $(DESTDIR)/opt/{} \;
	ln -sf /opt/pyi-hello/pyi-hello $(DESTDIR)/usr/bin/pyi-hello

deb:
	debuild --unsigned-source --unsigned-changes -b

clean:
	rm -fr \
		build/ \
		dist/ \
		build_venv/ \
		debian/pyi-hello/ \
		debian/.debhelper/ \
		debian/debhelper-build-stamp \
		debian/files \
		*.spec \
