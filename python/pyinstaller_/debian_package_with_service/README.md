This example shows how to package a [PyInstaller](https://pyinstaller.org/)
`onedir` distribution as a [Debian binary package](https://www.debian.org/doc/debian-policy/ch-binary.html)
along with a `systemd` service.

To build the package on Debian/Ubuntu, install the official `devscripts`
package, change to the `dummy-service-0.0` directory, and run `make deb` or
`debuild --unsigned-source --unsigned-changes -b`. The resulting `.deb` will be
in the parent directory (i.e. the one this `README` lives in), and it can be
installed with `dpkg -i dummy-service_0.0-1_amd64.deb`, which will install the
PyInstaller distribution and a corresponding `systemd` service which will be
started after installation. The dummy service prints its own uptime every 3
seconds, you can view the output by running `journalctl -f --unit dummy-service`
