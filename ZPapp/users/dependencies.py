# Зависимости для проверки аутонтефицирован ли пользователь
from datetime import datetime

from fastapi import HTTPException, Request, Depends # Необходимо, чтобы распарсить информацию о токенах из запроса
from jose import jwt, JWTError

from ZPapp.config import settings

from ZPapp.users.dao import UsersDAO
from ZPapp.users.models import Users


def get_token(request: Request): # Получение cookies
    token = request.cookies.get('fitness_cookie') # Проверяем, есть ли такой ключ
    if not token: # Если такого токена нет, райзим ошибку 500
        raise HTTPException(status_code=500)
    return token # Возвращаем токен


async def get_current_user(token: str = Depends(get_token)): # Достаем user из cookies
    # Request в FastAPI существует только в рамках одного запроса, поэтому, необходимо использовать Depends, а не переменную (token = get_token)
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, settings.ALGORITHM) # раскодированный словарь
        # Декодируем наш JWT-токен
    except JWTError:
        raise HTTPException(status_code=500) # некорректный формат токена
    
    expire: str = payload.get('exp') # Получаем дату истечения
    if (not expire) or (int(expire) < datetime.utcnow().timestamp()):
        raise HTTPException(status_code=500) # Либо токен некорректный, либо дата эксперации истекла
    
    user_id: str = payload.get('sub') # Получаем id ползователя

    if not user_id:
        raise HTTPException(status_code=500)
    # print(user_id, type(user_id))

    
    user = await UsersDAO.find_by_id(int(user_id)) # Используем функцию для поиска юзера

    if not user:
        raise HTTPException(status_code=500)
    
    return user # Лучше создать отдельно метод, чтобы возвращать без пароля

    # 2) В куке содержится не абы какая строка, а JWT токен
    # 3) JWT токен все еще живой, дата экспирации не прошла
    # 4) В токене есть необходимые поля с данными пользователя
    # 5) Пользователь с таким id существует в БД
    # 6) Возвращение данных о пользователе: id, email, имя, фамилия и т.п.
