import logging
import sys
from logging.handlers import RotatingFileHandler

LOG_LEVEL = logging.INFO
formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s")

# Console handler
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(formatter)

# File handler with rotation
file_handler = RotatingFileHandler("app.log", maxBytes=10 * 1024 * 1024, backupCount=5)
file_handler.setFormatter(formatter)


def get_logger(name: str):
    logger = logging.getLogger(name)
    if not logger.handlers:
        logger.setLevel(LOG_LEVEL)
        logger.addHandler(console_handler)
        logger.addHandler(file_handler)
    return logger
