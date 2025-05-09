from fastapi_users.authentication import (
    AuthenticationBackend,
    CookieTransport,
    JWTStrategy,
)
from fastapi_users import FastAPIUsers
from src.models import User
from .manager import get_user_manager

from src.config import SECRET_AUTH


cookie_transport = CookieTransport(cookie_name="fm", cookie_max_age=10800)


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=SECRET_AUTH, lifetime_seconds=10800)


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=cookie_transport,
    get_strategy=get_jwt_strategy,
)

fastapi_auth = FastAPIUsers[User, int](get_user_manager, [auth_backend])
