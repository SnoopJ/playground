import logging

logger = logging.getLogger(__name__)

def func():
    logger.debug("This is a noisy log message from somelib.pkg, I want it filtered out")
