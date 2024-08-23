from typing import List

from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.schemas import AuthorResponse, AuthorBase, AuthorStatusUpdate
from src.repository import author as repository_author

router = APIRouter(prefix='/author', tags=["author"])

@router.get("/", response_model=List[AuthorResponse])
async def read_authors(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    authors = await repository_author.get_authors(skip, limit, db)
    return authors


@router.get("/{author_id}", response_model=AuthorResponse)
async def read_author(author_id: int, db: Session = Depends(get_db)):
    author = await repository_author.get_author(author_id, db)
    if author is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Author not found")
    return author


@router.post("/", response_model=AuthorResponse)
async def create_author(body: AuthorBase, db: Session = Depends(get_db)):
    return await repository_author.create_author(body, db)


@router.put("/{author_id}", response_model=AuthorResponse)
async def update_author(body: AuthorBase, author_id: int, db: Session = Depends(get_db)):
    author = await repository_author.update_author(author_id, body, db)
    if author is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="author not found")
    return author


@router.patch("/{author_id}", response_model=AuthorResponse)
async def update_status_author(body: AuthorStatusUpdate, author_id: int, db: Session = Depends(get_db)):
    author = await repository_author.update_status_author(author_id, body, db)
    if author is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Author not found")
    return author


@router.delete("/{author_id}", response_model=AuthorResponse)
async def remove_author(author_id: int, db: Session = Depends(get_db)):
    author = await repository_author.remove_author(author_id, db)
    if author is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Author not found")
    return author
