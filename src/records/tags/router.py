from fastapi import APIRouter

from src.routers.base import BaseRouter
from src.models import Tag
from src.schemas import TagDTO, TagAddDTO


tags_router = APIRouter(
    prefix="/tags",
    tags=["tags"],
)

expense_router = BaseRouter(
    model=Tag,
    schema=TagDTO,
    create_schema=TagAddDTO,
    update_schema=TagAddDTO,
    prefix="/expense_tags",
    tags=["tags"],
    record_type_id=1,
).router

income_router = BaseRouter(
    model=Tag,
    schema=TagDTO,
    create_schema=TagAddDTO,
    update_schema=TagAddDTO,
    prefix="/income_tags",
    tags=["tags"],
    record_type_id=2,
).router

tags_router.include_router(expense_router)
tags_router.include_router(income_router)
