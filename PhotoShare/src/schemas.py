from datetime import datetime
from typing import List
from pydantic import BaseModel, Field, EmailStr, ConfigDict

from src.database.models import Role

class TagModel(BaseModel):
    name: str = Field(max_length=25)


class TagResponse(TagModel):
    id: int

    class Config(ConfigDict):
        from_attributes = True

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

    class Config(ConfigDict):
        from_attributes = True


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
    id: int
    description: str
    photo: str
  
class PhotoModel(BaseModel):
    description: str = Field(max_length=500)
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
    
    class Config(ConfigDict):
        from_attributes = True

class CloudinarImage(BaseModel):
    rounding: str | None = None
    sharpen: str | None = None
    repaint_the_T_shirt: str | None = None
    restore: str | None = None
    enhance: str | None = None
    optimization: str | None = None

class QrcodeModel(BaseModel):
    qrcode_url: str

class QrcodeResponse(QrcodeModel):
    id: int

    class Config(ConfigDict):
        from_attributes = True

class User_Photo(BaseModel):
    id: int
    username: str
    created_at: datetime
    avatar: str
    photos: List[PhotoBase]

class CommentsBase(BaseModel):
    comment: str = Field(max_length=50)

class CommentsResponse(CommentsBase):
    id: int
    photo_id: int
    user_id: int
    updated_at: datetime

    class Config(ConfigDict):
        from_attributes = True

class UpdateProfile(BaseModel):
    username: str | None = Field(min_length=5, max_length=16)


class UpdateFullProfile(BaseModel):
    role: str | None = None