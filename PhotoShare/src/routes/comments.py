#RoleAccess для захисту маршрутів у маршрутизаторах:
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from . import models, schemas
from .database import SessionLocal
from .roles import Role, RoleAccess

router = APIRouter()

allowed_operation_get = RoleAccess([Role.admin, Role.moderator, Role.user])
allowed_operation_post = RoleAccess([Role.admin, Role.moderator, Role.user])
allowed_operation_patch = RoleAccess([Role.admin, Role.moderator, Role.user])
allowed_operation_delete = RoleAccess([Role.admin, Role.moderator])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/comments/{comment_id}", response_model=schemas.Comment)
@allowed_operation_get
async def read_comment(comment_id: int, db: Session = Depends(get_db)):
    db_comment = db.query(models.Comment).filter(models.Comment.id == comment_id).first()
    if db_comment is None:
        raise HTTPException(status_code=404, detail="Comment not found")
    return db_comment

@router.post("/comments/", response_model=schemas.Comment)
@allowed_operation_post
async def create_comment(comment: schemas.CommentCreate, db: Session = Depends(get_db)):
    db_comment = models.Comment(content=comment.content, user_id=comment.user_id, photo_id=comment.photo_id)
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment

@router.patch("/comments/{comment_id}", response_model=schemas.Comment)
@allowed_operation_patch
async def update_comment(comment_id: int, comment: schemas.CommentCreate, db: Session = Depends(get_db)):
    db_comment = db.query(models.Comment).filter(models.Comment.id == comment_id).first()
    if db_comment is None:
        raise HTTPException(status_code=404, detail="Comment not found")
    if db_comment.user_id != request.state.current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to update this comment")
    db_comment.content = comment.content
    db.commit()
    db.refresh(db_comment)
    return db_comment

@router.delete("/comments/{comment_id}", response_model=schemas.Comment)
@allowed_operation_delete
async def delete_comment(comment_id: int, db: Session = Depends(get_db)):
    db_comment = db.query(models.Comment).filter(models.Comment.id == comment_id).first()
    if db_comment is None:
        raise HTTPException(status_code=404, detail="Comment not found")
    if db_comment.user_id != request.state.current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this comment")
    db.delete(db_comment)
    db.commit()
    return db_comment
