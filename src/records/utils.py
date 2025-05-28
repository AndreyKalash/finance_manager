from src.database.core.db import Base
from sqlalchemy.ext.asyncio import AsyncSession
from src.models import User
from src.database.crud import delete_data, select_data, update_data, upload_data
from pydantic import BaseModel


async def get_items_common(
    session: AsyncSession,
    model: type[Base],
    current_user: User,
    record_type_id: int,
    limit: int,
    skip: int,
):
    filters = [model.record_type_id == record_type_id, model.user_id == current_user]
    items = await select_data(session, model, filters, limit=limit, skip=skip)
    return [item.to_dto() for item in items]


async def create_item_common(
    session: AsyncSession,
    model: type[Base],
    new_item: BaseModel,
    current_user: User,
    record_type_id: int,
):
    try:
        db_item = model(
            user_id=current_user.id,
            record_type_id=record_type_id,
            **new_item.model_dump()
        )
        await upload_data(session, db_item)
        return db_item.to_dto()
    except Exception as e:
        await session.rollback()
        raise e


async def update_item_common(
    session: AsyncSession,
    model: type[Base],
    current_user: User,
    new_item: BaseModel,
    item_id: int,
):
    try:
        filters = [
            model.id == item_id,
            model.user_id == current_user.id,
        ]

        updated_item = await update_data(session, model, new_item.model_dump(), filters)
        return updated_item.to_dto()

    except Exception as e:
        await session.rollback()
        raise e


async def delete_item_common(
    session: AsyncSession,
    model: type[Base],
    current_user: User,
    item_id,
):
    try:
        filters = [
            model.id == item_id,
            model.user_id == current_user.id,
        ]
        deleted = await delete_data(session=session, model=model, filters=filters)
        return deleted
    except Exception as e:
        await session.rollback()
        raise e
