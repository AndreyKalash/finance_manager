from typing import Annotated
from fastapi import APIRouter, Body, Depends
from sqlalchemy import and_, delete, insert, select
from sqlalchemy.ext.asyncio import AsyncSession
from src.models import Unit, User
from src.database.core.db import get_async_session

from .schemas import UnitAddDTO
from src.auth.auth_config import fastapi_auth

current_user = fastapi_auth.current_user()
units_router = APIRouter(
    prefix="/units",
    tags=["units"],
)

@units_router.get("/", response_model=list[UnitAddDTO])
async def get_units(
    session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(current_user),
) -> list[UnitAddDTO]:
    query = select(Unit.unit_name).where(Unit.user_id == current_user.id)
    result = await session.execute(query)
    units = result.mappings().all()
    return units


@units_router.post("/", response_model=dict)
async def post_unit(
    new_unit: Annotated[UnitAddDTO, Body()],
    session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(current_user),
):
    db_unit = new_unit.model_dump()
    db_unit["user_id"] = current_user.id

    statement = insert(Unit).values(db_unit)
    try:
        await session.execute(statement)
        await session.commit()
        return {"status": "ok"}
    except:
        session.rollback()
        return {"status": "nonono"}


@units_router.delete("/")
async def delete_category(
    del_unit_name: Annotated[str, Body()],
    session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(current_user),
):
    statement = delete(Unit).where(
        and_(Unit.name == del_unit_name, Unit.user_id == current_user.id)
    )
    try:
        await session.execute(statement)
        await session.commit()
        return {"status": "ok"}
    except Exception as ex:
        print(ex)
        await session.rollback()
        return {"status": "nonono"}
