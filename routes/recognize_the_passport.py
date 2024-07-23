import io
import requests

from fastapi import APIRouter, Depends, Query

import config
from models import Passport, RecognitionResult
from security import check_api_key
from utils import base64_to_bytesio, decode_image_url, download_image, convert_to_bytesio
from vision.yandex_vision import YandexVision, YandexDecoder
from logger import logger

router = APIRouter()
yandex_oauth_token = config.YANDEX_OAUTH_TOKEN
yandex_folder_id = config.YANDEX_FOLDER_ID


@router.get("/recognize_the_passport/",
            response_model=RecognitionResult,
            summary="Распознать паспорт")
def recognize_the_passport(
    image: str = Query(..., description="URL-адрес изображения или Base64"),
    key: str = Query(..., description="Токен авторизации"),
    is_authorized: bool = Depends(check_api_key)
):
    if not is_authorized:
        logger.warning("Не валидный токен авторизации")
        return RecognitionResult(status='error', result="Несанкционированный запрос")

    file_bytes_io = None

    if "base64" in image:
        image_base64 = image.split(",")[1]

        file_bytes_io = base64_to_bytesio(image_base64)
    else:
        try:
            url: str = decode_image_url(image)
        except Exception as e:
            logger.error(f"Не удалось получить ссылку на файл, или ссылка указана некорректно: {str(e)}")
            return RecognitionResult(
                status='error',
                result=f"Не удалось получить ссылку на файл, или ссылка указана некорректно: {str(e)}"
            )

        try:
            image: requests.Request = download_image(url)
        except Exception as e:
            logger.error(f"Ошибка при скачивании изображения: {str(e)}")
            return RecognitionResult(status='error', result=f"Ошибка обработки изображения: {str(e)}")

        try:
            file_bytes_io: io.IOBase = convert_to_bytesio(image)
        except Exception as e:
            logger.error(f"Ошибка конвертации в io.IOBase: {str(e)}")
            return RecognitionResult(status='error', result=f"Ошибка обработки изображения: {str(e)}")

    try:
        yandex_vision = YandexVision(
            oauth_token=yandex_oauth_token, folder_id=yandex_folder_id)
    except Exception as e:
        logger.error(f"Ошибка при создании экземпляра YandexVision: {str(e)}")
        return RecognitionResult(status='error', result=f"Ошибка при создании экземпляра YandexVision: {str(e)}")

    try:
        recognize_yandex_data: requests.Response = yandex_vision.recognize_the_passport(
            file_bytes_io)
    except Exception as e:
        logger.error(f"Ошибка распознавания паспорта: {str(e)}")
        return RecognitionResult(status='error', result=f"Ошибка распознавания паспорта: {str(e)}")

    try:
        yandex_result_passport: Passport = YandexDecoder.expand_it_into_a_passport_model(
            recognize_yandex_data)
    except Exception as e:
        logger.error(f"Ошибка декодирования данных паспорта: {str(e)}")
        return RecognitionResult(status='error', result=f"Ошибка декодирования данных паспорта: {str(e)}")

    return RecognitionResult(status='ok', result=yandex_result_passport)
