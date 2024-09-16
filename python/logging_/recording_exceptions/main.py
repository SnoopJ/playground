import logging
import sys


logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


if __name__ == "__main__":
    logger.info("A regular old logging message")
    try:
        raise RuntimeError("A subsequent error") from ValueError("original cause")
    except:
        logging.exception("An error occurred (with exc_info)")
        logging.exception("An error occurred (without exc_info)", exc_info=False)
