from sqlalchemy import Column, Integer, String, func, ForeignKey, Boolean, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.sqltypes import DateTime
from sqlalchemy.orm import relationship, Mapped, mapped_column
from typing import List

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String(50))
    email = Column(String(250), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    created_at = Column('crated_at', DateTime, default=func.now())
    avatar = Column(String(255), nullable=True)
    refresh_token = Column(String(255), nullable=True)
    confirmed = Column(Boolean, default=False)


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

class Photos(Base):
    __tablename__ = "photos"
    id = Column(Integer, primary_key=True)
    photo = Column(String(500), nullable=True)
    comment = Column(String(500), nullable=True)
    tags = relationship("Tag", secondary=quote_m2m_tag, backref="photos")
    user_id = Column('users_id', ForeignKey('users.id', ondelete='CASCADE'), default=None)
    user = relationship ('User', backref='photos')
    created_at = Column('created_at', DateTime, default=func.now())
