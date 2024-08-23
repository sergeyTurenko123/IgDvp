from typing import List

from sqlalchemy.orm import Session

from src.database.models import Quote, Author
from src.schemas import AuthorBase, AuthorUpdate, AuthorStatusUpdate


async def get_authors(skip: int, limit: int, db: Session) -> List[Author]:
    return db.query(Author).offset(skip).limit(limit).all()


async def get_author(author_id: int, db: Session) -> Author:
    return db.query(Author).filter(Author.id == author_id).first()


async def create_author(body: AuthorBase, db: Session) -> Author:
    author = Author(fullname=body.fullname, 
                   born_date=body.born_date, 
                   born_location=body.born_location, 
                   description=body.description)
    db.add(author)
    db.commit()
    db.refresh(author)
    return author

async def remove_author(author_id: int, db: Session) -> Author | None:
    author = db.query(Author).filter(Author.id == author_id).first()
    if author:
        db.delete(author)
        db.commit()
    return author


async def update_author(author_id: int, body: AuthorUpdate, db: Session) -> Author | None:
    author = db.query(Author).filter(Author.id == author_id).first()
    if author:
        author.fullname = body.fullname
        author.born_date = body.born_date
        author.born_location = body.born_location
        author.description = body.description
        db.commit()
    return author


async def update_status_author(author_id: int, body: AuthorStatusUpdate, db: Session) -> Author | None:
    author = db.query(Quote).filter(Quote.id == author_id).first()
    if author:
        author.done = body.done
        db.commit()
    return author
