from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from ZPapp.config import settings


engine = create_async_engine(settings.DATABASE_URL) # Подключение к БД // точка входа SQLalchemy в наше приложение

async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


class Base(DeclarativeBase): # Объявляем класс Base, наследуем от DeclarativeBase из sqlalchemy.orm
    pass



