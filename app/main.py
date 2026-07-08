from fastapi import FastAPI
from app.routers import home, auth

app = FastAPI(title="Ngân Hàng Đề AI")

app.include_router(home.router)
app.include_router(auth.router)