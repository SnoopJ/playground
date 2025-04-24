import logging

logger = logging.getLogger(__name__)

try:
    import somelib

    # NOTE: if other imports or configuration (e.g. tweaking library loggers) is necessary, I do that here as well

    SOMELIB_AVAILABLE = True
except ImportError as exc:
    logger.warning("somelib is not available, functionality will be degraded")
    # NOTE: I find it helpful to issue a warning and *also* store the exception details in a higher logging level. YMMV.
    logger.debug("Exception details:", exc_info=exc)

    SOMELIB_AVAILABLE = False
