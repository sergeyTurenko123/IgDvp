from sqlalchemy.orm import Session
import cloudinary
from cloudinary.uploader import upload
import cloudinary.api
import cloudinary.utils
import qrcode
from io import BytesIO

from src.database.models import Photos, Users, Qrcode
from src.schemas import CloudinarImage
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
    # f'photoApp/{user.username}_{datetime.now().strftime("%Y%m%d%H%M%S")}'
    public_id = f'Photoapp/{photo.description}_{user.id}'
    if cloudinary_action == 'rounding':
        r = cloudinary.uploader.upload(photo_photo, public_id=public_id, overwrite=True)
        photo_url = cloudinary.CloudinaryImage(public_id).build_url(transformation=[
            {'aspect_ratio': "1:1", 'gravity': "auto", 'width': 500, 'crop': "auto"},
            {'radius': "max"}])
    elif cloudinary_action == 'sharpen':
        r = upload(photo_photo, public_id=public_id, overwrite=True)
        photo_url = cloudinary.CloudinaryImage(public_id).build_url(effect="sharpen:150") # резкость
    elif cloudinary_action == 'repaint_the_T_shirt':
        r = upload(photo_photo, public_id=public_id, overwrite=True)
        photo_url = cloudinary.CloudinaryImage(public_id).build_url(effect="gen_recolor:prompt_t-shirt;to-color_E7E719") # перекрасить футболку
    elif cloudinary_action == 'restore':
        r = upload(photo_photo, public_id=public_id, overwrite=True)
        photo_url = cloudinary.CloudinaryImage(public_id).build_url(effect="gen_restore") # востановление
    elif cloudinary_action == 'enhance':
        r = upload(photo_photo, public_id=public_id, overwrite=True)
        photo_url = cloudinary.CloudinaryImage(public_id).build_url(effect="enhance") # усиливает
    elif cloudinary_action == 'optimization':
        r = upload(photo_photo, public_id=public_id, overwrite=True)
        photo_url = cloudinary.CloudinaryImage(public_id).build_url(transformation=[
            {'width': 1000, 'crop': "scale"},
            {'quality': "auto"},
            {'fetch_format': "auto"}])# оптимизация
    print(photo_url)
    if photo:
        photo.photo = photo_url
        db.commit()
    return photo

async def qrcode_cread(photo_id, user:Users, db: Session):
    photo = db.query(Photos).filter(Photos.id == photo_id).filter(Photos.user_id==user.id).first()
    photo_url = photo.photo
    photo_id = photo.id
    
    cloudinary.config(
        cloud_name=config.CLD_NAME,
        api_key=config.CLD_API_KEY,
        api_secret=config.CLD_API_SECRET,
        secure=True
    )

    if photo:
        qr_original = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_M,
            box_size=10,
            border=4,
            )
            
        qr_original.add_data(photo_url)
        qr_original.make(fit=True)
        folder_path = "qr_codes"
        public_id = f'{photo.description}_{user.id}'

        # Save QR 
        qr_code_original_image = qr_original.make_image(fill_color="black", back_color="white")
        qr_code_original_image_io = BytesIO()
        qr_code_original_image.save(qr_code_original_image_io, format="PNG")

        # Upload QR 
        qr_code_original_response = upload(
            qr_code_original_image_io.getvalue(),
            folder=folder_path,
            public_id=f"{folder_path}/{public_id}_qr_code",
            format="png",
            overwrite=True
            )

        qr_code_original_url = qr_code_original_response['secure_url']

        qrcode_url = db.query(Qrcode).filter(Qrcode.photo_id == photo_id).first()
        if qrcode_url:
            qrcode_url.qrcode_url =  qr_code_original_url
            db.commit()
            return qrcode_url
        else:
            qrcode_url = Qrcode(qrcode_url=qr_code_original_url, photo_id=photo_id)
            db.add(qrcode_url)
            db.commit()
            db.refresh(qrcode_url)
            return qrcode_url
    return {"error": "Image not found."}