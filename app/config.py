from typing import Literal

from pydantic import model_validator, ConfigDict
from pydantic_settings import BaseSettings
from os.path import abspath, dirname, join

# Определяем путь к файлу .env
BASE_DIR = dirname(dirname(abspath(__file__)))
ENV_FILE = join(BASE_DIR, ".env")


class Settings(BaseSettings):
    MODE: Literal["DEV", "TEST", "PROD"]

    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_NAME: str
    DB_PASS: str
    DATABASE_URL: str = ""

    @model_validator(mode="after")
    def get_database_url(self):
        self.DATABASE_URL = (
            f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}"
            # f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}?async_fallback=True"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )
        return self


    TEST_DB_HOST: str
    TEST_DB_PORT: int
    TEST_DB_USER: str
    TEST_DB_NAME: str
    TEST_DB_PASS: str
    TEST_DATABASE_URL: str = ""


    @model_validator(mode="after")
    def get_test_database_url(self):
        self.TEST_DATABASE_URL = (
            f"postgresql+asyncpg://{self.TEST_DB_USER}:{self.TEST_DB_PASS}"
            # f"@{self.TEST_DB_HOST}:{self.TEST_DB_PORT}/{self.TEST_DB_NAME}?async_fallback=True"
            f"@{self.TEST_DB_HOST}:{self.TEST_DB_PORT}/{self.TEST_DB_NAME}"
        )
        return self


    SECRET_KEY: str

    ALGORITHM: str
    SMTP_HOST: str
    SMTP_PORT: int
    SMTP_USER: str

    SMTP_PASS: str
    REDIS_HOST: str


    REDIS_PORT: int

    # class Config:
    #     env_file = ENV_FILE
    model_config = ConfigDict(env_file=ENV_FILE)


settings = Settings()
