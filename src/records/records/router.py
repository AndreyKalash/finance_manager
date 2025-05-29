# router.py
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Body, Depends, HTTPException, Query
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.auth_config import fastapi_auth
from src.database.core.db import get_async_session
from src.database.crud import select_data
from src.models import Record, User, Tag

from .reports import generate_csv, generate_excel, generate_filename, generate_pdf
from src.routers.base import BaseRouter
from src.schemas import (
    ExpenseRecordDTO,
    ExpenseRecordAddDTO,
    IncomeRecordAddDTO,
    IncomeRecordDTO,
)


class RecordRouter(BaseRouter):
    def __init__(self, prefix, record_type_id, schema, create_schema):
        """
        Инициализация роутера для работы с записями.
        
        :param prefix: префикс URL для маршрутов
        :param record_type_id: тип записи (1 - расходы, 2 - доходы)
        :param schema: схема для сериализации данных
        :param create_schema: схема для валидации при создании
        """
        super().__init__(
            model=Record,
            schema=schema,
            create_schema=create_schema,
            update_schema=create_schema,
            prefix=prefix,
            tags=["records"],
            record_type_id=record_type_id,
        )
        # Добавление кастомного эндпоинта для экспорта
        self.router.add_api_route(
            '/export/',
            self.export_records,
            methods=["GET"],
            response_class=StreamingResponse
            )

    async def create_record(
        self, session: AsyncSession, data: BaseModel, current_user: User
    ):
        """
        Создание записи с привязкой тегов.
        
        :param session: асинхронная сессия БД
        :param data: валидированные данные записи
        :param current_user: текущий авторизованный пользователь
        """
        tags = await select_data(session, Tag, filters=[Tag.id.in_(data.tags)])
        kwargs = self.get_kwargs(current_user)
        kwargs["tags"] = tags
        return await self.create_base(
            session, data, kwargs, ["tags", "unit", "category"], ["tags"]
        )

    async def update_base(
        self, session: AsyncSession, current_user: User, data: BaseModel, item_id: UUID
    ):
        """
        Обновление записи с обработкой тегов.
        
        :param item_id: UUID обновляемой записи
        """
        filters = self.get_filters(current_user)
        filters.append(self.model.id == item_id)
        record = await self.get_base(
            session, filters, skip=0, limit=1, selectload_list=[self.model.tags]
        )
        if not record:
            raise HTTPException(status_code=404, detail="Record not found")
        record = record[0]
        # Обновление базовых полей
        update_data = data.model_dump(exclude={"tags"})
        for key, value in update_data.items():
            setattr(record, key, value)
        # Логика обновления тегов (синхронизация множеств)
        if data.tags is not None:
            current_tags = {tag.id for tag in record.tags}
            new_tags = set(data.tags)
            # Удаление отсутствующих тегов
            for tag_id in current_tags - new_tags:
                record.tags = [tag for tag in record.tags if tag.id != tag_id]
            # Добавление новых тегов
            existing_tag_ids = {tag.id for tag in record.tags}
            tags_to_add = [
                tag
                for tag_id in new_tags - existing_tag_ids
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
        current_user: User = Depends(fastapi_auth.current_user()),
    ):
        try:
            data = self.create_schema.model_validate(data)
            db_item = await self.create_record(session, data, current_user)
            return db_item
        except Exception as e:
            await session.rollback()
            raise HTTPException(400, detail=str(e))
        
    async def export_records(
        self,
        extension: Annotated[str, Query()],
        session: AsyncSession = Depends(get_async_session),
        current_user: User = Depends(fastapi_auth.current_user())
    ):
        """
        Экспорт записей в указанном формате.
        
        :param extension: формат файла (csv/xlsx/pdf)
        :return: StreamingResponse с файлом
        """
        filters = self.get_filters(current_user)
        items = await self.get_base(session, filters, no_limit=True)
        
        data = [item.to_dto().model_dump() for item in items]
        # Маппинг генераторов файлов
        file_generators = {
            'csv': (generate_csv, 'text/csv', 'data.csv'),
            'xlsx': (generate_excel, 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', 'data.xlsx'),
            'pdf': (generate_pdf, 'application/pdf', 'data.pdf')
        }

        if extension not in file_generators:
            raise HTTPException(status_code=400, detail="Unsupported file type")

        generator, media_type, filename = file_generators[extension]
        
        try:
            # Генерация файла в памяти
            buffer = await generator(data, self.record_type_id)
            filename = generate_filename(extension)
            # Настройка streaming ответа
            return StreamingResponse(
                buffer,
                media_type=media_type,
                headers={
                    'Content-Disposition': f'attachment; filename="{filename}"',
                    'Access-Control-Expose-Headers': 'Content-Disposition'
                }
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))


records_router = APIRouter(
    prefix="/records",
    tags=["records"],
)

expense_router = RecordRouter(
    prefix="/expense_records",
    record_type_id=1,
    schema=ExpenseRecordDTO,
    create_schema=ExpenseRecordAddDTO,
).router

income_router = RecordRouter(
    prefix="/income_records",
    record_type_id=2,
    schema=IncomeRecordDTO,
    create_schema=IncomeRecordAddDTO,
).router

records_router.include_router(expense_router)
records_router.include_router(income_router)
