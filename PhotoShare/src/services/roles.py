# roles.py
from fastapi import HTTPException, status, Depends
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from typing import List
from . import models, schemas, auth
from .database import SessionLocal

# Декоратор для перевірки ролі
def role_required(required_roles: List[str]):
    def decorator(func):
        async def wrapper(*args, **kwargs):
            request = kwargs.get("request")
            token = request.headers.get("Authorization")
            if token:
                token = token.replace("Bearer ", "")
                try:
                    payload = jwt.decode(token, auth.SECRET_KEY, algorithms=[auth.ALGORITHM])
                    username: str = payload.get("sub")
                    if username is None:
                        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
                    
                    db: Session = kwargs.get("db")
                    user = db.query(models.User).filter(models.User.username == username).first()
                    if user is None or user.role not in required_roles:
                        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions")
                    
                    kwargs["current_user"] = user
                except JWTError:
                    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
            else:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token required")

            return func(*args, **kwargs)

        return wrapper
    return decorator

# Приклад використання декоратора
from fastapi import APIRouter, Request

router = APIRouter()

@router.get("/admin-data/")
@role_required(required_roles=["admin"])
async def read_admin_data(request: Request, db: Session = Depends(SessionLocal)):
    current_user = request.state.current_user
    return {"msg": "Hello Admin", "user": current_user.username}

@router.get("/moderator-data/")
@role_required(required_roles=["admin", "moderator"])
async def read_moderator_data(request: Request, db: Session = Depends(SessionLocal)):
    current_user = request.state.current_user
    return {"msg": "Hello Moderator", "user": current_user.username}

@router.get("/user-data/")
@role_required(required_roles=["admin", "moderator", "user"])
async def read_user_data(request: Request, db: Session = Depends(SessionLocal)):
    current_user = request.state.current_user
    return {"msg": "Hello User", "user": current_user.username}
