from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.orm import Session
import cloudinary
import cloudinary.uploader
from cloudinary import CloudinaryImage

from src.database.db import get_db
from src.database.models import Users
from src.repository import users as repository_user
from src.services.auth import auth_service
from src.conf.config import config
from src.schemas import UserDb, User_Photo

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/{user_name}", response_model=User_Photo)
async def read_users_me(user_name: str, db: Session = Depends(get_db)):
    user = await repository_user.get_user(user_name, db)
    return user

@router.get("/me/", response_model=UserDb)
async def read_users_me(user: Users = Depends(auth_service.get_current_user)):
    return user

@router.patch('/avatar', response_model=UserDb)
async def update_avatar_user(
    file: UploadFile = File(), 
    user: Users = Depends(auth_service.get_current_user),
    db: Session = Depends(get_db)):
    """
    Update avatar user
    param file: Contact details.
    type: str
    :param user: User.
    :type user: str
    param db: The database session
    type: Session
    """
    cloudinary.config(
        cloud_name=config.CLD_NAME,
        api_key=config.CLD_API_KEY,
        api_secret=config.CLD_API_SECRET,
        secure=True
    )
    
    r = cloudinary.uploader.upload(file.file, public_id=f'UserApp/{user.username}', overwrite=True)
    srcURL = CloudinaryImage(f'UserApp/{user.username}').build_url(transformation=[
    {'aspect_ratio': "1:1", 'gravity': "auto", 'width': 500, 'crop': "auto"},
    {'radius': "max"}])
    
    user = await repository_user.update_avatar(user.email, srcURL, db)
    return user
