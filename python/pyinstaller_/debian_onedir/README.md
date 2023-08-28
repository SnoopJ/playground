This example shows how to package a [PyInstaller](https://pyinstaller.org/)
`onefile` distribution as a [Debian binary package](https://www.debian.org/doc/debian-policy/ch-binary.html).

To build the package on Debian/Ubuntu, install the official `devscripts`
package, change to the `pyi-hello-0.0` directory, and run `make deb` or
`debuild --unsigned-source --unsigned-changes -b`. The resulting `.deb` will be
in the parent directory (i.e. the one this `README` lives in), and it can be
installed with `dpkg -i pyi-hello_0.0-1_amd64.deb`, which will install the
PyInstaller distribution to `/opt/pyi-hello` and drop a symlink to the
entrypoint in `/usr/bin/`.

It's rough around the edges (the Debian package linter will *definitely*
complain) and I've pieced it together after reading multiple sources, but
perhaps it will be helpful to you too. These are the resources I leaned on most
heavily while preparing this sample:

* https://www.debian.org/doc/manuals/packaging-tutorial/packaging-tutorial.en.pdf
* https://tldp.org/HOWTO/html_single/Debian-Binary-Package-Building-HOWTO
* https://www.debian.org/doc/debian-policy/ch-binary.html

Note that I have deliberately _not_ filled in a lot of the metadata in the
files in the `debian/` directory to keep this example straightforward.
