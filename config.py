import os
from dotenv import load_dotenv
import sys

from logger import logger

load_dotenv()


SECURITY_KEY = os.getenv('SECURITY_KEY')
YANDEX_FOLDER_ID = os.getenv('YANDEX_FOLDER_ID')
YANDEX_OAUTH_TOKEN = os.getenv('YANDEX_OAUTH_TOKEN')


if not SECURITY_KEY:
    logger.error('SECURITY_KEY не задан в переменных окружения')
    sys.exit(1)

if not YANDEX_FOLDER_ID:
    logger.error('YANDEX_FOLDER_ID не задан в переменных окружения')
    sys.exit(1)

if not YANDEX_OAUTH_TOKEN:
    logger.error('YANDEX_OAUTH_TOKEN не задан в переменных окружения')
    sys.exit(1)
