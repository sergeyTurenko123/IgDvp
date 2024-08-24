from typing import List
import pathlib
from fastapi import APIRouter, HTTPException, Depends, status, UploadFile, File
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.schemas import QuoteModel, QuoteUpdate, QuoteStatusUpdate, QuoteResponse
from src.repository import quote as repository_quotes
from src.repository import author as repository_author
from src.database.models import Author

router = APIRouter(prefix='/quotes', tags=["quotes"])


@router.get("/", response_model=QuoteResponse)
async def read_quotes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    quotes = await repository_quotes.get_quotes(skip, limit, db)
    return quotes

@router.get("/{quote_id}", response_model=QuoteResponse)
async def read_quote(quote_id: int, db: Session = Depends(get_db)):
    quote = await repository_quotes.get_quote(quote_id, db)
    if quote is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="quote not found")
    return quote

@router.post("/uploadfile/")
async def create_upload_file(file: UploadFile = File()):
    pathlib.Path("uploads").mkdir(exist_ok=True)
    file_path = f"uploads/{file.filename}"
    with open(file_path, "wb") as f:
        f.write(await file.read())
    return {"file_path": file_path}

@router.post("/", response_model=QuoteResponse, status_code=status.HTTP_201_CREATED)
async def create_quote(body: QuoteModel, db: Session = Depends(get_db)):
    return await repository_quotes.create_quote(body, db)


@router.put("/{quote_id}", response_model=QuoteResponse)
async def update_quote(body: QuoteUpdate, quote_id: int, db: Session = Depends(get_db)):
    quote = await repository_quotes.update_quote(quote_id, body, db)
    if quote is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="quote not found")
    return quote


@router.patch("/{quote_id}", response_model=QuoteResponse)
async def update_status_quote(body: QuoteStatusUpdate, quote_id: int, db: Session = Depends(get_db)):
    quote = await repository_quotes.update_status_quote(quote_id, body, db)
    if quote is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")
    return quote


@router.delete("/{quote_id}", response_model=QuoteResponse)
async def remove_note(quote_id: int, db: Session = Depends(get_db)):
    quote = await repository_quotes.remove_quote(quote_id, db)
    if quote is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Quote not found")
    return quote
