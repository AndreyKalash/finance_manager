from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Body, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.auth_config import fastapi_auth
from src.database.core.db import get_async_session
from src.database.database import delete_data, select_data, update_data, upload_data
from src.models import Unit, User

from .schemas import UnitAddDTO, UnitDTO

current_user = fastapi_auth.current_user()
units_router = APIRouter(
    prefix="/units",
    tags=["units"],
)


@units_router.get("/", response_model=list[UnitDTO])
async def get_units(
    session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(current_user),
    limit: Annotated[int, Query(ge=1, le=100)] = 100,
    skip: Annotated[int, Query(ge=0, le=100)] = 0,
) -> list[UnitDTO]:

    units = await select_data(session, Unit, current_user.id, limit, skip)
    return [unit.to_dto() for unit in units]


@units_router.post("/", response_model=UnitDTO)
async def create_unit(
    new_unit: Annotated[UnitAddDTO, Body()],
    session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(current_user),
) -> UnitDTO:
    try:
        db_unit = Unit(user_id=current_user.id, **new_unit.model_dump())
        await upload_data(session, db_unit)
        return db_unit.to_dto()
    except Exception as e:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error creating unit: {str(e)}",
        )


@units_router.patch("/{unit_id}", response_model=UnitDTO)
async def update_unit(
    unit_id: UUID,
    unit_data: Annotated[UnitAddDTO, Body()],
    session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(current_user),
) -> UnitDTO:
    filters = [
        Unit.id == unit_id,
        Unit.user_id == current_user.id,
    ]

    updated_unit = await update_data(session, Unit, unit_data.model_dump(), filters)

    if not updated_unit:
        raise HTTPException(status_code=404, detail="Unit not found")

    return updated_unit.to_dto()


@units_router.delete("/{unit_id}", status_code=200)
async def delete_unit(
    unit_id: UUID,
    session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(current_user),
):
    filters = [Unit.id == unit_id, Unit.user_id == current_user.id]
    deleted = await delete_data(session=session, model=Unit, filters=filters)

    if not deleted:
        raise HTTPException(status_code=404, detail="Unit not found")
    return {"id": str(unit_id), "status": "deleted"}
