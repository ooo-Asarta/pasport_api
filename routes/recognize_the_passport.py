import io
import requests

from fastapi import APIRouter, Depends, Query, HTTPException

import config
from models import Passport
from security import check_api_key
from utils import decode_image_url, download_and_convert_to_bytesio
from vision.yandex_vision import YandexVision, YandexDecoder

router = APIRouter()
yandex_oauth_token = config.YANDEX_OAUTH_TOKEN
yandex_folder_id = config.YANDEX_FOLDER_ID


@router.get("/recognize_the_passport/",
            response_model=Passport,
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
        raise HTTPException(status_code=400, detail=f"Ошибка: {str(e)}")

    try:
        yandex_vision = YandexVision(
            oauth_token=yandex_oauth_token, folder_id=yandex_folder_id)
    except Exception as e:
        logger.error(f"Ошибка при создании экземпляра YandexVision: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Ошибка: {str(e)}")

    try:
        recognize_yandex_data: requests.Response = yandex_vision.recognize_the_passport(
            file_bytes_io)
    except Exception as e:
        logger.error(f"Ошибка распознавания паспорта: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Ошибка: {str(e)}")

    try:
        yandex_result_passport: Passport = YandexDecoder.expand_it_into_a_passport_model(
            recognize_yandex_data)
    except Exception as e:
        logger.error(f"Ошибка декодирования данных паспорта: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Ошибка: {str(e)}")

    return yandex_result_passport
