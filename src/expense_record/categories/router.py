from typing import Annotated
from uuid import UUID
from fastapi import APIRouter, Body, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from src.models import Category, User
from src.database.core.db import get_async_session

from .schemas import CategoryDTO, CategoryAddDTO
from src.auth.auth_config import fastapi_auth
from src.database.database import (
    select_data,
    insert_user_data,
    delete_user_data,
    update_user_data,
)


current_user = fastapi_auth.current_user()
categories_router = APIRouter(
    prefix="/categories",
    tags=["categories"],
)


@categories_router.get("/", response_model=list[CategoryDTO])
async def get_categories(
    session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(current_user),
    limit: Annotated[int, Query(ge=1, le=100)] = 100,
    skip: Annotated[int, Query(ge=0, le=100)] = 0,
) -> list[CategoryDTO]:

    categories = await select_data(session, Category, current_user.id, limit, skip)
    # categories_dto = [
    #     CategoryDTO.model_validate(row, from_attributes=True) for row in categories_orm
    # ]
    return categories


@categories_router.post("/")
async def post_category(
    new_category: Annotated[CategoryAddDTO, Body()],
    session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(current_user),
):
    db_category = new_category.model_dump()
    db_category["user_id"] = current_user.id

    is_added = await insert_user_data(session, Category, db_category)

    resp_info = {}
    if is_added:
        resp_info.update(status="ok")
    else:
        resp_info.update(status="nono")

    return resp_info


@categories_router.patch("/{category_id}")
async def update_category(
    category_id: UUID,
    updated_category: Annotated[CategoryAddDTO, Body()],
    session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(current_user),
):
    db_category = updated_category.model_dump()
    filter_conditions = [
        Category.id == category_id,
        Category.user_id == current_user.id,
    ]

    is_added = await update_user_data(session, Category, db_category, filter_conditions)

    resp_info = {}
    if is_added:
        resp_info.update(status="ok")
    else:
        resp_info.update(status="nono")

    return resp_info


@categories_router.delete("/")
async def delete_category(
    category_name: Annotated[CategoryDTO, Body()],
    session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(current_user),
):
    filter_conditions = [
        Category.name == category_name.name,
        Category.user_id == current_user.id,
    ]
    is_deleted = await delete_user_data(session, Category, filter_conditions)

    resp_info = {}
    if is_deleted:
        resp_info.update(status="ok")
    else:
        resp_info.update(status="nono")

    return resp_info
