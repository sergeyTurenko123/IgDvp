from typing import List
from fastapi import HTTPException
from sqlalchemy.orm import Session

from src.database.models import Tag
from src.schemas import TagModel


async def get_tags(skip: int, limit: int, db: Session) -> List[Tag]:
    return db.query(Tag).offset(skip).limit(limit).all()


async def get_tag(tag_id: int, db: Session) -> Tag:
    tag = db.query(Tag).filter(Tag.id == tag_id).first()
    return tag

async def create_tag(body: TagModel, db: Session) -> Tag:
    tag1 = db.query(Tag).filter(Tag.name == body.name).first()
    if not tag1:
        tag = Tag(name=body.name)
        db.add(tag)
        db.commit()
        db.refresh(tag)
        return tag
    else:
        raise HTTPException(status_code=404, detail="tag exists")


async def update_tag(tag_id: int, body: TagModel, db: Session) -> Tag | None:
    tag = db.query(Tag).filter(Tag.id == tag_id).first()
    if tag:
        tag .name = body.name
        db.commit()
    return tag


async def remove_tag(tag_id: int, db: Session)  -> Tag | None:
    tag = db.query(Tag).filter(Tag.id == tag_id).first()
    if tag:
        db.delete(tag)
        db.commit()
    return tag
