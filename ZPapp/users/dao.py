# Отдельный файл для работы с БД // DAO → Data Access Object

from sqlalchemy import select, and_

from ZPapp.database import async_session_maker # импортируем генератор сессий
from ZPapp.dao.base import BaseDAO # Базовый класс для работы с БД
# from app.users.models import Users

from ZPapp.users.models import Users


class UsersDAO(BaseDAO):

    # Методы обращения к таблице
    model = Users # Задаем значение модели Users


    # Метод для обращение к БД для поиска всех дел у пользователя
    # @classmethod
    # async def get_todo(cls, user_id: int):
        # SELECT users."id" AS users.id, users."name", users.email, todos."id" AS todos.id, todos.text, todos.date_start, todos.date_stop, todos.success
        # FROM users
        # JOIN todos ON users."id" == todos."owners"
        # WHERE ...

        # async with async_session_maker() as session: # В асинхронном режиме открываем сессию для запроса к БД
        #     query = (
        #         select(
        #             Users.id,
        #             Users.name,
        #             Users.email,

        #             Todos.id,
        #             Todos.text,
        #             Todos.date_start,
        #             Todos.date_stop,
        #             Todos.success,
        #         ).join(Todos, Users.id == Todos.owner)
        #     .where(and_(Todos.date_start < Todos.date_stop, Users.id == user_id))
                    # )
            
            # query = (
            #     select(
            #         Users.id,
            #         Users.name,
            #         Users.email,

            #         Todos.id,
            #         Todos.text,
            #         Todos.date_start,
            #         Todos.date_stop,
            #         Todos.success,
            #     ).select_from(Users).join(Todos, Users.id == Todos.owner)
            #     .where(and_(Todos.date_start < Todos.date_stop, Users.id == user_id))
            #         )
                # → для того, чтобы выбрать только выбранного по id user`а и дела, у которых дата начала меньше даты окончания
                # WHERE (Todos.date_start < Todos.date_stop) AND (Users.id == user_id)
            
            # result = await session.execute(query) # Исполнить запрос к БД
            # return result.mappings().all() # Возвращает пользователя и все дела, соответствующие данному пользователю по условию
            
            
            # select(cls.model).filter_by(id=model_id)
            # # ищем конкретный id-шник (в каждой таблице у нас есть поле id)
            # # SELECT * FROM table_name WHERE id = 'model_id'
            # result = await session.execute(query)
            # return result.scalar_one_or_none() # возвращает либо одну строку либо ничего (специальный метод алхимии)
