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

# Хэндлер, для записи 401 кода при обращений по /api/v1/orders/
# Если путь /auth/login, то не будет записываться в metrics.json
@app.exception_handler(HTTPException)
async def validation_exception_handler(request: Request, exc: HTTPException):
    if exc.status_code == 401 and request.scope["route"].path != "/auth/login":
        collect_metrics(endpoint=request.method + " " + request.scope["route"].path, success=False)

    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )

# Хэндлер, для записи 422 кода при обращений по /api/v1/orders/
# В случае падения данной ошибки будет записываться в metrics.json в соответствующую из методов
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    collect_metrics(endpoint=request.method + " " + request.scope["route"].path, success=False)
    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors()},
    )



# Middleware, для записи логов
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

# Base.metadata.drop_all(bind=engine)   # Очищаем БД, если есть необходимость, раскомментить
Base.metadata.create_all(bind=engine)   # Создаем таблицы

# При первой инициализаций БД, создаются начальные данные, два пользователя с ролями ADMIN и USER, и несолько заказов
with SessionLocal() as db:
    seed_initial_users(db)