from ZPapp.database import async_session_maker, engine
from sqlalchemy import select, insert, delete, update

# Data Access Object (DAO)
# Вершиной иерархии DAO является абстрактный класс или интерфейс с описанием общих методов, которые будут использоваться при взаимодействии с базой данных. Как правило, это методы поиска, удаление по ключу, обновление и т.д.

class BaseDAO: # Создаём класс BaseDAO, в котором прописываем методы для выполнения запросов к БД
    model = None  # Модель по умолчанию = None

    # В случае, когда функция обращается к стороннему серверу (в данном случае к БД), методы должны быть асинхронными (async, 
    # async with → в случае открытия сессии, для того, чтобы в случае ошибки, сессия была в любом случае закрыта)

    # Метод поиска в БД по id
    @classmethod
    async def find_by_id(cls, model_id: int):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(id=model_id)
            # ищем конкретный id-шник (в каждой таблице у нас есть поле id)
            # SELECT * FROM table_name WHERE id = 'model_id'
            result = await session.execute(query) # Испольнить запрос
            return result.scalar_one_or_none() # возвращает либо один объект либо ничего (специальный метод алхимии)
        
    # Метод поиска в БД по фильтрам (найти одну строку или ничего)
    @classmethod
    async def find_one_or_none(cls, **filter_by):
        #Проверяем, зарегистрирован ли пользователь
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(**filter_by)
            # SELECT * FROM models WHERE **filter
            result = await session.execute(query) # Исполнить запрос
            return result.scalar_one_or_none() # возвращает либо один объект либо ничего (специальный метод алхимии)
        
    # Метод поиска в БД по фильтрам (найти все строки, соответствующие фильтру)
    @classmethod
    async def find_all(cls, **filter_by):
        async with async_session_maker() as session: # используем асинхронный контекстный менеджер
            # если произойдёт ошибка - сессия закроется
            query = select(cls.model).filter_by(**filter_by)

            result = await session.execute(query) # исполняем запрос и получим // <sqlalchemy.engine.result.ChunkedIteratorResult object at 0x7f242a738a40>
            return result.scalars().all() # Вернет уже JSON, т.к. FastAPI всегда пытается конвертировать ответ в JSON

    # Метод добавления в БД. Параметром указан словарь
    @classmethod
    async def add(cls, **data): # Добавление чего-то
        async with async_session_maker() as session:  # используем асинхронный контекстный менеджер
            query = insert(cls.model).values(**data) #.returning(cls.model.id) # INSERT INTO VALUES  /// return id
            await session.execute(query)  # Исполняем наш запрос и получим // <sqlalchemy.engine.result.ChunkedIteratorResult object at 0x7f242a738a40>
            await session.commit() # Закоммитить изменения. Если изменения в БД, то обязательно коммитить

    # Метод для удаления из БД по фильтрам
    @classmethod
    async def delete(cls, **filter_by): # удаление чего-то
        async with async_session_maker() as session: # используем асинхронный контекстный менеджер
            query = delete(cls.model).filter_by(**filter_by)
            print(query.compile(engine, compile_kwargs={'literal_binds': True})) # чтобы увидеть сырой запрос
            # DELETE FROM ... FROM ... AND ... == ...
            # compile - скомпилируй, engine - наш движок, compile_kwargs - необходимые аргументы для компиляции

            await session.execute(query) # исполняем запрос
            await session.commit() # фиксируем все изменения


    @classmethod
    async def find_all_for_param(cls, **filter_by):
        async with async_session_maker() as session: # используем асинхронный контекстный менеджер
            # если произойдёт ошибка - сессия закроется
            query = select(cls.model).filter_by(**filter_by)

            result = await session.execute(query) # исполняем запрос и получим // <sqlalchemy.engine.result.ChunkedIteratorResult object at 0x7f242a738a40>
            return result.scalars().all() # Вернет уже JSON, т.к. FastAPI всегда пытается конвертировать ответ в JSON


    @classmethod
    async def delete_for_param(cls, **filter_by): # удаление чего-то
        async with async_session_maker() as session: # используем асинхронный контекстный менеджер
            query = delete(cls.model).filter_by(**filter_by)
            print(query.compile(engine, compile_kwargs={'literal_binds': True})) # чтобы увидеть сырой запрос
            # DELETE FROM ... FROM ... AND ... == ...
            # compile - скомпилируй, engine - наш движок, compile_kwargs - необходимые аргументы для компиляции

            await session.execute(query) # исполняем запрос
            await session.commit() # фиксируем все изменения

    @classmethod
    async def data_update(cls, id, **kwargs): # Изменение данных
        async with async_session_maker() as session:
            query = update(cls.model).where(cls.model.id == id).values(**kwargs)
            await session.execute(query) # исполняем запрос
            await session.commit() # фиксируем все изменения