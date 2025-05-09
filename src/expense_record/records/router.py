from typing import Annotated
from fastapi import APIRouter, Body, Depends, Query
from sqlalchemy import func, insert, select
from sqlalchemy.ext.asyncio import AsyncSession
from src.models import Record, User
from src.database.core.db import get_async_session

from .schemas import RecordDTO, RecordAddDTO
from src.auth.auth_config import fastapi_auth

records_router = APIRouter(
    prefix="/records",
    tags=["records"],
)


@records_router.get("/", response_model=list[RecordDTO])
async def get_records(
    limit: Annotated[int, Query(ge=1, le=100)] = 100,
    skip: Annotated[int, Query(ge=0, le=100)] = 0,
    session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(fastapi_auth.current_user()),
) -> list[RecordDTO]:

    records = []
    return records


@records_router.post("/")
async def add_record(
    new_record: Annotated[RecordAddDTO, Body()],
    session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(fastapi_auth.current_user()),
):

    db_record = new_record.model_dump()
    db_record["user_id"] = current_user.id

    statement = insert(Record).values(db_record)
    try:
        await session.execute(statement)
        await session.commit()
        return {"status": "ok"}
    except:
        session.rollback()
        return {"status": "nonono"}
