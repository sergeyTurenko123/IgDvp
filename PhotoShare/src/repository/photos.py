from typing import List
from fastapi import HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
import cloudinary
import cloudinary.uploader
from src.conf.config import config

from src.database.models import Photos, Tag, Users
from src.schemas import PhotoUpdate, PhotoStatusUpdate, PhotoModel

async def get_photos(skip: int, limit: int, db: Session) -> List[Photos]:
    return db.query(Photos).offset(skip).limit(limit).all()

async def get_photo(photo_id: int, db: Session) -> Photos:
    return db.query(Photos).filter(Photos.id == photo_id).first()

async def create_photo(body: PhotoModel, db: Session, file: UploadFile = File()) -> Photos:
    tags = db.query(Tag).filter(Tag.id.in_(body.tags)).all()
    user = db.query(Users).filter(Users.id == body.user_id).first()
    cloudinary.config(
        cloud_name=config.CLD_NAME,
        api_key=config.CLD_API_KEY,
        api_secret=config.CLD_API_SECRET,
        secure=True
    )
    r = cloudinary.uploader.upload(file.file, public_id=f'NotesApp/{user.username}', overwrite=True)
    src_url = cloudinary.CloudinaryImage(f'NotesApp/{user.username}')\
                        .build_url(width=250, height=250, crop='fill', version=r.get('version'))
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    photo = Photos(photo = src_url, description = body.description, tags=tags, user=user)
    db.add(photo)
    db.commit()
    db.refresh(photo)
    return photo

async def remove_photo(quote_id: int, db: Session) -> Photos | None:
    quote = db.query(Photos).filter(Photos.id == quote_id).first()
    if quote:
        db.delete(quote)
        db.commit()
    return quote


async def update_photo(photo_id: int, body: PhotoUpdate, db: Session) -> Photos | None:
    photo = db.query(Photos).filter(Photos.id == photo_id).first()
    if photo:
        tags = db.query(Tag).filter(Tag.id.in_(body.tags)).all()
        photo.photo = body.photo
        photo.description = body.description
        photo.user = body.user_id
        photo.tags = tags
        db.commit()
    return photo


async def update_status_photo(photo_id: int, body: PhotoStatusUpdate, db: Session) -> Photos | None:
    photo = db.query(Photos).filter(Photos.id == photo_id).first()
    if photo:
        photo.done = body.done
        db.commit()
    return photo
