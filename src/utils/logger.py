import logging

from sys import stdout


def get_logger_instance(name=__name__):
    logger = logging.getLogger(name)
    logging.basicConfig(
        level=logging.INFO,
        format="[%(asctime)s %(filename)s:%(lineno)d] %(levelname)s - %(message)s",
        handlers=[
            logging.StreamHandler(stdout),
        ],
    )
    return logger
