import logging
from .config import AcmeConfig
from .logging_init import _initialize_logging, DelayedLoggerAdapter


def main(use_custom_logger: bool = False):
    logger = logging.getLogger(__name__)
    if use_custom_logger:
        _base_logger = logger
        logger = DelayedLoggerAdapter(_base_logger)

    if use_custom_logger:
        logger.info(
            "This logger has no handlers at call time, "
            "but the message will be deferred until there are some",
        )
    else:
        logger.info(
            "This logger has no handlers at call time, "
            "this message will not be visible"
        )

    config = AcmeConfig()
    _initialize_logging(config)

    if use_custom_logger:
        logger.delayed = False

    logger.info("Hello after configuration")
