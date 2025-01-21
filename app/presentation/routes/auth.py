from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.application.use_cases.login import LoginUseCase
from app.infrastructure.auth.token_service import TokenService
from app.infrastructure.db import get_db
from app.infrastructure.repositories.user_repository import SQLAlchemyUserRepository
from app.presentation.dto import *

auth_router = APIRouter()

@auth_router.post("/login")
def login(
    data: AuthDTO = Depends(),
    db: Session = Depends(get_db)
):
    user_repository = SQLAlchemyUserRepository(db)
    token_service = TokenService()
    login_use_case = LoginUseCase(user_repository, token_service)
    return login_use_case.execute(data.username, data.password)