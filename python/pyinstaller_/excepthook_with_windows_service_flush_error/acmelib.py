from itertools import count
import logging
import logging.handlers
from pathlib import Path
import time


HERE = Path(__file__).parent.resolve()
LOGFILE = HERE.joinpath("acmelib.log")


logging.basicConfig(
    level=logging.DEBUG,
    handlers=[
        logging.handlers.TimedRotatingFileHandler(str(LOGFILE), when="D", utc=True, encoding="UTF8"),
    ],
)

logger = logging.getLogger(__name__)

def main():
    logger.info("acmelib.main() beginning")
    for num in range(5):
        logger.info("acmelib.main() looping (iteration #%d)", num)
        time.sleep(0.25)

    raise RuntimeError("An error inside my library")
