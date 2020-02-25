import master
import logging
import time
import os
import sys


# exceptions handler


def execp_handler(type, value, tb):
    logger.exception("Exception: {}".format(value))


# Initiates the logger


if __name__ == "__main__":

    if not os.path.exists('logs'):
        os.mkdir('logs')
    logger = logging.getLogger("Topological-Navigation-Editor")
    # Creates a console log with timestamp
    handler = logging.FileHandler('logs/{}.log'.format(time.strftime("%Y-%m-%d %H-%M-%S")))
    formatter = logging.Formatter("%(asctime)s %(levelname)s: %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    handler2 = logging.StreamHandler()
    handler2.setFormatter(formatter)
    logger.addHandler(handler2)
    logger.setLevel(logging.DEBUG)
    logger.info('{}'.format(time.asctime()))

    sys.excepthook = execp_handler

    master.launch(logger)
