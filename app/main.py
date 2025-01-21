from fastapi import FastAPI

from app.infrastructure.db import SessionLocal, Base, engine
from app.presentation.routes import orders, auth

app = FastAPI(
    title="Order Management API",
    description="API для управления заказами с авторизацией, кэшированием и логированием.",
    version="1.0.0"
)

app.include_router(orders.router, prefix="/api/v1", tags=["Orders"])
app.include_router(auth.auth_router, prefix="/auth", tags=["Authentication"])

Base.metadata.create_all(bind=engine)