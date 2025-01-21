from app.domain.models.order_models import Order, Product
from app.domain.interfaces.order_interfaces import OrderRepository, ProductRepository
from app.infrastructure.logging.logger import logger
from app.infrastructure.cache.cache_service import order_cache

from typing import Optional
from types import SimpleNamespace

class OrderUseCases:
    def __init__(self, order_repository: OrderRepository, product_repository: Optional[ProductRepository] = None):
        self.order_repository = order_repository
        self.product_repository = product_repository

    def create(self, order_create, cur_user_id):
        total_price = sum(p.price * p.quantity for p in order_create.products)
        order = Order(customer_name=order_create.customer_name, products=order_create.products, total_price=total_price, user_id=cur_user_id, status="pending")
        new_order = self.order_repository.create(order)
        for p in order_create.products:
            product = Product(name=p.name, price=p.price, quantity=p.quantity, order_id=new_order.order_id)
            self.product_repository.add(product)

        for_cache_dict = {
            "total_price": order.total_price,
            "order_id": new_order.order_id,
            "user_id": order.user_id,
            "customer_name": order.customer_name,
            "status": order.status,
            "is_deleted": new_order.is_deleted,
            "products": [Product(name=p.name, price=p.price, quantity=p.quantity, order_id=new_order.order_id) for p in order.products]
        }

        for_cache = SimpleNamespace(**for_cache_dict)

        order_cache.set(new_order.order_id, for_cache)

        logger.info(f"Order {new_order.order_id} created successfully")
        return order, {"order_id": new_order.order_id}



    def put(self, order_upd, current_order):
        if order_upd.status:
            current_order.status = order_upd.status

        if order_upd.products:
            current_order.total_price += sum(p.price * p.quantity for p in order_upd.products)

            for product_data in order_upd.products:
                product = Product(
                    name=product_data.name,
                    price=product_data.price,
                    quantity=product_data.quantity,
                    order_id=current_order.order_id
                )
                self.product_repository.add(product)

        self.order_repository.save(current_order)

        order_cache.set(current_order.order_id, current_order)

        logger.info(f"Order {current_order.order_id} edited successfully")
        return current_order



    def delete(self, current_order):
        current_order.is_deleted = True

        self.order_repository.save(current_order)

        order_cache.delete(current_order.order_id)

        logger.info(f"Order {current_order.order_id} deleted successfully")
        return current_order



    def get_order_by_id(self, order_id):
        order = order_cache.get(order_id)
        if not order:
            order = self.order_repository.get_by_id(order_id)
            if order:
                order_cache.set(order_id, order)
        return order