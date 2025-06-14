# base.py
from typing import Generic, List, Optional, Type, TypeVar, Dict, Any
from uuid import UUID
from fastapi import APIRouter, Body, Depends, HTTPException, Query, Path, Response
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel, create_model
from src.database.core.db import Base, get_async_session
from src.models import User
from src.auth.auth_config import fastapi_auth
from src.database.crud import delete_data, select_data, update_data, upload_data
# Объявление дженерик-типов для гибкой работы с разными моделями и схемами
ModelType = TypeVar("ModelType", bound=Base)
SchemaType = TypeVar("SchemaType", bound=BaseModel)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class BaseRouter(Generic[ModelType, SchemaType, CreateSchemaType, UpdateSchemaType]):
    def __init__(
        self,
        model: Type[ModelType],
        schema: Type[SchemaType],
        create_schema: Type[CreateSchemaType],
        update_schema: Type[UpdateSchemaType],
        prefix: str = "",
        tags: List[str] = None,
        record_type_id: Optional[int] = None,
        get_all_route: bool = True,
        create_route: bool = True,
        update_route: bool = True,
        delete_route: bool = True,
        custom_dependencies: Dict[str, List[Depends]] = None,
        custom_responses: Dict[str, Dict[int, Dict[str, Any]]] = None,
        description: str = "",
        order_by = None
    ):
        """
        Базовый роутер для CRUD операций.
        
        :param model: SQLAlchemy модель
        :param schema: Pydantic схема для ответов
        :param create_schema: Схема для создания записей
        :param update_schema: Схема для обновления записей
        :param prefix: Префикс URL пути
        :param tags: Теги для документации Swagger
        :param record_type_id: Идентификатор типа записи для фильтрации
        :param get_all_route: Флаг создания эндпоинта для получения всех записей
        :param create_route: Флаг создания эндпоинта для создания записи
        :param update_route: Флаг создания эндпоинта для обновления
        :param delete_route: Флаг создания эндпоинта для удаления
        :param custom_dependencies: Кастомные зависимости для маршрутов
        :param custom_responses: Кастомные HTTP ответы
        :param description: Описание для документации
        """
        self.router = APIRouter(prefix=prefix, tags=tags or [])
        self.model = model
        self.schema = schema
        self.record_type_id = record_type_id

        self.create_schema = create_schema
        self.update_schema = update_schema
        
        self.order_by = order_by.desc() if order_by else self.model.created_at.desc()

        self.dependencies = self._setup_dependencies(custom_dependencies)
        self.responses = self._setup_responses(custom_responses)

        self._setup_routes(
            get_all_route,
            create_route,
            update_route,
            delete_route,
            description,
        )

    def _generate_update_schema(self) -> Type[BaseModel]:
        """Генерация схемы для обновления с необязательными полями"""
        fields = {}
        for name, field_info in self.create_schema.__annotations__.items():
            if name not in ["id", "created_at", "updated_at"]:
                fields[name] = (Optional[field_info], None)

        return create_model(
            f"{self.create_schema.__name__}Update", __base__=BaseModel, **fields
        )

    def _setup_dependencies(self, custom_deps: Dict = None) -> Dict:
        """Инициализация зависимостей для маршрутов"""
        deps = {
            "get_all": [],
            "get_one": [],
            "create": [],
            "update": [],
            "delete": [],
        }

        if custom_deps:
            for route, route_deps in custom_deps.items():
                if route in deps:
                    deps[route].extend(route_deps)

        return deps

    def _setup_responses(self, custom_responses: Dict = None) -> Dict:
        """Настройка HTTP ответов для документации"""
        responses = {
            "get_all": {404: {"description": "Элементы не найдены"}},
            "get_one": {404: {"description": "Элемент не найден"}},
            "create": {400: {"description": "Ошибка в запросе"}},
            "update": {
                404: {"description": "Элемент не найден"},
                400: {"description": "Ошибка в запросе"},
            },
            "delete": {404: {"description": "Элемент не найден"}},
        }

        if custom_responses:
            for route, resps in custom_responses.items():
                if route in responses:
                    responses[route].update(resps)

        return responses

    def _setup_routes(
        self,
        get_all: bool,
        create: bool,
        update: bool,
        delete: bool,
        description: str,
    ):
        """Создание стандартных CRUD маршрутов"""
        model_name = description or self.model.__name__

        if get_all:
            self.router.add_api_route(
                "/",
                self.get_all,
                methods=["GET"],
                response_model=List[self.schema],
                dependencies=self.dependencies["get_all"],
                responses=self.responses["get_all"],
                summary=f"Получить все записи {model_name}",
                description=f"Получить список всех {model_name} с пагинацией и фильтрацией",
            )

        if create:
            self.router.add_api_route(
                "/",
                self.create,
                methods=["POST"],
                response_model=self.schema,
                dependencies=self.dependencies["create"],
                responses=self.responses["create"],
                status_code=201,
                summary=f"Создать {model_name}",
                description=f"Создать новую запись {model_name}",
            )

        if update:
            self.router.add_api_route(
                "/{item_id}",
                self.update,
                methods=["PATCH"],
                response_model=self.schema,
                dependencies=self.dependencies["update"],
                responses=self.responses["update"],
                summary=f"Обновить {model_name}",
                description=f"Обновить существующую запись {model_name}",
            )

        if delete:
            self.router.add_api_route(
                "/{item_id}",
                self.delete,
                methods=["DELETE"],
                dependencies=self.dependencies["delete"],
                responses=self.responses["delete"],
                status_code=204,
                response_class=Response,
                summary=f"Удалить {model_name}",
                description=f"Удалить запись {model_name} по ID",
            )

    def get_filters(self, current_user: User) -> List:
        """Формирование базовых фильтров для запросов"""
        filters = []
        # Фильтр по типу записи (для разделения расходов/доходов)
        if self.record_type_id is not None:
            filters.append(self.model.record_type_id == self.record_type_id)

        if hasattr(self.model, "user_id"):
            filters.append(self.model.user_id == current_user.id)

        return filters

    def get_kwargs(self, current_user: User) -> Dict[str, Any]:
        """Получение дополнительных параметров для создания записи"""
        kwargs = {}

        if hasattr(self.model, "user_id"):
            kwargs["user_id"] = current_user.id

        if self.record_type_id is not None:
            kwargs["record_type_id"] = self.record_type_id

        return kwargs

    async def get_base(
        self,
        session: AsyncSession,
        filters: List,
        limit: int = 100,
        skip: int = 0,
        selectload_list: List = [],
        no_limit: bool = False
    ) -> List[ModelType]:
        """
        Базовый метод для получения записей из БД с фильтрацией и пагинацией.
        
        :param session: Асинхронная сессия SQLAlchemy
        :param filters: Список фильтров SQLAlchemy
        :param limit: Максимальное количество записей (по умолчанию 100)
        :param skip: Смещение в выборке (для пагинации)
        :param selectload_list: Список отношений для eager loading
        :param no_limit: Флаг отключения лимита выборки
        :return: Список объектов модели
        """
        return await select_data(
            session,
            self.model,
            filters,
            limit=limit,
            skip=skip,
            selectload=selectload_list,
            no_limit=no_limit,
            order_by=self.order_by
        )

    async def create_base(
        self,
        session: AsyncSession,
        data: CreateSchemaType,
        kwargs: dict,
        names: List = None,
        exclude: list = [],
    ) -> ModelType:
        """
        Базовый метод создания записи с обработкой связей.
        
        :param data: Валидированные данные из схемы создания
        :param kwargs: Дополнительные параметры для модели
        :param names: Список имен отношений для обработки
        :param exclude: Поля для исключения при создании
        :return: Созданный объект модели
        """
        db_item = self.model(**data.model_dump(exclude=[*exclude]), **kwargs)
        await upload_data(session, db_item, names or [])
        return db_item

    async def update_base(
        self,
        session: AsyncSession,
        current_user: User,
        data: UpdateSchemaType,
        item_id: UUID,
    ):
        """
        Базовый метод обновления записи с проверкой прав доступа.
        
        :param data: Частичные данные для обновления
        :param item_id: UUID обновляемой записи
        :return: Обновленный объект модели
        """
        filters = self.get_filters(current_user)
        filters.append(self.model.id == item_id)

        return await update_data(
            session, self.model, data.model_dump(exclude_unset=True), filters
        )

    async def delete_base(
        self, session: AsyncSession, current_user: User, item_id: UUID
    ) -> bool:
        """
        Базовый метод удаления записи с проверкой прав доступа.
        
        :param item_id: UUID удаляемой записи
        :return: Флаг успешного удаления
        """
        filters = self.get_filters(current_user)
        filters.append(self.model.id == item_id)

        return await delete_data(session, self.model, filters)

    async def get_all(
        self,
        session: AsyncSession = Depends(get_async_session),
        current_user: User = Depends(fastapi_auth.current_user()),
        limit: int = Query(
            100, ge=1, le=100, description="Максимальное количество записей"
        ),
        skip: int = Query(0, ge=0, description="Смещение от начала выборки"),
    ) -> List[SchemaType]:
        """
        Обработчик GET-запроса для получения списка записей.
        
        :param limit: Лимит записей (1-100)
        :param skip: Смещение для пагинации
        :return: Список DTO объектов
        """
        filters = self.get_filters(current_user)

        items = await self.get_base(session, filters=filters, limit=limit, skip=skip)
        return [item.to_dto() for item in items]

    async def get_one(
        self,
        item_id: UUID = Path(..., description="Идентификатор записи"),
        session: AsyncSession = Depends(get_async_session),
        current_user: User = Depends(fastapi_auth.current_user()),
    ) -> SchemaType:
        """
        Обработчик GET-запроса для получения одной записи.
        
        :param item_id: UUID записи
        :return: DTO объект
        """
        filters = self.get_filters(current_user)
        filters.append(self.model.id == item_id)

        items = await self.get_base(session, filters, limit=1)
        if not items:
            raise HTTPException(404, detail="Item not found")

        return items[0].to_dto()

    async def create(
        self,
        data: dict = Body(),
        session: AsyncSession = Depends(get_async_session),
        current_user: User = Depends(fastapi_auth.current_user()),
    ) -> SchemaType:
        """
        Обработчик POST-запроса для создания записи.
        
        :param data: Тело запроса в формате JSON
        :return: Созданный DTO объект
        """
        try:
            data = self.update_schema.model_validate(data)
            db_item = await self.create_base(
                session, data, self.get_kwargs(current_user)
            )
            return db_item.to_dto()
        except Exception as e:
            await session.rollback()
            raise HTTPException(400, detail=str(e))

    async def update(
        self,
        item_id: UUID,
        data: dict = Body(),
        session: AsyncSession = Depends(get_async_session),
        current_user: User = Depends(fastapi_auth.current_user()),
    ) -> SchemaType:
        """
        Обработчик PATCH-запроса для обновления записи.
        
        :param item_id: UUID обновляемой записи
        :param data: Частичные данные для обновления
        :return: Обновленный DTO объект
        """
        data = self.update_schema.model_validate(data)
        updated_item = await self.update_base(session, current_user, data, item_id)
        if not updated_item:
            raise HTTPException(404, detail="Item not found")

        return updated_item

    async def delete(
        self,
        item_id: UUID,
        session: AsyncSession = Depends(get_async_session),
        current_user: User = Depends(fastapi_auth.current_user()),
    ) -> None:
        """
        Обработчик DELETE-запроса для удаления записи.
        
        :param item_id: UUID удаляемой записи
        :return: HTTP 204 No Content при успехе
        """
        if not await self.delete_base(session, current_user, item_id):
            raise HTTPException(404, detail="Item not found")
