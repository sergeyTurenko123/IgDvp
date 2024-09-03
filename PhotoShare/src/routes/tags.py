from typing import List

from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.schemas import TagModel, TagResponse
from src.repository import tags as repository_tags

router = APIRouter(prefix='/tags', tags=["tags"])

@router.get("/", response_model=List[TagResponse], summary="Return the list of the tags.")
async def read_tags(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    tags = await repository_tags.get_tags(skip, limit, db)
    return tags


@router.get("/{tag_id}", response_model=TagResponse, summary="Return the tag with the specified id.")
async def read_tag(tag_id: int, db: Session = Depends(get_db)):
    tag = await repository_tags.get_tag(tag_id, db)
    if tag is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tag not found")
    return tag


@router.post("/", response_model=TagResponse, summary="Adds the tag.")
async def create_tag(body: TagModel, db: Session = Depends(get_db)):
    return await repository_tags.create_tag(body, db)


@router.put("/{tag_id}", response_model=TagResponse, summary="Update the tag with the specified id.")
async def update_tag(body: TagModel, tag_id: int, db: Session = Depends(get_db)):
    tag = await repository_tags.update_tag(tag_id, body, db)
    if tag is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tag not found")
    return tag


@router.delete("/{tag_id}", response_model=TagResponse, summary="Delete the tag with the specified id.")
async def remove_tag(tag_id: int, db: Session = Depends(get_db)):
    tag = await repository_tags.remove_tag(tag_id, db)
    if tag is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tag not found")
    return tag