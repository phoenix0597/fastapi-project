from pydantic_settings import BaseSettings
from os.path import abspath, dirname, join

# Определяем путь к файлу .env
BASE_DIR = dirname(dirname(abspath(__file__)))
ENV_FILE = join(BASE_DIR, ".env")


class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_NAME: str
    DB_PASS: str
    DATABASE_URL: str = ""
    
    class Config:
        env_file = ENV_FILE


settings = Settings()
settings.DATABASE_URL = \
    f"postgresql+asyncpg://{settings.DB_USER}:{settings.DB_PASS}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}?async_fallback=True"

print(settings.DATABASE_URL)