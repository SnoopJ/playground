"""
This sample illustrates a Windows service with an improper SvcStop() that can
leave the uvicorn web server running, as well as the right way to do it

The canonical reproduction of this is to run the service in debug mode; in the
case that inspired me to create this sample, I was bundling the file using
PyInstaller, full sequence:

    $ python3 -m PyInstaller service_shutdown_uvicorn.py
    ...
    $ ./dist/service_shutdown_uvicorn/service_shutdown_uvicorn.exe debug
    ...
    <Ctrl-C>
    <shutdown allegedly happens>
    <server is still running>

"""
import socket
import sys

# Windows API helpers
import win32serviceutil
import win32service
import servicemanager

import uvicorn


LOG_LEVEL = "info"


def _get_socket() -> socket.socket:
    sock = socket.create_server(('0.0.0.0', 9200))

    return sock


def _make_server():
    from fastapi import FastAPI
    app = FastAPI()

    sock = _get_socket()
    config = uvicorn.Config(app, log_level=LOG_LEVEL)
    server = uvicorn.Server(config=config)

    return server, sock


class DummyService(win32serviceutil.ServiceFramework):

    _svc_name_ = "DummyService"
    _svc_deps = None  # sequence of service names this service depends on, or None
    _svc_display_name_ = 'Dummy Service'

    def SvcStop(self):
        """Stop the service"""
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)

        # NOTE:Uncomment the below to get proper shutdown of the web server
        # server = getattr(self, "server", None)
        # if server:
        #     server.should_exit = True

        self.ReportServiceStatus(win32service.SERVICE_STOPPED)

    def SvcDoRun(self):
        """Start the service; does not return until stopped"""
        self.server, sock = _make_server()
        # NOTE:The '*_' here swallows potential additional (uninteresting) information from e.g. IPv6 addresses
        host, port, *_ = sock.getsockname()
        self.socks = [sock]
        self.server.run(sockets=self.socks)


def main():
    if len(sys.argv) == 1:
        servicemanager.Initialize()
        servicemanager.PrepareToHostSingle(DummyService)
        servicemanager.StartServiceCtrlDispatcher()
    else:
        win32serviceutil.HandleCommandLine(DummyService)


if __name__ == '__main__':
    main()
