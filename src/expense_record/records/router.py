from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Body, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.auth_config import fastapi_auth
from src.database.core.db import get_async_session
from src.database.database import delete_data, insert_data, select_data, update_data, upload_data
from src.models import Record, User, Tag, RecordTag

from .schemas import RecordAddDTO, RecordDTO

records_router = APIRouter(
    prefix="/records",
    tags=["records"],
)
current_user = fastapi_auth.current_user()


@records_router.get("/", response_model=list[RecordDTO])
async def get_records(
    limit: Annotated[int, Query(ge=1, le=100)] = 100,
    skip: Annotated[int, Query(ge=0, le=100)] = 0,
    session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(current_user),
) -> list[RecordDTO]:

    records = await select_data(session, Record, current_user.id, limit=limit, skip=skip)
    return [record.to_dto() for record in records]


@records_router.post("/", response_model=RecordDTO)
async def create_record(
    new_record: Annotated[RecordAddDTO, Body()],
    session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(current_user),
):
    try:
        tags = await select_data(session, Tag, current_user.id, filters=[Tag.id.in_(new_record.tags)])
        db_record = Record(user_id=current_user.id, tags=tags, **new_record.model_dump(exclude={"tags"}))
        await upload_data(session, db_record, ['tags', 'unit', 'category'])
        return db_record.to_dto()
    
    except Exception as e:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error creating record: {str(e)}",
        )


@records_router.patch("/{record_id}")
async def update_record(
    record_id: UUID,
    record_data: Annotated[RecordAddDTO, Body()],
    session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(current_user),
):
    record = await select_data(
        session,
        Record,
        current_user_uuid=current_user.id,
        filters=[Record.id == record_id],
        selectload=[Record.tags],
        check_user=True
    )
    
    
    if not record:
        raise HTTPException(status_code=404, detail="Record not found")
    record = record[0]
    
    update_data = record_data.model_dump(exclude={"tags"})
    for key, value in update_data.items():
        setattr(record, key, value)

    if record_data.tags is not None:
        current_tags = {tag.id for tag in record.tags}
        new_tags = set(record_data.tags)
        
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


@records_router.delete("/{record_id}", status_code=200)
async def delete_record(
    record_id: UUID,
    session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(current_user),
):
    filters = [Record.id == record_id, Record.user_id == current_user.id]
    deleted = await delete_data(session=session, model=Record, filters=filters)

    if not deleted:
        raise HTTPException(status_code=404, detail="Record not found")
    return {"id": str(record_id), "status": "deleted"}
