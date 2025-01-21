from enum import Enum

class Role(Enum):
    USER = "user"
    ADMIN = "admin"

class User:
    def __init__(self, user_id: int, username: str, hashed_password: str, role: Role):
        self.user_id = user_id
        self.username = username
        self.hashed_password = hashed_password
        self.role = role