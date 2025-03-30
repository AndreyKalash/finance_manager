from uuid import UUID
from pydantic import BaseModel, ConfigDict, EmailStr
from fastapi_users.schemas import BaseUserCreate, BaseUser, BaseUserUpdate


class UserRead(BaseUser):
    id: UUID
    username: str
    email: EmailStr
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False

    model_config = ConfigDict(from_attributes=True)


class UserCreate(BaseUserCreate):
    username: str
    email: EmailStr
    password: str
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False


class UserUpdate(BaseUserUpdate):
    username: str
    password: str | None = None
    email: EmailStr | None = None
    is_active: bool | None = None
    is_superuser: bool | None = None
    is_verified: bool | None = None
