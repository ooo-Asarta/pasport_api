import os
from dotenv import load_dotenv
import sys

load_dotenv()


SECURITY_KEY = os.getenv('SECURITY_KEY')
YANDEX_FOLDER_ID = os.getenv('YANDEX_FOLDER_ID')
YANDEX_OAUTH_TOKEN = os.getenv('YANDEX_OAUTH_TOKEN')
#VK_OAUTH_TOKEN = os.getenv('VK_OAUTH_TOKEN')

if not SECURITY_KEY:
    logger.error('SECURITY_KEY is not set in the environment')
    sys.exit(1)

if not YANDEX_FOLDER_ID:
    logger.error('YANDEX_FOLDER_ID is not set in the environment')
    sys.exit(1)

if not YANDEX_OAUTH_TOKEN:
    logger.error('YANDEX_OAUTH_TOKEN is not set in the environment')
    sys.exit(1)

#if not VK_OAUTH_TOKEN:
#    logger.error('VK_OAUTH_TOKEN is not set in the environment')
#    sys.exit(1)