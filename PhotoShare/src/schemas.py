from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field, model_validator
from dataclasses import dataclass, field

class TagModel(BaseModel):
    name: str = Field(max_length=25)


class TagResponse(TagModel):
    id: int

    class Config:
        orm_mode = True

class AuthorBase(BaseModel):
    fullname: str = Field(max_length=50)
    born_date: str = Field(max_length=50)
    born_location: str = Field(max_length=50)
    description: str = Field(max_length=50)

class AuthorUpdate(AuthorBase):
    done: bool

class AuthorStatusUpdate(BaseModel):
    done: bool

class AuthorResponse(AuthorBase):
    id: int
    created_at: datetime
    
    class Config:
        orm_mode = True
        
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
    author: AuthorResponse
    created_at: datetime
    
    class Config:
        orm_mode = True