from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field, EmailStr
from dataclasses import dataclass, field

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
    photo: str
    description: str = Field(max_length=500)    
    
class PhotoModel(PhotoBase):
    tags: List[int]
    user_id: int

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

class CommentBase(BaseModel):
    comment: str = Field(max_length=50)
    photo_id: str = Field(max_length=150)
    user_id: str = Field(max_length=50)
    created_at: datetime
    updated_at: datetime

class CommentResponse(CommentBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True