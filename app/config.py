from pydantic import model_validator
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
    
    SECRET_KEY: str
    ALGORITHM: str
    
    @model_validator(mode="after")
    def get_database_url(self):
        self.DATABASE_URL = (
            f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}?async_fallback=True"
        )
        return self
    
    class Config:
        env_file = ENV_FILE
    

settings = Settings()
