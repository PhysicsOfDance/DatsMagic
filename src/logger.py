import os
import sys
import logging

def get_logger(name):
    """
    Get a logger with the given name
    """
    logger = logging.getLogger(name)
    ch = logging.StreamHandler()
    if os.environ.get("LOGFILE", None):
        filename = os.environ["LOGFILE"] 
        file = logging.FileHandler(filename)

    console = logging.StreamHandler(stream=sys.stdout)

    logger.setLevel(logging.DEBUG)
    logger.addHandler(file)
    logger.addHandler(console)

    return logger