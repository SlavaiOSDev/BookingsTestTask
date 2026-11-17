import os
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
import contextlib
from collections.abc import AsyncIterator
from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "fastapi_db")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASS = os.getenv("DB_PASSWORD", "secret123")

DATABASE_URL = (
    f"postgresql+asyncpg://"
    f"{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

engine = create_async_engine(DATABASE_URL)

Session = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
)

@contextlib.asynccontextmanager
async def transaction() -> AsyncIterator[AsyncSession]:
    async with Session() as session:
        async with session.begin():
            yield session