import logging
import sys

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

info_handler = logging.StreamHandler(stream=sys.stdout)
info_handler.setLevel(logging.INFO)

error_handler = logging.StreamHandler(stream=sys.stderr)
error_handler.setLevel(logging.ERROR)

info_formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
error_formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')

info_handler.setFormatter(info_formatter)
error_handler.setFormatter(error_formatter)

logger.addHandler(info_handler)
logger.addHandler(error_handler)