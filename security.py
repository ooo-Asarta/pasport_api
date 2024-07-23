from fastapi.security import APIKeyQuery
from config import SECURITY_KEY
from fastapi import Depends
from logger import logger


api_key_query = APIKeyQuery(name='key', auto_error=False)


def check_api_key(api_key: str = Depends(api_key_query)):
    logger.info(f"{api_key=}")
    # Здесь вы можете добавить логику проверки ключа доступа
    # Например, проверить его наличие в базе данных или хранилище ключей

    # Возвращаем True, если ключ совпадает или False в противном случае
    return api_key in SECURITY_KEY
