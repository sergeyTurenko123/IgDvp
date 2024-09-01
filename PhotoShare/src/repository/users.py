from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from libgravatar import Gravatar
from fastapi import HTTPException

from src.database.models import Users, Photos
from src.schemas import UserModel


async def get_user_by_email(email: str, db: Session) -> Users:
    """
    Gets user by email.
    :param email: User email.
    :type email: str
    :param db: The database session.
    :type db: Session
    """
    return db.query(Users).filter(Users.email == email).first()

async def update_avatar(email: str, url: str | None, db: AsyncSession) -> Users:
    """
    Updates the user's avatar.
    :param email: User email.
    :type email: str
    :param url: Image address.
    :type url: str
    :param db: The database session.
    :type db: Session
    """
    
    user = await get_user_by_email(email, db)
    user.avatar = url
    db.commit()
    return user

async def create_user(body: UserModel, db: Session) -> Users:
    """
    Creates a user.
    :param body: User data.
    :type body: str
    :param db: The database session.
    :type db: Session
    """
    avatar = None
    try:
        g = Gravatar(body.email)
        avatar = g.get_image()
    except Exception as e:
        print(e)
    new_user = Users(**body.model_dump(), avatar=avatar)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


async def update_token(user: Users, token: str | None, db: Session) -> None:
    """
    Update token.
    :param user: User data.
    :type user: str
    :param token: refresh token.
    :type token: str
    :param db: The database session.
    :type db: Session
    """
    user.refresh_token = token
    db.commit()

async def confirmed_email(email: str, db: Session) -> None:
    """
    Confirms email address.
    :param email: User email.
    :type user: str
    :param db: The database session.
    :type db: Session
    """
    user = await get_user_by_email(email, db)
    user.confirmed = True
    db.commit()

async def get_user(user_name, db: Session) -> Users:
    user = db.query(Users).filter(Users.username==user_name).first()
    # photo = db.query(Photos).filter(Photos.user_id==user_name).all()
    if not user:
        raise HTTPException(status_code=404, detail="user not found")
    return (user)