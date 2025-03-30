from typing import Annotated
from fastapi import APIRouter, Body, Depends
from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession
from src.models import Tag, User
from src.database.core.db import get_async_session
from src.database.database import select_data, insert_user_data, delete_user_data

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
) -> list[TagDTO]:

    fields = [Tag.name, Tag.color]
    filter_conditions = [Tag.user_id == current_user.id]
    tags = await select_data(session, fields, filter_conditions)

    return tags


@tags_router.post("/")
async def post_tags(
    new_tag: Annotated[TagDTO, Body()],
    session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(current_user),
):
    db_tag = new_tag.model_dump()
    db_tag["user_id"] = current_user.id
    is_added = await insert_user_data(session, Tag, db_tag)

    resp_info = {}
    if is_added:
        resp_info.update(status="ok")
    else:
        resp_info.update(status="nono")

    return resp_info


@tags_router.delete("/")
async def delete_category(
    tag_name: Annotated[TagDTO, Body()],
    session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(current_user),
):
    filter_conditions = [Tag.name == tag_name.name, Tag.user_id == current_user.id]
    is_deleted = await delete_user_data(session, Tag, filter_conditions)

    resp_info = {}
    if is_deleted:
        resp_info.update(status="ok")
    else:
        resp_info.update(status="nono")

    return resp_info
