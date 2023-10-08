# pydantic схемы → отвечает за валидацию

# from datetime import date
from typing import Optional
from enum import Enum
from pydantic import BaseModel
from ZPapp.users.schemas import Users


class Property(BaseModel): # Создаем схему модели Pets, с помощью pydantic

    address: str
    country: str
    listingStatus: str
    zpid: str
    price: float
    livingArea: int
    bedrooms: int
    bathrooms: int

    class Config: # Нужно, чтобы pydantic распознал схему алхимии
        # // смотри на нашу модель не только как на словарь, но и как на класс, у которого есть атрибуты
        orm_mode = True
