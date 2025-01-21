from pydantic import BaseModel

class AuthDTO(BaseModel):
    username: str
    password: str