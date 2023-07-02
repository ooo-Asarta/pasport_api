from fastapi import APIRouter, Depends, Query
from models import Status, ProcessImageRequest
from security import check_api_key
from utils import decode_image_url, download_and_convert_to_bytesio
from vision.yandex_vision import YandexVision
from fastapi.encoders import jsonable_encoder
#from vision.vk_vision import VkVision
router = APIRouter()
oauth_token = ''
folder_id = ''

@router.get("/process_image/")
async def process_image(image: str = Query(..., description="URL-адрес изображения"), is_authorized: bool = Depends(check_api_key)):
    if not is_authorized:
        return {"error": "Unauthorized"}

    try:
        url = decode_image_url(image)
        file_bytes_io = download_and_convert_to_bytesio(url)
        yandex_vision = YandexVision(oauth_token=oauth_token, folder_id=folder_id)
        yandex_result_pasport = await yandex_vision.precognize_passport(file_bytes_io)
        
        passport_json = jsonable_encoder(yandex_result_pasport)
    except Exception as e:
        print(f"Error: {str(e)}")
    
    # Здесь вы можете добавить логику для обработки изображения
    # Например, можно выполнить анализ изображения, применить модель машинного обучения и т.д.
    
    # Возвращаем статус

    return passport_json