from sqlalchemy.orm import Session
from app.domain.interfaces.user_interfaces import UserRepository
from app.infrastructure.models.user_models import User

class SQLAlchemyUserRepository(UserRepository):
    def __init__(self, session: Session):
        self.session = session

    def get_by_username(self, username: str) -> User | None:
        user = self.session.query(User).filter_by(username=username).first()
        return user