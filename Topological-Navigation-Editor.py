import master
import logging
import time
import os

if __name__ == "__main__":

    if not os.path.exists('logs'):
        os.mkdir('logs')
    logger = logging.getLogger("Topological-Navigation-Editor")
    handler = logging.FileHandler('logs/{}.log'.format(time.strftime("%Y-%m-%d %H-%M-%S")))
    formatter = logging.Formatter("%(asctime)s %(levelname)s: %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    handler2 = logging.StreamHandler()
    handler2.setFormatter(formatter)
    logger.addHandler(handler2)
    logger.setLevel(logging.DEBUG)
    logger.info('{}'.format(time.asctime()))

    master.launch(logger)
