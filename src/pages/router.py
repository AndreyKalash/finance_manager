from typing import Annotated, Optional
from fastapi import Depends, Query, Request, APIRouter
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from src.models import User
from src.auth.auth_config import fastapi_auth


pages_router = APIRouter(
    prefix="",
    tags=["Pages"],
)
templates = Jinja2Templates(directory="src//templates")


@pages_router.get("/", response_class=HTMLResponse)
async def get_main_page(
    request: Request,
    limit: Annotated[int, Query(ge=1, le=50)] = 50,
    user: Optional[User] = Depends(fastapi_auth.current_user(optional=True)),
):
    if user is None:
        return RedirectResponse(url="/login", status_code=303)

    return templates.TemplateResponse(
        request=request,
        name="main.html",
        context={"title": "Finance manager", "user": user},
    )


@pages_router.get("/login", response_class=HTMLResponse)
async def get_expenses(request: Request):
    return templates.TemplateResponse(
        request=request, name="login.html", context={"title": "Вход"}
    )


@pages_router.get("/register", response_class=HTMLResponse)
async def serve_register_page(request: Request):
    return templates.TemplateResponse(
        request=request, name="login.html", context={"title": "Регистрация"}
    )


@pages_router.get("/expenses", response_class=HTMLResponse)
async def get_expenses(request: Request):
    return templates.TemplateResponse(
        request=request, name="expenses.html", context={"title": "Траты"}
    )


@pages_router.get("/profile", response_class=HTMLResponse)
async def get_profile(request: Request):
    return templates.TemplateResponse(
        request=request, name="profile.html", context={"title": "Профиль"}
    )
