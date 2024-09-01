import cloudinary
import cloudinary.uploader
from cloudinary.utils import cloudinary_url
from typing import List
from sqlalchemy.orm import Session
from fastapi import HTTPException
from datetime import datetime

from src.database.models import Photos, Users
from src.schemas import CloudinarImage
from src.conf.config import config

async def cloudinary_editor(photo_id, cloudinary_action, user:Users, db: Session):
    photo = db.query(Photos).filter(Photos.id == photo_id).filter(Photos.user_id==user.id).first()
    photo_photo = photo.photo
    photo_name = photo_photo
    cloudinary.config(
        cloud_name=config.CLD_NAME,
        api_key=config.CLD_API_KEY,
        api_secret=config.CLD_API_SECRET,
        secure=True
    )
    public_id = f'photoApp/{user.username}_{datetime.now().strftime("%Y%m%d%H%M%S")}'
    if cloudinary_action == 'rounding':
        r = cloudinary.uploader.upload(photo_photo, public_id=public_id, overwrite=True)
        photo_url = cloudinary.CloudinaryImage(public_id).build_url(transformation=[
            {'aspect_ratio': "1:1", 'gravity': "auto", 'width': 500, 'crop': "auto"},
            {'radius': "max"}])
    elif cloudinary_action == 'sharpen':
        r = cloudinary.uploader.upload(photo_photo, public_id=public_id, overwrite=True)
        photo_url = cloudinary.CloudinaryImage(public_id).build_url(effect="sharpen:150") # резкость
    elif cloudinary_action == 'repaint_the_T_shirt':
        r = cloudinary.uploader.upload(photo_photo, public_id=public_id, overwrite=True)
        photo_url = cloudinary.CloudinaryImage(public_id).build_url(effect="gen_recolor:prompt_t-shirt;to-color_E7E719") # перекрасить футболку
    elif cloudinary_action == 'restore':
        r = cloudinary.uploader.upload(photo_photo, public_id=public_id, overwrite=True)
        photo_url = cloudinary.CloudinaryImage(public_id).build_url(effect="gen_restore") # востановление
    elif cloudinary_action == 'enhance':
        r = cloudinary.uploader.upload(photo_photo, public_id=public_id, overwrite=True)
        photo_url = cloudinary.CloudinaryImage(public_id).build_url(effect="enhance") # усиливает
    elif cloudinary_action == 'optimization':
        r = cloudinary.uploader.upload(photo_photo, public_id=public_id, overwrite=True)
        photo_url = cloudinary.CloudinaryImage(public_id).build_url(transformation=[
            {'width': 1000, 'crop': "scale"},
            {'quality': "auto"},
            {'fetch_format': "auto"}])# оптимизация
    print(photo_url)
    if photo:
        photo.photo = photo_url
        db.commit()
    return photo
