import io
import requests

from fastapi import APIRouter, Depends, Query, HTTPException

import config
from models import Passport, RecognitionResult
from security import check_api_key
from utils import decode_image_url, download_and_convert_to_bytesio
from vision.yandex_vision import YandexVision, YandexDecoder
from logger import logger

router = APIRouter()
yandex_oauth_token = config.YANDEX_OAUTH_TOKEN
yandex_folder_id = config.YANDEX_FOLDER_ID


@router.get("/recognize_the_passport/",
            response_model=RecognitionResult,
            summary="Распознать паспорт")
def recognize_the_passport(
    image: str = Query(..., description="URL-адрес изображения"),
    key: str = Query(..., description="Токен авторизации"),
    is_authorized: bool = Depends(check_api_key)
):
    if not is_authorized:
        logger.warning("Несанкционированный запрос")
        raise HTTPException(status_code=401, detail="Не авторизован")

    try:
        url: str = decode_image_url(image)
        file_bytes_io: io.BytesIO = download_and_convert_to_bytesio(url)
    except Exception as e:
        logger.error(f"Ошибка обработки изображения: {str(e)}")
        raise RecognitionResult(status="error", result=str(e))


    try:
        yandex_vision = YandexVision(
            oauth_token=yandex_oauth_token, folder_id=yandex_folder_id)
    except Exception as e:
        logger.error(f"Ошибка при создании экземпляра YandexVision: {str(e)}")
        raise RecognitionResult(status="error", result=str(e))

    try:
        recognize_yandex_data: requests.Response = yandex_vision.recognize_the_passport(
            file_bytes_io)
    except Exception as e:
        logger.error(f"Ошибка распознавания паспорта: {str(e)}")
        raise RecognitionResult(status="error", result=str(e))

    try:
        yandex_result_passport: Passport = YandexDecoder.expand_it_into_a_passport_model(
            recognize_yandex_data)
    except Exception as e:
        logger.error(f"Ошибка декодирования данных паспорта: {str(e)}")
        raise RecognitionResult(status="error", result=str(e))


    raise {"status": "ок", "result": yandex_result_passport}