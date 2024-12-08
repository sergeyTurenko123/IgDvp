from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel  
import cloudinary
import cloudinary.uploader

from src.database.db import get_db
from src.database.models import Users, Photos
from src.repository import user as repository_user
from src.services.auth import auth_service
from src.conf.config import config
from src.schemas import UserDb

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/me/", response_model=UserDb)
async def read_users_me(user: Users = Depends(auth_service.get_current_user)):
    return user

@router.patch('/avatar', response_model=UserDb)
async def update_avatar_user(file: UploadFile = File(), user: Users = Depends(auth_service.get_current_user),
                             db: Session = Depends(get_db)):
    cloudinary.config(
        cloud_name=config.CLD_NAME,
        api_key=config.CLD_API_KEY,
        api_secret=config.CLD_API_SECRET,
        secure=True
    )

    r = cloudinary.uploader.upload(file.file, public_id=f'NotesApp/{user.username}', overwrite=True)
    src_url = cloudinary.CloudinaryImage(f'NotesApp/{user.username}')\
                        .build_url(width=250, height=250, crop='fill', version=r.get('version'))
    user = await repository_user.update_avatar(user.email, src_url, db)
    return user

@router.get("/profile/{username}", response_model=UserDb)
async def get_user_profile(username: str, db: Session = Depends(get_db)):
    user = db.query(Users).filter(Users.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    photo_count = db.query(Photos).filter(Photos.user_id == user.id).count()
    
    return {
        "username": user.username,
        "email": user.email,
        "registered_at": user.created_at,
        "photo_count": photo_count,
        "avatar": user.avatar
    }

class UserUpdate(BaseModel):  
    username: str
    email: str

@router.patch("/me/", response_model=UserDb)
async def update_user_me(user_update: UserUpdate, 
                         user: Users = Depends(auth_service.get_current_user),
                         db: Session = Depends(get_db)):
    user.username = user_update.username
    user.email = user_update.email

    db.commit()
    db.refresh(user)
    
    return user
