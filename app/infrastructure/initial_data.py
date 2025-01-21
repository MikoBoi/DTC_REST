from sqlalchemy.orm import Session
from app.infrastructure.models.user_models import *

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