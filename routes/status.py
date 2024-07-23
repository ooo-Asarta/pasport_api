from fastapi import APIRouter
from logger import logger

router = APIRouter()


@router.get("/")
async def get_status():
    logger.info('Запрос на получение статуса')
    return {'status': 'ок'}
