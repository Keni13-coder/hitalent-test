from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import (
    async_sessionmaker,
    create_async_engine,
)

from config import settings


class Base(DeclarativeBase):
    pass


if settings.MODE.lower() == "test":
    DATABASE_PARAMS = {"poolclass": NullPool}
else:
    DATABASE_PARAMS = {
        'isolation_level': "REPEATABLE READ",
    }

DATABASE_URL = settings.postgres_url

engine = create_async_engine(
    DATABASE_URL,
    **DATABASE_PARAMS,
)

async_session_maker = async_sessionmaker(engine, expire_on_commit=False)