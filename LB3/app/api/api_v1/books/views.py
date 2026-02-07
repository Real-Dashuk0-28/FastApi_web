from typing import Annotated
from fastapi import APIRouter, Depends

from LB3.modules.book import Book, BookCreate
from .crud import get_books, create_book
from .dependencies import get_book_by_slug

router = APIRouter(prefix="/books", tags=["books"])


@router.get("/", response_model=list[Book])
def list_books():
    return get_books()


@router.post("/", response_model=Book)
def add_book(book_in: BookCreate):
    book = Book(**book_in.model_dump())
    return create_book(book)


@router.get("/{slug}", response_model=Book)
def book_details(
    book: Annotated[Book, Depends(get_book_by_slug)],
):
    return book
