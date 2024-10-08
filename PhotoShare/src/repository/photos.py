from typing import List
from sqlalchemy.orm import Session
from fastapi import HTTPException

from src.database.models import Photos, Tag, Users
from src.schemas import PhotoUpdate, PhotoStatusUpdate, PhotoModel

async def get_photos(skip: int, limit: int, db: Session) -> List[Photos]:
    return db.query(Photos).offset(skip).limit(limit).all()

async def get_search_by_tags(tag: str, db: Session,) -> List[Photos]:
    tags = db.query(Tag).filter(Tag.name==tag).first()
    if not tags:
        raise HTTPException(status_code=404, detail="tag not found")
    photos = db.query(Photos).filter(Photos.tags.contains(tags)).all()
    return photos

async def get_photo(photo_id: int, db: Session) -> Photos:
    photo = db.query(Photos).filter(Photos.id == photo_id).first()
    if photo is None:
        raise HTTPException(status_code=404, detail="photo not found")
    return photo

async def create_image_repository(body: PhotoModel, photo_url: str, user:Users, db: Session) -> Photos:
    tags = db.query(Tag).filter(Tag.name.in_(body.tags)).all()        
    photo = Photos(photo=photo_url, description=body.description, tags=tags, user_id=user.id)
    db.add(photo)
    db.commit()
    db.refresh(photo)
    return photo

async def remove_photo(photo_id: int, user:Users, db: Session) -> Photos | None:
    photo = db.query(Photos).filter(Photos.id == photo_id).filter(Photos.user_id==user.id).first()
    if photo:
        db.delete(photo)
        db.commit()
    return photo


async def update_photo(photo_id: int, body: PhotoModel, user:Users, db: Session) -> Photos | None:
    tags = db.query(Tag).filter(Tag.name.in_(body.tags)).all()
    photo = db.query(Photos).filter(Photos.id == photo_id).filter(Photos.user_id==user.id).first()
    if photo:
        photo.description = body.description
        photo.tags = tags
        db.commit()
    return photo


async def update_status_photo(photo_id: int, body: PhotoStatusUpdate, user:Users, db: Session) -> Photos | None:
    photo = db.query(Photos).filter(Photos.id == photo_id).filter(Photos.user_id==user.id).first()
    if photo:
        photo.done = body.done
        db.commit()
    return photo
