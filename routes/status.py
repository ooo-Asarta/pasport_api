from fastapi import APIRouter


router = APIRouter()

@router.get("/")
async def get_status():
    logger.info('Запрос на получение статуса')
    return {'status': 'ок'}