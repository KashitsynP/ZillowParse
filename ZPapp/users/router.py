from fastapi import APIRouter, Response, Query # Response - ответ, который мы отправим серверу
from pydantic import EmailStr

from ZPapp.users.schemas import Users, SUserAuth
from ZPapp.users.dao import UsersDAO
from ZPapp.users.auth import get_password_hash, create_access_token, authentificate_user, verify_password
from ZPapp.users.dependencies import Depends, get_current_user


router = APIRouter(
    prefix='/users', # данный префикс будет перед всеми эндпоинтами
    tags=['Пользователи'] # название этого роутера для объединения роутеров в группу в документации
)

@router.post('/register') # Роутер для регистрации пользователя
async def registration(user_data: SUserAuth, role: str = Query('user', enum=['user', 'admin', 'superuser'])): # Функция регистрации пользователей
    existing_user = await UsersDAO.find_one_or_none(email=user_data.email)
    if existing_user: # Если юзер уже существует, то сообщаем об этом
        return {'message': 'Пользователь уже существует!'}
    
    existing_superuser = await UsersDAO.find_one_or_none(role='superuser') # Обращаемся к БД, смотрим есть ли у нас superuser

    if existing_superuser and role == 'superuser': # если суперпользователь уже существует
        return {'суперпользователь существует в одном единственном экземпляре!'}
    # raise UserAlreadyExistsException # Если по данному email уже есть регистрация, то будет 500 ошибка
    hashed_password = get_password_hash(user_data.password) # Хэшируем пароль
    await UsersDAO.add(email=user_data.email, hashed_password=hashed_password, role=role) # Добавляем пользователя в БД
    return {'message': 'success'} # сообщение в случае успешной регистрации



@router.post('/login') # Роутер для аутентификации пользователя
async def login(response: Response, user_data: SUserAuth):
    user = await authentificate_user(email=user_data.email, password=user_data.password) # проверяем юзера, если ок → присваиваем в переменную
    
    if not user:
        return {'message': 'Такого пользователя нет'}

    data = {'sub': str(user.id)} # Создаем словарь с id юзера
    token = create_access_token(data) # Создаем токен

    response.set_cookie('fitness_cookie', token, httponly=True, secure=True) # На основании созданного токена создаем куки
    # Засетим cookie // Для того, чтобы мы в дальнейшем могли пользоваться защищенными эндпоинтами
    # название, токен, важный параметр безопасности (httponly - чтобы через JS нельзя было подделать), чтобы токен нельзя было воспроизвести через JS
    # secure=True - чтобы можно было взаимодействовать только через протокол https
    return {'message': 'success'} # Возвращаем ответ клиенту в свагере


@router.get('/me') # Пользователь получает информацию о себе
async def read_users_me(current_user: Users = Depends(get_current_user)):
    # т.к. есть Depends - всё проходит по циклу зависимостей
    return {'user': current_user.id, 'role': current_user.role} # Возвращаем словарь, состоящий из данных о юзере


@router.get('/all_users') # Показать всех пользователей, доступно только суперпользователю
async def read_all_users(current_user: Users = Depends(get_current_user)):
    if current_user.role != 'superuser':
        return {'Такое доступно только для суперпользователя!'}
    users = await UsersDAO.find_all()
    return {'users': users}


# @router.get('get_todos/') # Получение списка дел у данного пользователя. (нужно залогинится сперва)
# async def get_todos(current_user: Users = Depends(get_current_user)): # Обращаемся к текущему пользователю
#     todos = await UsersDAO.get_todo(user_id=current_user.id) # Берем его id и передаем в функцию
#     return todos # Возвращаем список дел текущего пользователя


@router.post('/logout') # Разлогиниться (выйти из системы)
async def logout_user(response: Response): # Получаем ответ от сервера
    response.delete_cookie('fitness_cookie') # Из полученного ответа удаляем заданные куки
    return {'message': 'logout was successfull'} # Возвращаем ответ клиенту в свагере



@router.patch('/change_password') # Смена пароля пользователя
async def change_pass(old_password: str, 
                      new_password: str, 
                      current_user: Users = Depends(get_current_user)):
    if not verify_password(old_password, current_user.hashed_password) :
        return None
    new_password_hash = get_password_hash(new_password)

    await UsersDAO.data_update(id=current_user.id, hashed_password=new_password_hash) # Обновляем данные с новым паролем

    return {'message': 'password was successfully changed'}


@router.patch('/change_role') # Поменять роль. Доступно только для superuser
async def change_role(id:int, role: str = Query('user', enum=['user', 'admin']), current_user: Users = Depends(get_current_user)):  
    if current_user.role != 'superuser':
        return {'message': 'Отказано в доступе! Ваша роль должна быть superuser!'}
    await UsersDAO.data_update(id=id, role=role) # Обновляем данные с новой ролью пользователя
    return {'message': 'success', 'Новая роль': role}


@router.delete('/delete_user') # Удалить пользователя. Доступно только для admin и superuser
async def delete_user(user_id:int, current_user: Users = Depends(get_current_user)):
    if (current_user.role != 'superuser' and current_user.role != 'admin'):
        return {'message': 'Отказано в доступе! Ваша роль должна быть не ниже admin!'}
    
    user = await UsersDAO.find_one_or_none(id=user_id) # Находим юзера по id
    if not user:  # Если польователь по id не найден
        return {'message': 'Пользователя с таким id не существует!'}
    
    await UsersDAO.delete(id=user_id) # Удаляем пользователя
    return {'message': 'Пользователь удалён'}

    
