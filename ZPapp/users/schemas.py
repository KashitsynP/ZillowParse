# pydantic схемы → отвечает за валидацию

# from datetime import date
from typing import List, Optional
from enum import Enum
from pydantic import BaseModel, EmailStr


class RoleChoise(str, Enum):
    admin = 'admin'
    user = 'user'
    superuser = 'superuser'


class Users(BaseModel): # Создаем схему модели Users, с помощью pydantic
    id: int
    name: Optional[str]
    role: RoleChoise
    email: EmailStr
    password: str

    class Config: # Нужно, чтобы pydantic распознал схему алхимии
        # // смотри на нашу модель не только как на словарь, но и как на класс, у которого есть атрибуты
        orm_mode = True


class SUserAuth(BaseModel): # Создаем отдельный класс SUserAuth с минимальными параметрами для авторизации
    email: EmailStr
    password: str
    # role: RoleChoise

    class Config: # Нужно, чтобы pydantic распознал схему алхимии
        orm_mode = True



    # info: List[Info] # Валидируем через другой класс List[Info] - список объектов Info



