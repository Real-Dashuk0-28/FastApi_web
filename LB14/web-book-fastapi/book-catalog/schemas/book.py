from typing import Annotated
from annotated_types import MinLen, MaxLen

from pydantic import BaseModel, field_validator


class BookBase(BaseModel):
    title: str
    description: str
    pages: int


class BookCreate(BookBase):
    slug: Annotated[str, MinLen(3), MaxLen(30)]

    @field_validator('pages')
    @classmethod
    def pages_must_be_positive(cls, v: int) -> int:
        """Проверка, что количество страниц больше 0"""
        if v <= 0:
            raise ValueError('pages must be greater than 0')
        return v


class BookUpdate(BaseModel):
    """Модель для полного обновления (все поля обязательны)"""
    title: str
    description: str
    pages: int



class BookPartialUpdate(BookBase):
    """
    Модель для  частичного обновления
    """

    title: str | None = None
    description: str | None = None
    pages: int | None = None


class Book(BookBase):
    """
    Модель книги
    """

    slug: str
