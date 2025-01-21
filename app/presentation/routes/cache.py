from fastapi import APIRouter
from app.infrastructure.cache.cache_service import order_cache

cache_router = APIRouter()

@cache_router.get("/orders")
def get_cache_orders():
    cached_orders = order_cache.get_all()
    return {order_id: order for order_id, order in cached_orders}