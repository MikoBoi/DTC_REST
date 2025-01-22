import pytest
from app.infrastructure.cache.cache_service import OrderCache

@pytest.fixture
def cache():
    return OrderCache(max_size=10)

def test_add_to_cache(cache):
    order = {"order_id": 1, "customer_name": "John"}
    cache.set(order["order_id"], order)

    assert cache.get(1) == order

def test_update_cache(cache):
    order = {"order_id": 1, "customer_name": "John"}
    cache.set(order["order_id"], order)

    updated_order = {"order_id": 1, "customer_name": "Jane"}
    cache.set(order["order_id"], updated_order)

    assert cache.get(1)["customer_name"] == "Jane"

def test_delete_from_cache(cache):
    order = {"order_id": 1, "customer_name": "John"}
    cache.set(order["order_id"], order)

    cache.delete(order["order_id"])
    assert cache.get(1) is None