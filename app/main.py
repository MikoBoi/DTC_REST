from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError, HTTPException
from fastapi.responses import JSONResponse

from app.infrastructure.db import SessionLocal, Base, engine
from app.infrastructure.initial_data import seed_initial_users

from app.infrastructure.logging.logger import logger

from app.presentation.routes import orders, auth, cache, metrics
from app.presentation.routes.orders import collect_metrics

app = FastAPI(
    title="Order Management API",
    description="API для управления заказами с авторизацией, кэшированием и логированием.",
    version="1.0.0"
)

@app.exception_handler(HTTPException)
async def validation_exception_handler(request: Request, exc: HTTPException):
    if exc.status_code == 401 and request.scope["route"].path != "/auth/login":
        collect_metrics(endpoint=request.method + " " + request.scope["route"].path, success=False)

    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    collect_metrics(endpoint=request.method + " " + request.scope["route"].path, success=False)
    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors()},
    )



@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"Received request: {request.method} {request.url}")
    response = await call_next(request)
    logger.info(f"Responded with status code {response.status_code}")
    return response

app.include_router(orders.router, prefix="/api/v1", tags=["Orders"])
app.include_router(auth.auth_router, prefix="/auth", tags=["Authentication"])
app.include_router(metrics.metrics_router, tags=["Metrics"])
app.include_router(cache.cache_router, prefix="/cache", tags=["Cache"])

# Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

with SessionLocal() as db:
    seed_initial_users(db)