from sqlalchemy.orm import Session
from app.domain.interfaces.order_interfaces import OrderRepository, ProductRepository
from app.infrastructure.models.order_models import Order
from app.infrastructure.models.order_models import Product

class SQLAlchemyOrderRepository(OrderRepository):
    def __init__(self, session: Session):
        self.session = session

    def create(self, order):
        db_order = Order(
            customer_name=order.customer_name,
            total_price=order.total_price,
            status=order.status,
            user_id=order.user_id
        )
        self.session.add(db_order)
        self.session.commit()
        self.session.refresh(db_order)
        return db_order

    def save(self, order):
        self.session.commit()
        self.session.refresh(order)
        return order

    def get_by_id(self, order_id):
        return self.session.query(Order).filter(Order.order_id == order_id, Order.is_deleted == False).first()

    def get_orders(self, cur_usr, status=None, min_price=None, max_price=None):
        query = self.session.query(Order)

        query = query.filter(Order.is_deleted == False)

        if cur_usr["role"] == "USER":
            query = query.filter(Order.user_id == int(cur_usr["user_id"]))

        if status:
            query = query.filter(Order.status == status)
        if min_price:
            query = query.filter(Order.total_price >= min_price)
        if max_price:
            query = query.filter(Order.total_price <= max_price)
        return query.all()



class SQLAlchemyProductRepository(ProductRepository):
    def __init__(self, session: Session):
        self.session = session

    def add(self, product):
        db_product = Product(
            name=product.name,
            price=product.price,
            quantity=product.quantity,
            order_id=product.order_id
        )
        self.session.add(db_product)
        self.session.commit()
        self.session.refresh(db_product)
        return db_product