from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from src.config import DATABASE_URL

engine = create_async_engine(DATABASE_URL)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


class Base(DeclarativeBase):

    def __repr__(self) -> str:
        cols = []
        for i, col in enumerate(self.__table__.columns.keys()):
            cols.append(f"{col}={getattr(self, col)}")

        return f"<{self.__class__.__table__}: {', '.join(cols)}>"


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session
