from fastapi import HTTPException, status
from .crud import get_book

def book_by_id(book_id: int):
    book = get_book(book_id)
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found"
        )
    return book
