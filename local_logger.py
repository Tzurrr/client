import logging


def log_to_local_file(msg):
    logging.basicConfig(filename='logs.log', encoding='utf-8', level=logging.DEBUG)
    logging.warning(msg)

