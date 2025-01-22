from fastapi import APIRouter
from app.presentation.routes.orders import metrics

metrics_router = APIRouter()

# Вывод metrics.json
@metrics_router.get("/metrics")
def get_metrics():
    return metrics.get_metrics()