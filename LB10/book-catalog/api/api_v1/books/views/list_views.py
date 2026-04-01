from fastapi import APIRouter, status, Depends, HTTPException
from .....api.api_v1.books.crud import storage
from .....api.dependencies import user_auth_or_api_token_required
from .....schemas.book import Book, BookCreate

router = APIRouter(
    prefix="/books",
    tags=["Books"],
    dependencies=[Depends(user_auth_or_api_token_required)],
    responses={
        status.HTTP_409_CONFLICT: {
            "description": "Book with this slug already exists",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Book with slug 'harry' already exists"
                    }
                }
            }
        }
    }
)


@router.get("/", response_model=list[Book])
def get_books():
    """Получить список всех книг"""
    return storage.get()


@router.post(
    "/",
    response_model=Book,
    status_code=status.HTTP_201_CREATED,
)
def create_book(book_in: BookCreate) -> Book:
    """Создать новую книгу"""
    existing_book = storage.get_by_slug(book_in.slug)
    if existing_book:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Book with slug '{book_in.slug}' already exists"
        )
    return storage.create(book_in=book_in)