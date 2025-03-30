from fastapi import FastAPI
from starlette.staticfiles import StaticFiles
import src.routers as ar
import uvicorn

app = FastAPI()

app.mount("/static", StaticFiles(directory="src/static"), name="static")

app.include_router(ar.auth_router)
app.include_router(ar.user_router)
app.include_router(ar.units_router)
app.include_router(ar.tags_router)
app.include_router(ar.categories_router)
app.include_router(ar.records_router)
app.include_router(ar.pages_router)


if __name__ == '__main__':
    uvicorn.run(app=app, reload=True)
