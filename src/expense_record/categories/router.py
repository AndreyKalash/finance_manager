from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Body, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.auth_config import fastapi_auth
from src.database.core.db import get_async_session
from src.database.database import delete_data, select_data, update_data, upload_data
from src.models import Category, User

from .schemas import CategoryAddDTO, CategoryDTO

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

    categories = await select_data(session, Category, current_user.id, limit=limit, skip=skip)
    return [category.to_dto() for category in categories]


@categories_router.post("/", response_model=CategoryDTO)
async def create_category(
    new_category: Annotated[CategoryAddDTO, Body()],
    session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(current_user),
):
    try:
        db_category = Category(user_id=current_user.id, **new_category.model_dump())
        await upload_data(session, db_category)
        return db_category.to_dto()
    except Exception as e:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error creating category: {str(e)}",
        )


@categories_router.patch("/{category_id}")
async def update_category(
    category_id: UUID,
    category_data: Annotated[CategoryAddDTO, Body()],
    session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(current_user),
):
    filters = [
        Category.id == category_id,
        Category.user_id == current_user.id,
    ]

    updated_category = await update_data(
        session, Category, category_data.model_dump(), filters
    )

    if not updated_category:
        raise HTTPException(status_code=404, detail="Category not found")

    return updated_category.to_dto()


@categories_router.delete("/{category_id}", status_code=200)
async def delete_category(
    category_id: UUID,
    session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(current_user),
):
    filters = [Category.id == category_id, Category.user_id == current_user.id]
    deleted = await delete_data(session=session, model=Category, filters=filters)

    if not deleted:
        raise HTTPException(status_code=404, detail="Category not found")
    return {"id": str(category_id), "status": "deleted"}
