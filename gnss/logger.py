import logging

LOGLEVEL = logging.DEBUG
logger = logging.getLogger(__name__)
logger.setLevel(LOGLEVEL)
logger.addHandler(logging.StreamHandler())