from fastapi import APIRouter, Body, Depends, status, HTTPException
from sqlalchemy.orm import Session

from src.schemas import PhotoResponse, CloudinarImage, QrcodeResponse
from src.repository import cloudinary as repository_cloudinary
from src.database.db import get_db
from src.database.models import Users
from src.services.auth import auth_service

router = APIRouter(prefix='/cloudinary', tags=["cloudinary"])

@router.put("/{photo_id}", response_model=PhotoResponse)
async def cloudinary_editor(
    photo_id: int,
    cloudinary_action: CloudinarImage = Body(
        openapi_examples={
            "1": {
                "summary": "rounding",
                "value": {"rounding":"rounding"},
                },
            "2": {
                "summary": "sharpen",
                "value": {"sharpen":"sharpen"},
            },
            "3": {
                "summary": "repaint_the_T_shirt",
                "value": {"repaint_the_T_shirt":"repaint_the_T_shirt"},
            },
            "4": {
                "summary": "restore",
                "value": {"restore":"restore"},
            },
            "5": {
                "summary": "enhance",
                "value": {"enhance":"enhance"},
            },
            "6": {
                "summary": "optimization",
                "value": {"optimization":"optimization"},
            },
        },
    ),
    db: Session = Depends(get_db), 
    current_user: Users = Depends(auth_service.get_current_user)
):
    for val in cloudinary_action:
        if val.count(None) == 0:
            body = val
            photo = await repository_cloudinary.cloudinary_editor(photo_id, body[1], current_user, db)
            if photo is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Photo not found")
            return photo

@router.get("/{photo_id}", response_model=QrcodeResponse)
async def qrcode_cread(
    photo_id: int,
    db: Session = Depends(get_db), 
    current_user: Users = Depends(auth_service.get_current_user)):
    img = await repository_cloudinary.qrcode_cread(photo_id, current_user, db)
    return img      