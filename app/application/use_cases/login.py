from fastapi import HTTPException

from app.domain.interfaces.user_interfaces import UserRepository
from app.infrastructure.auth.token_service import TokenService

class LoginUseCase:
    def __init__(self, user_repository: UserRepository, token_service: TokenService):
        self.user_repository = user_repository
        self.token_service = token_service

    def execute(self, username: str, password: str) -> dict:
        user = self.user_repository.get_by_username(username)
        if not user or user.password != password:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        token = self.token_service.create_access_token(user_id=user.user_id, role=user.role.value.upper())
        return {"access_token": token, "token_type": "bearer"}