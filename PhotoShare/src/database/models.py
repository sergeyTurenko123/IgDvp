from sqlalchemy import Column, Integer, String, func, Table, Boolean
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.sqltypes import DateTime
from sqlalchemy.orm import relationship, Mapped, mapped_column
from typing import List

Base = declarative_base()

class Users(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String(50))
    email = Column(String(250), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    created_at = Column('crated_at', DateTime, default=func.now())
    avatar = Column(String(255), nullable=True)
    refresh_token = Column(String(255), nullable=True)
    confirmed = Column(Boolean, default=False)


photos_m2m_tag = Table(
    "photo_m2m_tag",
    Base.metadata,
    Column("id", Integer, primary_key=True),
    Column("photo_id", Integer, ForeignKey("photo.id", ondelete="CASCADE")),
    Column("tag_id", Integer, ForeignKey("tag.id", ondelete="CASCADE")),
)

class Tag(Base):
    __tablename__ = "tag"
    id = Column(Integer, primary_key=True)
    name = Column(String(25), nullable=False, unique=True)

class Photos(Base):
    __tablename__ = "photo"
    id = Column(Integer, primary_key=True)
    photo = Column(String(500), nullable=True)
    description = Column(String(500), nullable=True)
    tags = relationship("Tag", secondary=photos_m2m_tag, backref="photo")
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    user = relationship('Users', backref='photo')
    done = Column(Boolean, default=False)
    created_at = Column('created_at', DateTime, default=func.now())

class Comments(Base):
    __tablename__ = "comment"
    id = Column(Integer, primary_key=True)
    comment = Column(String(250), nullable=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    user = relationship('Users', backref='photo')
    photo_id = Column(Integer, ForeignKey('photo.id', ondelete='CASCADE'), nullable=False)
    user = relationship('Photos', backref='comment')

class Qrcode(Base):
    __tablename__ = "qrcode"
    id = Column(Integer, primary_key=True)
    qrcode = Column(String(250), nullable=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    user = relationship('Users', backref='qrcode')