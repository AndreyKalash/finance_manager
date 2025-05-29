import logging

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles

import src.routers as ar

logging.basicConfig(level=logging.DEBUG)
app = FastAPI()

origins = [
    "http://localhost:8080",
    "http://localhost",
    "http://127.0.0.1:8080",
    "http://192.168.0.11:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["Content-Disposition"]
)

app.include_router(ar.auth_router)
app.include_router(ar.user_router)
app.include_router(ar.units_router)
app.include_router(ar.tags_router)
app.include_router(ar.categories_router)
app.include_router(ar.records_router)
app.include_router(ar.stats_router)


if __name__ == "__main__":
    uvicorn.run(app=app, reload=True)
