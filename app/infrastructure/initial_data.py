from sqlalchemy.orm import Session
from app.infrastructure.models.user_models import *
from app.infrastructure.models.order_models import *

def seed_initial_users(db: Session):
    if db.query(User).count() == 0:
        users = [
            User(
                user_id=1,
                username="admin",
                password="admin",
                role=Role.ADMIN,
            ),
            User(
                user_id=2,
                username="user",
                password="user",
                role=Role.USER,
            ),
        ]
        db.add_all(users)
        db.commit()

        orders = [
            Order(
                customer_name="CN1", total_price=100, user_id=1, status="pending"
            ),
            Order(
                customer_name="CN2", total_price=100, user_id=1, status="confirmed"
            ),
            Order(
                customer_name="CN3", total_price=100, user_id=2, status="pending"
            ),
            Order(
                customer_name="CN4", total_price=100, user_id=2, status="cancelled", is_deleted=True
            ),
            Order(
                customer_name="CN5", total_price=100, user_id=1, status="confirmed"
            ),
            Order(
                customer_name="CN6", total_price=100, user_id=2, status="pending", is_deleted=True
            ),
            Order(
                customer_name="CN7", total_price=100, user_id=2, status="cancelled"
            ),
        ]

        db.add_all(orders)
        db.commit()

        for product in range(len(orders)):
            db.add(Product(name="PRD"+str(product+1), price=100, quantity=1, order_id=product+1))
            db.commit()