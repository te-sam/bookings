from typing import Literal
from pydantic import ConfigDict
from pydantic_settings import BaseSettings
from secrets import token_bytes
from base64 import b64encode

class Settings(BaseSettings):
    MODE: Literal['DEV', 'TEST', 'PROD']

    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    TEST_DB_HOST: str
    TEST_DB_PORT: int
    TEST_DB_USER: str
    TEST_DB_PASS: str
    TEST_DB_NAME: str    

    ALGORITM: str
    SECRET_KEY: str

    REDIS_HOST: str
    REDIS_PORT: int

    SMTP_HOST: str
    SMTP_PORT: int
    SMTP_USER: str
    SMTP_PASS: str
  
    # class Config:
    #     env_file = ".env"
    model_config = ConfigDict(env_file=".env")

settings = Settings()