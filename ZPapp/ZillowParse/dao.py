# Отдельный файл для работы с БД // DAO → Data Access Object

from sqlalchemy import select, and_, insert

from ZPapp.database import async_session_maker # импортируем генератор сессий
from ZPapp.dao.base import BaseDAO # Базовый класс для работы с БД
from ZPapp.ZillowParse.models import Property

class PropertyDAO(BaseDAO):

    # Методы обращения к таблице
    model = Property # Задаем значение модели Property
    