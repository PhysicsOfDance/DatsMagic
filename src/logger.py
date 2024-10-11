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
        file = logging.FileHandler(filename, encoding='utf-8')
        logger.addHandler(file)
    logger.setLevel(logging.DEBUG)

    # console = logging.StreamHandler(stream=sys.stdout)
    # logger.addHandler(console)
    return logger