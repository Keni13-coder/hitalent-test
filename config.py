import os, sys
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict
from loguru import logger


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra='ignore')
    
    MODE: Literal['test', 'dev', 'prod'] = 'test'
    ALLOWED_HOSTS : list[str] = ['localhost:3000']
    POSTGRESQL_URL: str
    REDIS_URL: str
    
    @property
    def redis_url(self):
        return f'redis://{self.REDIS_URL}'
    
    @property
    def postgres_url(self):
        return f'postgresql+asyncpg://{self.POSTGRESQL_URL}{"_test" if self.MODE == "test" else ""}'

def init_logger():     
    logger.add(
        sink=sys.stdout,
        level="DEBUG",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {name}:{function}:{line} - {message}",
        )
        
    logger.add(
        sink=os.path.join("logs", "app_{time:YYYY-MM-DD}.log"),
        rotation="1 day",
        retention="7 days",
        level="INFO",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {name}:{function}:{line} - {message}",
    )

    logger.add(
        sink=os.path.join("logs", "errors_{time:YYYY-MM-DD}.log"),
        level="ERROR",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {name}:{function}:{line} - {message}",
        rotation="1 day"
    )
    

settings = Settings()
init_logger()