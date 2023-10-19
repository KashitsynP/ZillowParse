from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from ZPapp.users.router import router as user_router
from ZPapp.ZillowParse.router import router as ZP_router

app = FastAPI()

app.include_router(user_router) # Подключаем маршруты пользователей
app.include_router(ZP_router) # Подключаем маршруты парсера

app.mount("/static", StaticFiles(directory="ZPapp/static"), name="static")

origins = [
    "http://localhost",
    "https://localhost:8000",
    ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)
