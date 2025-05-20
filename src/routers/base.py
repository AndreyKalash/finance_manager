from typing import Annotated, Generic, List, Optional, Type, TypeVar, Dict, Any
from uuid import UUID
from fastapi import APIRouter, Body, Depends, HTTPException, Query, Path, Response
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel, create_model
from src.database.core.db import Base, get_async_session
from src.models import User
from src.auth.auth_config import fastapi_auth
from src.database.crud import delete_data, select_data, update_data, upload_data

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
        get_one_route: bool = True,
        create_route: bool = True,
        update_route: bool = True,
        delete_route: bool = True,
        custom_dependencies: Dict[str, List[Depends]] = None,
        custom_responses: Dict[str, Dict[int, Dict[str, Any]]] = None,
        description: str = "",
    ):
        self.router = APIRouter(prefix=prefix, tags=tags or [])
        self.model = model
        self.schema = schema
        self.record_type_id = record_type_id
        
        self.create_schema = create_schema
        self.update_schema = update_schema
        
        self.dependencies = self._setup_dependencies(custom_dependencies)
        self.responses = self._setup_responses(custom_responses)
        
        self._setup_routes(
            get_all_route, 
            get_one_route, 
            create_route, 
            update_route, 
            delete_route, 
            description
        )

    def _generate_update_schema(self) -> Type[BaseModel]:
        fields = {}
        for name, field_info in self.create_schema.__annotations__.items():
            if name not in ["id", "created_at", "updated_at"]:
                fields[name] = (Optional[field_info], None)
        
        return create_model(
            f"{self.create_schema.__name__}Update",
            __base__=BaseModel,
            **fields
        )

    def _setup_dependencies(self, custom_deps: Dict = None) -> Dict:
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
        responses = {
            "get_all": {404: {"description": "Элементы не найдены"}},
            "get_one": {404: {"description": "Элемент не найден"}},
            "create": {400: {"description": "Ошибка в запросе"}},
            "update": {
                404: {"description": "Элемент не найден"}, 
                400: {"description": "Ошибка в запросе"}
            },
            "delete": {404: {"description": "Элемент не найден"}},
        }
        
        if custom_responses:
            for route, resps in custom_responses.items():
                if route in responses:
                    responses[route].update(resps)
                    
        return responses
    
    def _setup_routes(self, get_all: bool, get_one: bool, create: bool, 
                     update: bool, delete: bool, description: str):
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
                description=f"Получить список всех {model_name} с пагинацией и фильтрацией"
            )
            
        if get_one:
            self.router.add_api_route(
                "/{item_id}",
                self.get_one,
                methods=["GET"],
                response_model=self.schema,
                dependencies=self.dependencies["get_one"],
                responses=self.responses["get_one"],
                summary=f"Получить {model_name} по ID",
                description=f"Получить конкретный {model_name} по ID"
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
                description=f"Создать новую запись {model_name}"
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
                description=f"Обновить существующую запись {model_name}"
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
                description=f"Удалить запись {model_name} по ID"
            )

    def get_filters(self, current_user: User) -> List:
        filters = []
        
        if self.record_type_id is not None:
            filters.append(self.model.record_type_id == self.record_type_id)
            
        if hasattr(self.model, "user_id"):
            filters.append(self.model.user_id == current_user.id)
            
        return filters
    
    def get_kwargs(self, current_user: User) -> Dict[str, Any]:
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
    ) -> List[ModelType]:
        return await select_data(
            session, 
            self.model, 
            filters, 
            limit=limit, 
            skip=skip, 
            selectload=selectload_list
        )
    
    async def create_base(
        self,
        session: AsyncSession,
        data: CreateSchemaType,
        kwargs: dict,
        names: List = None,
        exclude: list = []
    ) -> ModelType:
        db_item = self.model(**data.model_dump(exclude=[*exclude]), **kwargs)
        await upload_data(session, db_item, names or [])
        return db_item

    async def update_base(
        self,
        session: AsyncSession,
        current_user: User,
        data: UpdateSchemaType,
        item_id: UUID
    ):
        filters = self.get_filters(current_user)
        filters.append(self.model.id == item_id)
    
        return await update_data(
            session, 
            self.model, 
            data.model_dump(exclude_unset=True), 
            filters
        )


    async def delete_base(
        self,
        session: AsyncSession,
        current_user: User,
        item_id: UUID
    ) -> bool:
        filters = self.get_filters(current_user)
        filters.append(self.model.id == item_id)
        
        return await delete_data(session, self.model, filters)

    async def get_all(
        self,
        session: AsyncSession = Depends(get_async_session),
        current_user: User = Depends(fastapi_auth.current_user()),
        limit: int = Query(100, ge=1, le=100, description="Максимальное количество записей"),
        skip: int = Query(0, ge=0, description="Смещение от начала выборки"),
    ) -> List[SchemaType]:
        filters = self.get_filters(current_user)
        
        items = await self.get_base(
            session, filters=filters, limit=limit, skip=skip
        )
        
        return [item.to_dto() for item in items]

    def _parse_order_by(self, order_by: Optional[str]) -> List:
        order_list = []
        if order_by:
            for field in order_by.split(','):
                field = field.strip()
                if not field:
                    continue
                    
                if field.startswith('-') and hasattr(self.model, field[1:]):
                    order_list.append(getattr(self.model, field[1:]).desc())
                elif hasattr(self.model, field):
                    order_list.append(getattr(self.model, field).asc())
                    
        return order_list

    async def get_one(
        self,
        item_id: UUID = Path(..., description="Идентификатор записи"),
        session: AsyncSession = Depends(get_async_session),
        current_user: User = Depends(fastapi_auth.current_user())
    ) -> SchemaType:
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
        current_user: User = Depends(fastapi_auth.current_user())
    ) -> SchemaType:
        try:
            data = self.update_schema.model_validate(data)
            db_item = await self.create_base(session, data, self.get_kwargs(current_user))
            return db_item.to_dto()
        except Exception as e:
            await session.rollback()
            raise HTTPException(400, detail=str(e))

    async def update(
        self,
        item_id: UUID,
        data: dict = Body(),
        session: AsyncSession = Depends(get_async_session),
        current_user: User = Depends(fastapi_auth.current_user())
    ) -> SchemaType:
        data = self.update_schema.model_validate(data)
        updated_item = await self.update_base(session, current_user, data, item_id)
        if not updated_item:
            raise HTTPException(404, detail="Item not found")
            
        return updated_item


    async def delete(
        self,
        item_id: UUID,
        session: AsyncSession = Depends(get_async_session),
        current_user: User = Depends(fastapi_auth.current_user())
    ) -> None:
        if not await self.delete_base(session, current_user, item_id):
            raise HTTPException(404, detail="Item not found")
