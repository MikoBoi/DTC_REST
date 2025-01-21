from abc import ABC, abstractmethod
from app.domain.models.user_models import User

class UserRepository(ABC):
    @abstractmethod
    def get_by_username(self, username: str) -> User | None:
        pass