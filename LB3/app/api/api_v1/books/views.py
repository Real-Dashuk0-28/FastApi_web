from fastapi import APIRouter, Depends
from .crud import get_books
from .dependencies import book_by_id

router = APIRouter()

@router.get("/")
def read_books():
    return get_books()

@router.get("/{book_id}")
def read_book(book=Depends(book_by_id)):
    return book
