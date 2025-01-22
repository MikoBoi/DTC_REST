from abc import ABC, abstractmethod
from app.domain.models.order_models import Order, Product
from typing import Optional

class OrderRepository(ABC):
    @abstractmethod
    def create(self, order: Order):
        pass

    @abstractmethod
    def save(self, order: Order):
        pass

    @abstractmethod
    def get_by_id(self, order_id: int) -> Order:
        pass

    @abstractmethod
    def get_orders(self, cur_usr, status: Optional[str] = None, min_price: Optional[float] = None, max_price: Optional[float] = None):
        pass

class ProductRepository(ABC):
    @abstractmethod
    def add(self, product: Product):
        pass