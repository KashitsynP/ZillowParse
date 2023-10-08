# Здесь храним все данные о подключениях к различным БД, почтам и т.д.

from pydantic_settings import BaseSettings

class Settings(BaseSettings):

# Чтобы не светить персональными данными, создаём такую модель для подключения:
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    SECRET_KEY: str # JWT # bash: openssl rand -base64 32
    ALGORITHM: str  # JWT

# А все персональные данные храним в файле .env в корне приложения
    class Config:
        env_file = '.env'

    @property
    def DATABASE_URL(self): # Прописываем свойства для подключения к БД postgreSQL
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
    
settings = Settings()