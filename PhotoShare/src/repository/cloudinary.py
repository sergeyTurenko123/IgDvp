from cloudinary import CloudinaryImage
import cloudinary.uploader
from typing import List
from sqlalchemy.orm import Session
from fastapi import HTTPException

from src.database.models import Photos, Users
from src.schemas import PhotoUpdate, PhotoStatusUpdate, PhotoModel
from src.conf.config import config

async def cloudinary_editor(photo_id, cloudinary_action, user:Users, db: Session):
    photo = db.query(Photos).filter(Photos.id == photo_id).filter(Photos.user_id==user.id).first()
    photo_photo = photo.photo
    cloudinary.config(
        cloud_name=config.CLD_NAME,
        api_key=config.CLD_API_KEY,
        api_secret=config.CLD_API_SECRET,
        secure=True
    )
    
    if cloudinary_action == 'rounding':
        photo_url = cloudinary.CloudinaryImage(photo_photo).image(transformation=[
  {'aspect_ratio': "1:1", 'gravity': "auto", 'width': 500, 'crop': "auto"},
  {'radius': "max"}]) # округление фото
    elif cloudinary_action == 'sharpen':
        photo_url = cloudinary.CloudinaryImage(photo_photo).image(effect="sharpen:150") # резкость
    elif cloudinary_action == 'repaint_the_T_shirt':
        photo_url = cloudinary.CloudinaryImage(photo_photo).image(effect="gen_recolor:prompt_t-shirt;to-color_E7E719") # перекрасить футболку
    elif cloudinary_action == 'restore':
        photo_url = cloudinary.CloudinaryImage(photo_photo).image(effect="gen_restore") # востановление
    elif cloudinary_action == 'restore':
        photo_url = cloudinary.CloudinaryImage(photo_photo).image(effect="enhance") # усиливает
    elif cloudinary_action == 'restore':
        photo_url = cloudinary.CloudinaryImage(photo_photo).image(transformation=[
  {'width': 1000, 'crop': "scale"},
  {'quality': "auto"},
  {'fetch_format': "auto"}
  ])# оптимизация
    if photo:
        photo.photo = photo_url
        db.commit()
    return photo_url
