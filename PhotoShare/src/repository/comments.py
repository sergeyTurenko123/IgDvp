from typing import List
from sqlalchemy import select, and_
from datetime import datetime, timedelta

from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import Comments, Photos, Users
from src.schemas import CommentBase, CommentResponse

#
async def get_comments(skip: int, limit: int, photo: Photos, db: Session) -> List[Comments]:
    """
    Return the list of all comments in the specified interval.

    Args:
        skip (int): The starting position.
        limit (int): The final position.
        user (Users): Authorised user who search for a comments.
        db (Session): Just a session to retrieve data from DB.

    Returns:
        List[Comments]: List with all comments.
    """
    return db.query(Comments).filter(Comments.photo_id == photo.id).offset(skip).limit(limit).all()

#
async def get_comment(comment_id: int, user: Users, db: AsyncSession) -> Comments | None:
    """
    Search for a comment by it's id.

    Args:
        comment_id (int): Searched comment ID.
        user (Users): User who searching.
        db (AsyncSession): Just a session to retrieve data from DB.

    Returns:
        Comments | None: Return comment with a specified id or None.
    """
    return db.query(Comments).filter(Comments.id == comment_id).first()

#
async def create_comment(body: CommentBase, user: Users, photo:Photos, db: AsyncSession) -> Comments:
    """
    Add the comment by an authorised user.

    Args:
        body (CommentBase): Containes comment details.
        user (Users): Authorised user. 
        db (AsyncSession): Session to connect the DB.

    Returns:
        Comments: Created comment.
    """
    comment = Comments(comment=body.comment, user_id=user.id, photo_id=photo.id)
    db.add(comment)
    db.commit()
    db.refresh(comment)
    return comment


async def remove_comment(comment_id: int, user: Users, db: Session) -> Comments | None:
    """
    Delete the comment by it's ID.

    Args:
        comment_id (int): Id of the comment you want to delete.
        user (Users): Authorised user who search for a comment. 
        db (Session): Session to retrieve data from DB.

    Returns:
        Comments | None: Return deleted comment info.
    """
    comment = db.query(Comments).filter(Comments.id == comment_id, user.role_id == 1).first()
    if comment:
        db.delete(comment)
        db.commit()
    return comment


async def update_comment(comment_id: int, body: CommentBase, user: Users, db: Session) -> Comments | None:
    """
    Update the details of a comment by specified ID. 

    Args:
        comment_id (int): Id of a specified comment.
        body (CommentBase): The comment details that you want to update.
        user (Users): Authorised user who search for a comment. 
        db (Session): Session to retrieve data from DB.

    Returns:
        Comments | None: Return updated comment.
    """
    comment = db.query(Comments).filter(Comments.id == comment_id, Comments.user_id == user.id).first()
    if comment:
        comment.comment=body.comment
        db.commit()
    return comment