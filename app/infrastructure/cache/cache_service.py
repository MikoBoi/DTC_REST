from cachetools import LRUCache
from typing import Optional

class OrderCache:
    def __init__(self, max_size: int = 100):
        self.cache = LRUCache(max_size)

    def get(self, order_id: int) -> Optional[dict]:
        return self.cache.get(order_id)

    def set(self, order_id: int, order: dict):
        self.cache[order_id] = order

    def delete(self, order_id: int):
        if order_id in self.cache:
            del self.cache[order_id]

    def get_all(self):
        return self.cache.items()

order_cache = OrderCache()

all_orders_in_cache = order_cache.get_all()
for order_id, order in all_orders_in_cache:
    print(f"Order ID: {order_id}, Order: {order}")