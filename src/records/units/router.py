from src.models import Unit
from src.routers.base import BaseRouter

from src.schemas import UnitDTO, UnitAddDTO


class UnitRouter(BaseRouter):
    def __init__(self):
        super().__init__(
            model=Unit,
            schema=UnitDTO,
            create_schema=UnitAddDTO,
            update_schema=UnitAddDTO,
            prefix="/units",
            tags=['units'],
            )
    

units_router = UnitRouter().router

