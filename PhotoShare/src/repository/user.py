from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from libgravatar import Gravatar
from src.database.models import Photos, User
from src.schemas import UserModel


async def get_user_by_email(email: str, db: Session) -> User:
    """
    Gets user by email.
    :param email: User email.
    :type email: str
    :param db: The database session.
    :type db: Session
    """
    return db.query(User).filter(User.email == email).first()

async def update_avatar(email: str, url: str | None, db: AsyncSession) -> User:
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

async def create_user(body: UserModel, db: Session) -> User:
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
    new_user = User(**body.model_dump(), avatar=avatar)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


async def update_token(user: User, token: str | None, db: Session) -> None:
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