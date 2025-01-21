from fastapi import Depends, Header, HTTPException
from app.infrastructure.auth.token_service import TokenService

auth_service = TokenService()

def get_token(token: str = Header()) -> str:
    if not token:
        raise HTTPException(status_code=401, detail="Token header missing")
    return token

def get_current_user(token: str = Depends(get_token)):
    payload = auth_service.decode_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    return {"user_id": payload["sub"], "role": payload["role"]}