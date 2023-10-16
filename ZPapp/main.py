import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from ZPapp.users.router import router as user_router
from ZPapp.ZillowParse.router import router as ZP_router

app = FastAPI()

app.include_router(user_router) # Подключаем маршруты пользователей
app.include_router(ZP_router) # Подключаем маршруты парсера


# static_dir = os.path.join(os.path.dirname(__file__), "static")
app.mount("/", StaticFiles(directory="ZPapp/static"), name="static")
