from fastapi import HTTPException, status
from LB3.modules.book import Book
from .crud import BOOKS


def get_book_by_slug(slug: str) -> Book:
    book = next((b for b in BOOKS if b.slug == slug), None)
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with slug {slug!r} not found",
        )
    return book
