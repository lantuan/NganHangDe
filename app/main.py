from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.routers import home
from app.routers import auth
from app.routers import chat

app = FastAPI(title="Ngân Hàng Đề AI")

app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.include_router(home.router)
app.include_router(auth.router)
app.include_router(chat.router)