from fastapi import FastAPI
from routes import recognize_the_passport, status




app = FastAPI()

app.include_router(status.router)
app.include_router(recognize_the_passport.router)
