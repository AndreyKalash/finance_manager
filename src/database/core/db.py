from sqlalchemy import UpdateBase
from sqlalchemy.orm import DeclarativeBase
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from src.config import DATABASE_URL


engine = create_async_engine(DATABASE_URL)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)

class Base(DeclarativeBase):
    repr_col_num = 3
    repr_extra_cols = tuple()

    def __repr__(self) -> str:
        cols = []
        for i, col in enumerate(self.__table__.columns.keys()):
            if col in self.repr_extra_cols or i < self.repr_col_num:
                cols.append(f"{col}={getattr(self, col)}")

        return f"<{self.__class__.__table__.__name__}: {', '.join(cols)}>"


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


async def execute_statement(session: AsyncSession, statement: UpdateBase) -> bool:
    try:
        await session.execute(statement)
        await session.commit()
        return True
    except Exception as ex:
        print(ex)
        await session.rollback()
        return False
