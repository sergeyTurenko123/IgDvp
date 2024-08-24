from typing import List
from fastapi import HTTPException
from sqlalchemy.orm import Session

from src.database.models import Photos, Tag, User
from src.schemas import QuoteBase, QuoteUpdate, QuoteStatusUpdate, QuoteResponse, QuoteModel

async def get_quotes(skip: int, limit: int, db: Session) -> List[Quote]:
    return db.query(Quote).offset(skip).limit(limit).all()

async def get_quote(quote_id: int, db: Session) -> Quote:
    return db.query(Quote).filter(Quote.id == quote_id).first()

async def create_quote(body: QuoteModel, db: Session) -> Quote:
    tags = db.query(Tag).filter(Tag.id.in_(body.tags)).all()
    author = db.query(Author).filter(Author.id == body.author_id).first()
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    quote = Quote(quote=body.quote, tags=tags, author=author)
    db.add(quote)
    db.commit()
    db.refresh(quote)
    return quote


async def remove_quote(quote_id: int, db: Session) -> Quote | None:
    quote = db.query(Quote).filter(Quote.id == quote_id).first()
    if quote:
        db.delete(quote)
        db.commit()
    return quote


async def update_quote(quote_id: int, body: QuoteUpdate, db: Session) -> Quote | None:
    quote = db.query(Quote).filter(Quote.id == quote_id).first()
    if quote:
        tags = db.query(Tag).filter(Tag.id.in_(body.tags)).all()
        quote.quote = body.quote
        quote.author = body.author
        quote.tags = tags
        db.commit()
    return quote


async def update_status_quote(quote_id: int, body: QuoteStatusUpdate, db: Session) -> Quote | None:
    quote = db.query(Quote).filter(Quote.id == quote_id).first()
    if quote:
        quote.done = body.done
        db.commit()
    return quote
