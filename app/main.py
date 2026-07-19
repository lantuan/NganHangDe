from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.routers import home
from app.routers import auth
from app.routers import chat

from app.routers import auth
from app.routers import chat

from app.routers import data

from app.routers import exam

app = FastAPI(title="Ngân Hàng Đề AI")

app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.include_router(home.router)
app.include_router(auth.router)
app.include_router(chat.router)

app.include_router(data.router)

app.include_router(exam.router)