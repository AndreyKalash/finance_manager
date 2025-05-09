from fastapi import APIRouter

from .auth_config import auth_backend, fastapi_auth
from .schemas import UserCreate, UserRead, UserUpdate

auth_router = APIRouter(prefix="/auth", tags=["auth"])
auth_router.include_router(fastapi_auth.get_auth_router(auth_backend))
auth_router.include_router(fastapi_auth.get_register_router(UserRead, UserCreate))
auth_router.include_router(fastapi_auth.get_reset_password_router())
auth_router.include_router(fastapi_auth.get_verify_router(UserRead))

user_router = APIRouter(prefix="/users", tags=["users"])
user_router.include_router(fastapi_auth.get_users_router(UserRead, UserUpdate))
