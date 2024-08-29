from fastapi import APIRouter, HTTPException, Depends, status, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import List
import cloudinary
import cloudinary.uploader
from datetime import datetime

from src.conf.config import config
from src.database.models import Users, Tag
from src.services.auth import auth_service
from src.database.db import get_db
from src.schemas import PhotoModel, PhotoStatusUpdate, PhotoResponse
from src.repository import photos as repository_photo
from src.repository import tags as repository_tags

router = APIRouter(prefix='/photo', tags=["photo"])


@router.get("/", response_model=List[PhotoResponse])
async def read_photos(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db)):
    photos = await repository_photo.get_photos(skip, limit, db)
    return photos
    
@router.get("/{tags}", response_model=List[PhotoResponse])
async def read_photos( 
    tag: str | None=None,
    db: Session = Depends(get_db)):
    photo = await repository_photo.get_search_by_tags(tag, db)
    return photo

@router.get("/{photo_id}", response_model=PhotoResponse)
async def read_photo(photo_id: int, db: Session = Depends(get_db)):
    photo = await repository_photo.get_photo(photo_id, db)
    if photo is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Photo not found")
    return photo



@router.post("/", response_model=PhotoResponse, status_code=status.HTTP_201_CREATED)
async def create_photo(
        description: str = Form(...),
        tags: List[str] = Form([]),
        file: UploadFile = File(...),
        db: Session = Depends(get_db), current_user: Users = Depends(auth_service.get_current_user)):
    cloudinary.config(
        cloud_name=config.CLD_NAME,
        api_key=config.CLD_API_KEY,
        api_secret=config.CLD_API_SECRET,
        secure=True
    )
    public_id = f'photoApp/{current_user.username}_{datetime.now().strftime("%Y%m%d%H%M%S")}'
    r = cloudinary.uploader.upload(file.file, public_id=public_id, overwrite=False)
    photo_url = cloudinary.CloudinaryImage(public_id).build_url(
        version=r.get("version")
    )
    for tags_str in tags:
            tag_list = tags_str.split(",")
            tag_count = len(tag_list)

            if tag_count>5:
                raise HTTPException(
                        status_code=400, detail="Maximum number of tags - 5"
                )
            for tag_name in tag_list:
                tag_name = tag_name.strip()
                tag = db.query(Tag).filter_by(name=tag_name).first()
                if tag is None:
                    tag = Tag(name=tag_name)
                    db.add(tag)
                    db.commit()
                    db.refresh(tag)

    body = PhotoModel(description=description, tags=tag_list)
    image = await repository_photo.create_image_repository(body, photo_url, current_user, db)
    return image

@router.put("/{photo_id}", response_model=PhotoResponse)
async def update_photo(
    photo_id: int,
    description: str = Form(...), 
    tags: List[str] = Form([]), 
    db: Session = Depends(get_db), 
    current_user: Users = Depends(auth_service.get_current_user)):
    
    for tags_str in tags:
            tag_list = tags_str.split(",")
            tag_count = len(tag_list)

            if tag_count>5:
                raise HTTPException(
                        status_code=400, detail="Maximum number of tags - 5"
                )
            for tag_name in tag_list:
                tag_name = tag_name.strip()
                tag = db.query(Tag).filter_by(name=tag_name).first()
                if tag is None:
                    tag = Tag(name=tag_name)
                    db.add(tag)
                    db.commit()
                    db.refresh(tag)
    
    body = PhotoModel(description=description, tags=tag_list)
    photo = await repository_photo.update_photo(photo_id, body, current_user, db)
    if photo is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Photo not found")
    return photo


@router.patch("/{photo_id}", response_model=PhotoResponse)
async def update_status_photo(body: PhotoStatusUpdate, photo_id: int, db: Session = Depends(get_db),
                              current_user: Users = Depends(auth_service.get_current_user)):
    photo = await repository_photo.update_status_photo(photo_id, body, current_user, db)
    if photo is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Photo not found")
    return photo


@router.delete("/{photo_id}", response_model=PhotoResponse)
async def remove_photo(photo_id: int, db: Session = Depends(get_db), 
                       current_user: Users = Depends(auth_service.get_current_user)):
    photo = await repository_photo.remove_photo(photo_id, current_user, db)
    if photo is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Photo not found")
    return photo
