from datetime import datetime
from typing import List
from pydantic import BaseModel, Field, EmailStr

from src.database.models import Tag

class TagModel(BaseModel):
    name: str = Field(max_length=25)


class TagResponse(TagModel):
    id: int

    class Config:
        orm_mode = True

class UserModel(BaseModel):
    username: str = Field(min_length=4, max_length=16)
    email: str
    password: str = Field(min_length=6, max_length=10)


class UserDb(BaseModel):
    id: int
    username: str
    email: str
    created_at: datetime
    avatar: str

    class ConfigDict:
        orm_mode = True


class UserResponse(BaseModel):
    user: UserDb
    detail: str = "User successfully created"


class TokenModel(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class RequestEmail(BaseModel):
    email: EmailStr

class PhotoBase(BaseModel):
    description: str = Field(max_length=500)    
  
class PhotoModel(PhotoBase):
    tags: List[str]

class PhotoUpdate(PhotoModel):
    done: bool

class PhotoStatusUpdate(BaseModel):
    done: bool

class PhotoResponse(BaseModel):
    id: int
    photo: str
    description: str = Field(max_length=500)
    tags: List[TagResponse]
    user: UserDb
    created_at: datetime
    
    class Config:
        orm_mode = True

class CloudinarImage(BaseModel):
    rounding: str | None = None
    sharpen: str | None = None
    repaint_the_T_shirt: str | None = None
    restore: str | None = None
    enhance: str | None = None
    optimization: str | None = None

