from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field, EmailStr

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

        
class QuoteBase(BaseModel):
    quote: str = Field(max_length=500)
    
    
class QuoteModel(QuoteBase):
    tags: List[int]
    author_id: int

class QuoteUpdate(QuoteModel):
    done: bool

class QuoteStatusUpdate(BaseModel):
    done: bool

class QuoteResponse(BaseModel):
    id: int
    quote: str = Field(max_length=500)
    tags: List[TagResponse]
    author: UserResponse
    created_at: datetime
    
    class Config:
        orm_mode = True