from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from libgravatar import Gravatar
from fastapi import HTTPException

from src.database.models import Users, Role
from src.schemas import UserModel

def dict_is_empty(data: dict) -> bool:
    return all(v is None for v in data.values())


def dict_not_empty(data: dict) -> bool:
    return any(v is not None for v in data.values())

async def get_user_by_email(email: str, db: Session) -> Users:
    """
    Retrieves a user by his email.

    :param email: An email to get user from the database by.
    :type email: str
    :param db: The database session.
    :type db: Session
    :return: The user.
    :rtype: User
    """
    query = db.query(Users).filter(Users.email == email).first()
    return query

async def is_present_admin(db: Session) -> bool:
    """search if is present admin in users
    :param db: The database session.
    :type db: Session
    :return: True if any admin is
    :rtype: bool
    """
    result = db.query(Users).filter(Users.role == Role.admin).first()
    return result is not None

async def get_user_by_username(
    username: str, db: Session) -> Users:
    """
    Retrieves a user by his username.

    :param username: An username to get user from the database by.
    :type username: str
    :param db: The database session.
    :type db: Session
    :return: The user.
    :rtype: User
    """
    user = db.query(Users).filter(Users.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="user not found")
    return user

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
    if not await is_present_admin(db):
        new_user.role = Role.admin
    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    except Exception as err:
        print(f"ERROR create_user {err}")


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

async def get_user_by_id(id: int, db: Session, active: bool | None = True) -> Users:
    """
    Retrieves a user by his id.

    :param id: An id to get user from the database by.
    :type id: int
    :param db: The database session.
    :type db: Session
    :return: The user.
    :rtype: User
    """
    query = db.query(Users).filter(Users.id == id).first()
    return query

async def update_active(user_id: int, active: bool, db: Session) -> Users:
    """
    Updates user's active state.

    :param user_id:  id of user.
    :type user_id: int
    :param active: The active state of user.
    :type active: bool
    :param db: The database session.
    :type db: Session
    :return: The user.
    :rtype: User
    """
    user = await get_user_by_id(user_id, active=not active, db=db)
    if user:
        user.active = active  # type: ignore
        db.commit()
        # clear_user_cache(user)
    return user

async def update_role_user(user_id: int, role: Role, db: Session) -> Users:
    """
    Updates user's role.

    :param user_id: id of user.
    :type user_id: int
    :param active: role of user.
    :type active: str
    :param db: The database session.
    :type db: Session
    :return: The user.
    :rtype: User
    """
    user = await get_user_by_id(user_id, db)
    if user:
        user.role = role  # type: ignore
        db.commit()
        # clear_user_cache(user)
    return user


async def update_user(user_id: int, data: dict, db: Session) -> Users | None:
    """
    Updates user's role.

    :param user_id: id of user.
    :type user_id: int
    :param active: role of user.
    :type active: str
    :param db: The database session.
    :type db: Session
    :return: The user.
    :rtype: User
    """
    user = await get_user_by_id(user_id, db, active=None)
    if user:
        if data.get("username") is not None:
            newuser: Users = await get_user_by_username(
                str(data.get("username")), db, active=None
            )
            if newuser:
                return None
            user.username = data.get("username")  # type: ignore
        if data.get("is_active") is not None:
            user.active = data.get("is_active")  # type: ignore
        if data.get("role") is not None:
            user.role = data.get("role")  # type: ignore
            db.commit()
    return user


async def delete_user(user_id: int, db: Session) -> Users:
    """
    Delete user's with not active state.

    :param user_id:  id of user.
    :type user_id: int
    :param db: The database session.
    :type db: Session
    :return: The user.
    :rtype: User
    """
    user = await get_user_by_id(user_id, active=False, db=db)
    if user:
        db.delete(user)
        db.commit()
    return user