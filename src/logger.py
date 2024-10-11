import os
import sys
import logging

from const import LOGS_FOLDER, SESSION_START

def get_logger(name):
    """
    Get a logger with the given name
    """
    logger = logging.getLogger(name)
    ch = logging.StreamHandler()
    if os.environ.get("LOGFILE", None):
        filename = LOGS_FOLDER + os.environ["LOGFILE"] + "_" + SESSION_START + ".log"
        file = logging.FileHandler(filename)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(file)

    # console = logging.StreamHandler(stream=sys.stdout)
    # logger.addHandler(console)

    return logger