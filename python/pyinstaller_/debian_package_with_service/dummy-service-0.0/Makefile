all: bundle

build-venv:
	python3 -m venv build_venv
	build_venv/bin/python3 -m pip install PyInstaller \

bundle: build-venv
	# NOTE:`--python-option u` below runs the program in unbuffered mode, so that
	# the program's stdout/stderr are output to the system journal promptly
	build_venv/bin/python3 -m PyInstaller \
		--clean \
		--noconfirm \
		--name dummy-service \
		--strip \
		--python-option u \
		main.py

install:
	# this is pretty clunky and probably isn't the Right Way to do it, I'm sure there are sins here
	mkdir -p $(DESTDIR)/opt/dummy-service $(DESTDIR)/usr/bin
	# I know for sure that Debian doesn't like /opt/ but my use-case demands it
	env -C dist/ find ./dummy-service/ -type f -and -not -name "dummy-service.service" -exec install -vD {} $(DESTDIR)/opt/{} \;
	install -vD ./dummy-service.service $(DESTDIR)/lib/systemd/system/dummy-service.service
	ln -sf /opt/dummy-service/dummy-service $(DESTDIR)/usr/bin/dummy-service

deb:
	debuild --unsigned-source --unsigned-changes -b

clean:
	rm -fr \
		build/ \
		dist/ \
		build_venv/ \
		debian/dummy-service/ \
		debian/.debhelper/ \
		debian/debhelper-build-stamp \
		debian/files \
		*.spec \
