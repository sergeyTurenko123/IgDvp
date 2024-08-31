from fastapi import APIRouter, Body, Depends, status, File, Form, HTTPException
from src.schemas import PhotoResponse, CloudinarImage
from sqlalchemy.orm import Session

from src.repository import cloudinary as repository_cloudinary
from src.database.db import get_db
from src.conf.config import config
from src.database.models import Users, Tag
from src.services.auth import auth_service

router = APIRouter(prefix='/cloudinary', tags=["cloudinary"])

@router.put("/{photo_id}", response_model=PhotoResponse)
async def cloudinary_editor(
    photo_id: int,
    cloudinary_action: CloudinarImage = Body(
        openapi_examples={
            "rounding": {
                "summary": "rounding",
                "value": "rounding",
                },
            "sharpen": {
                "summary": "sharpen",
                "value": "sharpen",
            },
            "repaint_the_T_shirt": {
                "summary": "repaint_the_T_shirt",
                "value": "repaint_the_T_shirt",
            },
            "restore": {
                "summary": "restore",
                "value": "restore",
            },
            "enhance": {
                "summary": "enhance",
                "value": "enhance",
            },
            "optimization": {
                "summary": "optimization",
                "value": "optimization",
            },
        },
    ),
    db: Session = Depends(get_db), 
    current_user: Users = Depends(auth_service.get_current_user)
): 
    body = CloudinarImage(rounding=cloudinary_action.rounding, sharpen=cloudinary_action.sharpen, 
                          repaint_the_T_shirt=cloudinary_action.repaint_the_T_shirt, 
                          restore=cloudinary_action.restore, enhance=cloudinary_action.enhance, 
                          optimization=cloudinary_action.optimization)
    photo = await repository_cloudinary.cloudinary_editor(photo_id, body, current_user, db)
    if photo is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Photo not found")
    return photo