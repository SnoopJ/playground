import sys

# Windows API helpers
import win32serviceutil
import win32service
# NOTE: win32timezone is an induced dependency, this is here for PyInstaller's sake
import win32timezone  # noqa
import servicemanager


def _install_excepthook():
    from acmelib import logger

    _original_excepthook = sys.excepthook

    def _log_excepthook(*exc_info):
        exc_type, exc_value, exc_tb = exc_info
        logger.exception("Uncaught exception:", exc_info=exc_info)
        _original_excepthook(*exc_info)

    sys.excepthook = _log_excepthook
    logger.debug("entrypoint excepthook installed")


class AcmeDummyService(win32serviceutil.ServiceFramework):

    _svc_name_ = "AcmeDummyService"
    _svc_deps = None  # sequence of service names this service depends on, or None
    _svc_display_name_ = 'Acme Dummy Service'

    def SvcStop(self):
        """Stop the service"""
        self.ReportServiceStatus(win32service.SERVICE_STOPPED)

    def SvcDoRun(self):
        """Start the service; does not return until stopped"""
        _install_excepthook()

        from acmelib import main as acme_main
        acme_main()


def main():
    if len(sys.argv) == 1:
        servicemanager.Initialize()
        servicemanager.PrepareToHostSingle(AcmeDummyService)
        servicemanager.StartServiceCtrlDispatcher()
    else:
        win32serviceutil.HandleCommandLine(AcmeDummyService)


if __name__ == '__main__':
    main()
