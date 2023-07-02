from fastapi import FastAPI
from routes import status, process_image

app = FastAPI()

app.include_router(status.router)
app.include_router(process_image.router)