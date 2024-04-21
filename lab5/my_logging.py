import logging
import sys


def basic_conf(level=logging.DEBUG, output=sys.stdout) -> logging.Logger:
    handler = logging.StreamHandler(output)
    handler.setLevel(level)
    logger = logging.getLogger(__name__)
    logger.addHandler(handler)
    return logger
