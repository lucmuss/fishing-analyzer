import logging


class CustomLogger():

    def __init__(self):
        pass

    def get_logger(self, log_arg):
        logger = logging.getLogger(log_arg)
        logger.setLevel(logging.INFO)

        handler = logging.FileHandler('data_processing.log')
        handler.setLevel(logging.INFO)

        formatter = logging.Formatter('%(levelname)s | %(asctime)s | %(filename)s | %(funcName)s | %(message)s',
                                      datefmt='%Y-%m-%dT%I:%M:%S')
        handler.setFormatter(formatter)

        logger.addHandler(handler)

        return logger
