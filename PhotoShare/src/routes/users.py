from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, Path, status
from sqlalchemy.orm import Session
import cloudinary
import cloudinary.uploader
from cloudinary import CloudinaryImage

from src.conf import messages
from src.database.db import get_db
from src.database.models import Users, Role
from src.repository import users as repository_user
from src.services.auth import auth_services
from src.conf.config import config
from src.schemas import UserDb, User_Photo, UpdateFullProfile
from src.services.role import RoleAccess

router = APIRouter(prefix="/users", tags=["users"])

allowed_operations_modify = RoleAccess([Role.admin])
allowed_operations_bans = RoleAccess([Role.admin])
allowed_operations_delete = RoleAccess([Role.admin])
allowed_operations_admin = RoleAccess([Role.admin])

@router.get("/{user_name}", response_model=User_Photo)
async def read_user_name(user_name: str, db: Session = Depends(get_db)):
    user = await repository_user.get_user_by_username(user_name, db)
    return user

@router.get("/me/", response_model=UserDb)
async def read_users_me(user: Users = Depends(auth_services.get_current_user)):
    return user

@router.patch('/avatar', response_model=UserDb)
async def update_avatar_user(
    file: UploadFile = File(), 
    user: Users = Depends(auth_services.get_current_user),
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

@router.patch(
    "/{user_id}",
    dependencies=[Depends(allowed_operations_modify)],
    status_code=status.HTTP_200_OK,
    response_description=messages.USER_ACCEPTED,
    name="Change user's data",
)
async def update_user(
    data: UpdateFullProfile,
    user_id: int = Path(gt=0),
    owner: Users = Depends(auth_services.get_current_user),
    db: Session = Depends(get_db),
):
    """Update user data by their ID, Allowed only for Admin.

    :param user_id: id of user
    :type user_id: int
    :param owner: _description_, defaults to Depends(auth_service.get_current_user)
    :type owner: User, optional
    :param db: _description_, defaults to Depends(get_db)
    :type db: Session, optional
    """
    
    if owner.id == user_id:  # type: ignore
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=messages.USER_CANT_OPERATE_HIMSELF,
        )
    data_dict = data.model_dump()
    if repository_user.dict_not_empty(data_dict):
        user = await repository_user.update_user(user_id, data=data_dict, db=db)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=messages.USER_NOT_FOUND
            )
        return {"detail": messages.USER_ACCEPTED}
    raise HTTPException(
        status_code=status.HTTP_304_NOT_MODIFIED, detail=messages.USER_NOT_CHANGED
    )


@router.delete(
    "/{user_id}",
    dependencies=[Depends(allowed_operations_delete)],
    status_code=status.HTTP_200_OK,
    response_description="accepted",
    name="Delete user",
)
async def delete_user(
    user_id: int = Path(gt=0),
    owner: Users = Depends(auth_services.get_current_user),
    db: Session = Depends(get_db),
):
    """Delete user by their ID, with not active state.  Allowed for roles: admin.

    :param user_id: id of user
    :type user_id: int
    :param owner: _description_, defaults to Depends(auth_service.get_current_user)
    :type owner: User, optional
    :param db: _description_, defaults to Depends(get_db)
    :type db: Session, optional
    """
    if owner.id == user_id:  # type: ignore
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Can't operate with himself",
        )
    user = await repository_user.delete_user(user_id, db=db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=messages.USER_NOT_FOUND
        )
    return {"detail": messages.USER_ACCEPTED}