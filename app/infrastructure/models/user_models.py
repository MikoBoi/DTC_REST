from sqlalchemy import Column, Integer, String, Enum as SQLAlchemyEnum
from app.infrastructure.db import Base
from enum import Enum

class Role(Enum):
    USER = "user"
    ADMIN = "admin"

class User(Base):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    role = Column(SQLAlchemyEnum(Role), default=Role.USER)