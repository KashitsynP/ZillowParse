from sqlalchemy import Date, Column, Integer, String, JSON, SMALLINT, ForeignKey, Computed
from sqlalchemy.orm import relationship
from ZPapp.database import Base
# from app.users.schemas import RoleChoise

class Users(Base): # На основе класса Base, создаем модель (таблицу) Users
    __tablename__ = 'users' # название таблицы

    id = Column(Integer, primary_key=True, nullable=False) # (id = Колонка(число, первичный ключ, NotNull))
    name = Column(String) # имя = Колонка(строка, возможен бузымянный пользователь)
    role = Column(String, default='user')
    email = Column(String, nullable=False) # email = Колонка(строка, NotNull)
    hashed_password = Column(String, nullable=False) # захэшированный пароль = Колонка(строка, NotNull)
    # pets = relationship('Pets', back_populates='users') # Подписываемся на таблицу Pets

    