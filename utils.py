import requests
import io
import urllib
import base64

from logger import logger


def download_image(url: str) -> requests.Response:
    """
    Скачивает файл по указанному URL и преобразует его в объект io.BytesIO.

    Аргументы:
        url (str): URL файла для загрузки.

    Возвращает:
        io.BytesIO: Скачанный файл в виде объекта io.BytesIO.

    Исключения:
        Exception: Если файл не удается загрузить или происходит ошибка.
    """
    try:
        response = requests.get(
            url,
            verify=False,
            stream=True
        )
        response.raise_for_status()  # Проверка статуса ответа

        return response

    except requests.exceptions.RequestException as e:
        logger.error(f"Не удалось загрузить файл: {str(e)}")
        raise Exception(f"Не удалось загрузить файл: {str(e)}")


def convert_to_bytesio(response: requests.Response) -> io.BytesIO:
    try:
        file_bytes = io.BytesIO(response.content)
        return file_bytes
    except Exception as e:
        logger.error(f"Произошла ошибка: {str(e)}")
        raise Exception(f"Произошла ошибка: {str(e)}")


def decode_image_url(url: str) -> str:
    """
    Декодирует URL-кодированный URL изображения.

    Аргументы:
        url (str): Декодируемый URL.

    Возвращает:
        str: Декодированный URL.

    Исключения:
        Exception: Если происходит ошибка при декодировании URL.
    """
    try:
        decoded_url = urllib.parse.unquote(url)
        return decoded_url
    except Exception as e:
        logger.error(f"Ошибка при декодировании URL изображения: {str(e)}")
        raise Exception(f"Ошибка при декодировании URL изображения: {str(e)}")


def base64_to_bytesio(base64_data: str):
    image_data = base64_data.encode()
    image_bytes = base64.b64decode(image_data)

    return io.BytesIO(image_bytes)
