from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field, EmailStr, model_validator
from fastapi import UploadFile, File, Form
from dataclasses import dataclass

class TagModel(BaseModel):
    name: str = Field(max_length=25)


class TagResponse(TagModel):
    id: int

    class Config:
        orm_mode = True
        
        
class NoteBase(BaseModel):
    title: str = Field(max_length=50)
    description: str = Field(max_length=150)
    done: Optional[bool] = None


class NoteModel(NoteBase):
    tags: List[int]


class NoteUpdate(NoteModel):
    done: bool


class NoteStatusUpdate(BaseModel):
    done: bool


class NoteResponse(NoteBase):
    id: int
    created_at: datetime
    tags: List[TagResponse]

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
