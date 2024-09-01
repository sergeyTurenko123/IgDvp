from typing import List

from fastapi import APIRouter, HTTPException, Depends, status, Query, Path
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.db import get_db
from src.services.auth import auth_service
from src.database.models import Users, Photos
from src.schemas import CommentBase, CommentResponse
from src.repository import comments as repository_comments
from fastapi_limiter.depends import RateLimiter


router = APIRouter(prefix='/comments')


@router.get("/comments", response_model=List[CommentResponse], 
            summary="List of all comments.",
            description="No more than 10 requests per minute.", 
            dependencies=[Depends(RateLimiter(times=2, seconds=5))])
async def read_comments(photo: Photos, skip: int = 0, limit: int = 100, db: Session = Depends(get_db),
                     current_user: Users = Depends(auth_service.get_current_user)):
    """
    Route to get the all comments list.

    Args:
        skip (int, optional): The starting position. Defaults to 0.
        limit (int, optional): The final position. Defaults to 100.
        db (Session, optional): Session to connect to DB. Defaults to Depends(get_db).
        current_user (Users, optional): Authorised user who search for a comment. Defaults to Depends(auth_service.get_current_user).

    Returns:
        List[Comments]: List with all comments.
    """
    comments = await repository_comments.get_comments(skip, limit, photo, current_user, db)
    return comments

@router.get("/comment/{comment_id}", response_model=CommentResponse,
            summary="Get a comment by it's ID.", 
            description="No more than 10 requests per minute.", 
            dependencies=[Depends(RateLimiter(times=2, seconds=5))])
async def read_comment(comment_id: int = Path(ge=1), db: AsyncSession = Depends(get_db),
                     current_user: Users = Depends(auth_service.get_current_user)):
    """
    Route to get the comment by its ID.

    Args:
        comment_id (int, optional): Comment ID of a user you want to find. Defaults to Path(ge=1).
        db (AsyncSession, optional): Session to connect to DB. Defaults to Depends(get_db).
        current_user (User, optional): Authorised user who search for a comment. Defaults to Depends(auth_service.get_current_user).

    Raises:
        HTTPException: HTTP_404_NOT_FOUND if comment is not found.

    Returns:
        Comment | None: Return comment with a specified id or None.
    """
    comment = await repository_comments.get_comment(comment_id, current_user, db)
    if comment is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="NOT FOUND")
    return comment


@router.post("/comment", response_model=CommentResponse, status_code=status.HTTP_201_CREATED, 
             summary="Add a new comment.",
             description="No more than 2 requests per minute.",
             dependencies=[Depends(RateLimiter(times=2, seconds=60))])
async def create_comment(body: CommentBase, current_photo: Photos, db: Session = Depends(get_db),
                     current_user: Users = Depends(auth_service.get_current_user)):
    """
    Route to add a new comment.

    Args:
        body (CommentBase): Containes comment details such as name, surname, email, number, bday.
        db (Session, optional): Session to connect to DB. Defaults to Depends(get_db).
        current_user (User, optional): Authorised user. Defaults to Depends(auth_service.get_current_user).

    Returns:
        Comments: Created comment.
    """
    return await repository_comments.create_comment(body, current_user, current_photo, db)


@router.put("/{comment_id}", response_model=CommentResponse,
            summary="Update an existing comment by it's ID.",
            description="Put the comment ID in comment_id line. And then put the values itself to Request body.",
            dependencies=[Depends(RateLimiter(times=2, seconds=60))])
async def update_comment(comment_id: int, body: CommentBase, db: Session = Depends(get_db),
                     current_user: Users = Depends(auth_service.get_current_user)):
    """
    Route to update the comment finded by its ID.

    Args:
        body (CommentsBase): The comment details that you want to update.
        comment_id (int): Id of a specified comment you want to apdate.
        db (Session, optional): Session to connect to DB. Defaults to Depends(get_db).
        current_user (User, optional): Authorised user who search for a comment. Defaults to Depends(auth_service.get_current_user).

    Raises:
        HTTPException: HTTP_404_NOT_FOUND if comment not found.

    Returns:
        Comment | None: Return updated comment.
    """
    comment = await repository_comments.update_comment(comment_id, body, current_user, db)
    if comment is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found!")
    return comment


@router.delete("/{comment_id}", response_model=CommentResponse, 
               summary="Delete an existing comment by it's ID.",
               description="No more than 5 requests per minute.",
             dependencies=[Depends(RateLimiter(times=5, seconds=60))])
async def remove_comment(comment_id: int, db: Session = Depends(get_db),
                     current_user: Users = Depends(auth_service.get_current_user)):
    """
    Route to delete the comment finded by its ID.

    Args:
        comment_id (int): Id of the comment you want to delete.
        db (Session, optional): Session to connect to DB. Defaults to Depends(get_db).
        current_user (User, optional): Authorised user who search for a comment. Defaults to Depends(auth_service.get_current_user).

    Raises:
        HTTPException: HTTP_404_NOT_FOUND if comment not found.

    Returns:
        Comments | None: Return deleted comment info.
    """
    comment = await repository_comments.remove_comment(comment_id, current_user, db)
    if comment is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found")
    return comment
