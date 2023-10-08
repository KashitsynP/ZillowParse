from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta
from pydantic import EmailStr

from ZPapp.config import settings
from ZPapp.users.dao import UsersDAO


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto") # переменная для создания алгоритма шифрования


# Пароли хранятся в базе в захэшируемом виде, чтобы при взломе базы злоумышленник не смог войти в систему
# Для этого 2 следующие функции ↓
def get_password_hash(password:str) -> str: 
    # Получаем пароль и возвращаем хэшированную версию
    # (функция из документации) Tutorial → Security → OAuth2 with Password (and hashing), Bearer with JWT tokens
    return pwd_context.hash(password) # возвращаем захэшированный пароль


def verify_password(plain_password, hashed_password) -> bool:
    # Для проверки пароля на соответствие захэшированной версии
    return pwd_context.verify(plain_password, hashed_password) # Возвращает True, если захэшированный пароль соответствует введенному пользователем


async def authentificate_user(email: EmailStr, password: str): # Аутентификация пользователя по паролю и email
    user = await UsersDAO.find_one_or_none(email=email) # найти одного юзера по email
    # SELECT * FROM users WHERE email = email
    if not user or not verify_password(password, user.hashed_password): # Если пользователя нет или пароли не совпадают
        return None
    return user # Если все нормально → возвращается пользователь


def create_access_token(data: dict) -> str: # Принимает словарь и возвращает JWT(str)
    to_encode = data.copy() # т.к. словарь это изменяемая структура данных, то нужно создать копию данных, чтобы в случае изменения они не поменялись везде
    expire = datetime.utcnow() + timedelta(minutes=180) # Задаем дату экспирации (дата истечения срока действия access токена)
    # текущее время в utc формате + 30 минут //
    # время, когда истечет токен доступа (есть ещё рефреш токен - долгосрочный)
    

    to_encode.update({'exp': expire}) # Добавляем значение в словарь
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, settings.ALGORITHM) # (что кодируем, секретный ключ, по какому алгоритму шифрования)
    return encoded_jwt # Возвращаем закодированный jwt-токен

