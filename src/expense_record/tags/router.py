from typing import Annotated
from uuid import UUID
from fastapi import APIRouter, Body, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from src.models import Tag, User
from src.database.core.db import get_async_session
from src.database.database import select_data, update_data, upload_data, delete_data

from .schemas import TagDTO, TagAddDTO
from src.auth.auth_config import fastapi_auth


current_user = fastapi_auth.current_user()
tags_router = APIRouter(
    prefix="/tags",
    tags=["tags"],
)


@tags_router.get("/", response_model=list[TagDTO])
async def get_tags(
    session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(current_user),
    limit: Annotated[int, Query(ge=1, le=100)] = 100,
    skip: Annotated[int, Query(ge=0, le=100)] = 0,
) -> list[TagDTO]:
    tags = await select_data(session, Tag, current_user.id)
    return [tag.to_dto() for tag in tags]


@tags_router.post("/", response_model=TagDTO)
async def create_tag(
    new_tag: Annotated[TagAddDTO, Body()],
    session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(current_user),
):
    try:
        db_tag = Tag(user_id=current_user.id, **new_tag.model_dump())
        await upload_data(session, db_tag)
        return db_tag.to_dto()
    except Exception as e:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error creating tag: {str(e)}",
        )


@tags_router.patch("/{tag_id}")
async def update_tag(
    tag_id: UUID,
    tag_data: Annotated[TagAddDTO, Body()],
    session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(current_user),
):
    filters = [
        Tag.id == tag_id,
        Tag.user_id == current_user.id,
    ]

    updated_tag = await update_data(session, Tag, tag_data.model_dump(), filters)

    if not updated_tag:
        raise HTTPException(status_code=404, detail="Tag not found")

    return updated_tag.to_dto()


@tags_router.delete("/{tag_id}", status_code=200)
async def delete_tag(
    tag_id: UUID,
    session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(current_user),
):
    filters = [Tag.id == tag_id, Tag.user_id == current_user.id]
    deleted = await delete_data(session=session, model=Tag, filters=filters)

    if not deleted:
        raise HTTPException(status_code=404, detail="Tag not found")
    return {"id": str(tag_id), "status": "deleted"}
