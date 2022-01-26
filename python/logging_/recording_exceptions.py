import logging
import sys

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

if __name__ == "__main__":
    logger.info("A regular old logging message")
    try:
        raise RuntimeError("oh noes") from RuntimeError("original cause")
    except:
        logging.exception("An error occurred")
        logging.exception("An error occurred (exc_info suppressed)", exc_info=False)
