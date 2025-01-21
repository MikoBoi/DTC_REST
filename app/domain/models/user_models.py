from enum import Enum

class Role(Enum):
    USER = "user"
    ADMIN = "admin"

class User:
    def __init__(self, user_id: int, username: str, password: str, role: Role):
        self.user_id = user_id
        self.username = username
        self.password = password
        self.role = role