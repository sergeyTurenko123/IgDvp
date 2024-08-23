from sqlalchemy import Column, Integer, String, func, Table
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.sqltypes import DateTime
from sqlalchemy.orm import relationship, Mapped, mapped_column
from typing import List

Base = declarative_base()

class Author(Base):
    __tablename__ = "author"
    id = Column(Integer, primary_key=True)
    fullname = Column(String(50), nullable=False)
    born_date = Column(String(50), nullable=False)
    born_location = Column(String(50), nullable=True)
    description = Column(String(50), nullable=True)
    created_at = Column('created_at', DateTime, default=func.now())


quote_m2m_tag = Table(
    "quote_m2m_tag",
    Base.metadata,
    Column("id", Integer, primary_key=True),
    Column("quote_id", Integer, ForeignKey("quote.id", ondelete="CASCADE")),
    Column("tag_id", Integer, ForeignKey("tag.id", ondelete="CASCADE")),
)

class Tag(Base):
    __tablename__ = "tag"
    id = Column(Integer, primary_key=True)
    name = Column(String(25), nullable=False, unique=True)

class Quote(Base):
    __tablename__ = "quote"
    id = Column(Integer, primary_key=True)
    quote = Column(String(500), nullable=True)
    tags = relationship("Tag", secondary=quote_m2m_tag, backref="quote")
    author_id = Column('author', ForeignKey('author.id', ondelete='CASCADE'), default=None)
    author = relationship ('Author', backref='quote')
    created_at = Column('created_at', DateTime, default=func.now())
