import enum
from sqlalchemy import Column, Integer, String, func, Table, Boolean, Enum
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.sqltypes import DateTime
from sqlalchemy.orm import relationship

from src.database.db import engine

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

class Role(enum.Enum):
    user: str = "user"
    moderator: str = "moderator"  
    admin: str = "admin"

photos_m2m_tag = Table(
    "photos_m2m_tag",
    Base.metadata,
    Column("id", Integer, primary_key=True),
    Column("photos_id", Integer, ForeignKey("photos.id", ondelete="CASCADE")),
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
    description = Column(String(500), nullable=True)
    tags = relationship("Tag", secondary=photos_m2m_tag, backref="photos")
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    user = relationship('Users', backref='photos')
    done = Column(Boolean, default=False)
    created_at = Column('created_at', DateTime, default=func.now())

class Comments(Base):
    __tablename__ = "comments"
    id = Column(Integer, primary_key=True)
    comment = Column(String(250), nullable=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    user = relationship('Users', backref='comments')
    photo_id = Column(Integer, ForeignKey('photos.id', ondelete='CASCADE'), nullable=False)
    photo = relationship('Photos', backref='comments')
    updated_at = Column('updated_at', DateTime, default=func.now())

class Qrcode(Base):
    __tablename__ = "qrcode"
    id = Column(Integer, primary_key=True)
    qrcode_url = Column(String(250), nullable=True)
    photo_id = Column(Integer, ForeignKey('photos.id', ondelete='CASCADE'), nullable=False)
    photo = relationship('Photos', backref='qrcode')

class Bannedlist(Base):
    __tablename__ = "bannedlist"
    id = Column(Integer, primary_key=True)
    token = Column(String(255), nullable=False, unique=True)
    created_at = Column('crated_at', DateTime, default=func.now())
# Base.metadata.create_all(bind=engine)