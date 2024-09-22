from os import getenv
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()

DB_HOST = getenv('DB_HOST')
DB_PORT = getenv('DB_PORT')
DB_NAME = getenv('DB_NAME')
DB_USER = getenv('DB_USER')
DB_PASS = getenv('DB_PASS')


class Settings(BaseSettings):
    api_v1_prefix: str = '/api/v1'
    db_url: str = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    db_echo: bool = False


settings = Settings()
# print(settings.db_url)
