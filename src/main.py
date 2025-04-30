from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from starlette.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import src.routers as ar
import uvicorn
import logging

logging.basicConfig(level=logging.DEBUG)
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
