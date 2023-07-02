from fastapi import APIRouter
from models import Status

router = APIRouter()

@router.get("/")
async def get_status():
    return Status()