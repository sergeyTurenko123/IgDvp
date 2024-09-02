from fastapi import APIRouter, HTTPException, Depends, status, UploadFile, File # type: ignore
from sqlalchemy.orm import Session # type: ignore
from src.conf.config import config
import cloudinary.uploader # type: ignore

from src.database.models import Users
from src.services.auth import auth_service
from src.database.db import get_db
from src.schemas import PhotoModel, PhotoUpdate, PhotoStatusUpdate, PhotoResponse
from src.repository import photos as repository_photo

router = APIRouter(prefix='/photo', tags=["photo"])


@router.get("/", response_model=PhotoResponse)
async def read_photos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    photos = await repository_photo.get_photos(skip, limit, db)
    return photos

@router.get("/{photo_id}", response_model=PhotoResponse)
async def read_photo(photo_id: int, db: Session = Depends(get_db)):
    photo = await repository_photo.get_photo(photo_id, db)
    if photo is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Photo not found")
    return photo

@router.post("/", response_model=PhotoResponse, status_code=status.HTTP_201_CREATED)
async def create_photo(body: PhotoModel, file: UploadFile = File(), db: Session = Depends(get_db)):
    return await repository_photo.create_photo(body, file, db)

@router.put("/{photo_id}", response_model=PhotoResponse)
async def update_photo(body: PhotoUpdate, photo_id: int, db: Session = Depends(get_db)):
    photo = await repository_photo.update_photo(photo_id, body, db)
    if photo is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Photo not found")
    return photo


@router.patch("/{photo_id}", response_model=PhotoResponse)
async def update_status_photo(body: PhotoStatusUpdate, photo_id: int, db: Session = Depends(get_db)):
    photo = await repository_photo.update_status_photo(photo_id, body, db)
    if photo is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Photo not found")
    return photo


@router.delete("/{photo_id}", response_model=PhotoResponse)
async def remove_photo(photo_id: int, db: Session = Depends(get_db)):
    photo = await repository_photo.remove_photo(photo_id, db)
    if photo is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Photo not found")
    return photo
