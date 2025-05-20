from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Body, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.auth_config import fastapi_auth
from src.database.core.db import get_async_session
from src.database.crud import select_data
from src.models import Record, User, Tag

from src.routers.base import BaseRouter
from src.schemas import ExpenseRecordDTO, ExpenseRecordAddDTO, IncomeRecordAddDTO, IncomeRecordDTO

class RecordRouter(BaseRouter):
    def __init__(self, prefix, record_type_id, schema, create_schema):
        super().__init__(
            model=Record,
            schema=schema,
            create_schema=create_schema,
            update_schema=create_schema,
            prefix=prefix,
            tags=['records'],
            record_type_id=record_type_id
        )
        
    async def create_record(self, session:AsyncSession, data:BaseModel, current_user:User):
        tags = await select_data(session, Tag, filters=[Tag.id.in_(data.tags)])
        kwargs = self.get_kwargs(current_user)
        kwargs['tags'] = tags
        return await self.create_base(session, data, kwargs, ['tags', 'unit', 'category'], ['tags'])
    
    async def update_base(self, session:AsyncSession, current_user:User, data:BaseModel, item_id:UUID):
        filters = self.get_filters(current_user)
        filters.append(self.model.id==item_id)
        record = await self.get_base(
            session,
            filters,
            skip=0,
            limit=1,
            selectload_list=[self.model.tags]
        )
        if not record:
            raise HTTPException(status_code=404, detail="Record not found")
        record = record[0]
        
        update_data = data.model_dump(exclude={"tags"})
        for key, value in update_data.items():
            setattr(record, key, value)

        if data.tags is not None:
            current_tags = {tag.id for tag in record.tags}
            new_tags = set(data.tags)
            
            for tag_id in current_tags - new_tags:
                record.tags = [tag for tag in record.tags if tag.id != tag_id]
            
            existing_tag_ids = {tag.id for tag in record.tags}
            tags_to_add = [
                tag for tag_id in new_tags - existing_tag_ids 
                if (tag := await session.get(Tag, tag_id))
            ]
            record.tags.extend(tags_to_add)

        await session.commit()
        await session.refresh(record)
        
        return record.to_dto()
    
    async def create(
        self,
        data: dict = Body(),
        session: AsyncSession = Depends(get_async_session),
        current_user: User = Depends(fastapi_auth.current_user())
    ):
        try:
            data = self.create_schema.model_validate(data)
            db_item = await self.create_record(session, data, current_user)
            return db_item
        except Exception as e:
            await session.rollback()
            raise HTTPException(400, detail=str(e))
        
records_router = APIRouter(
    prefix="/records",
    tags=["records"],
)

expense_router = RecordRouter(
    prefix="/expense_records",
    record_type_id=1,
    schema=ExpenseRecordDTO,
    create_schema=ExpenseRecordAddDTO
).router

income_router = RecordRouter(
    prefix="/income_records",
    record_type_id=2,
    schema=IncomeRecordDTO,
    create_schema=IncomeRecordAddDTO
).router

records_router.include_router(expense_router)
records_router.include_router(income_router)