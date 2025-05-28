from fastapi import APIRouter

from src.auth.models import User
from src.routers.base import BaseRouter
from src.models import Category
from src.schemas import CategoryDTO, CategoryAddDTO


class ExpenseCategoryRouter(
    BaseRouter[Category, CategoryDTO, CategoryAddDTO, CategoryAddDTO]
):
    def __init__(self):
        super().__init__(
            model=Category,
            schema=CategoryDTO,
            create_schema=CategoryAddDTO,
            update_schema=CategoryAddDTO,
            prefix="/expense_categories",
            tags=["categories"],
            record_type_id=1,
        )


class IncomeCategoryRouter(
    BaseRouter[Category, CategoryDTO, CategoryAddDTO, CategoryAddDTO]
):
    def __init__(self):
        super().__init__(
            model=Category,
            schema=CategoryDTO,
            create_schema=CategoryAddDTO,
            update_schema=CategoryAddDTO,
            prefix="/income_categories",
            tags=["categories"],
            record_type_id=2,
        )


categories_router = APIRouter(
    prefix="/categories",
    tags=["categories"],
)

categories_router.include_router(ExpenseCategoryRouter().router)
categories_router.include_router(IncomeCategoryRouter().router)
