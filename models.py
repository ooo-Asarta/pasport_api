from pydantic import BaseModel

class Status(BaseModel):
    status: str = "ok"

class ProcessImageRequest(BaseModel):
    image: str