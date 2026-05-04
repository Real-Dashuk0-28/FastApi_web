from pydantic import BaseModel
from typing import List, Optional


class BookCreate(BaseModel):
    title: str
    slug: str

class Book(BaseModel):
    id: int
    title: str
    slug: str


class BookAlreadyExistsError(Exception):
    """Выбрасывается, при создании книги, к-ая уже сущ"""
    pass


class BookCrud:
    def __init__(self):
        self.books: List[Book] = []
        self.next_id = 1

    def get_book_by_slug(self, slug: str) -> Optional[Book]:
        """Книгу по slug. Не найдена — None"""
        for book in self.books:
            if book.slug == slug:
                return book
        return None

    def create_book(self, book_data: BookCreate) -> Book:
        """Создаёт книгу без проверок"""
        new_book = Book(
            id=self.next_id,
            title=book_data.title,
            slug=book_data.slug
        )
        self.books.append(new_book)
        self.next_id += 1
        return new_book

    def create_or_raise_if_exists(self, book_data: BookCreate) -> Book:
        """Создаёт книгу|выбрасывает исключение, если такой slug уже есть"""
        existing = self.get_book_by_slug(book_data.slug)
        if existing:
            raise BookAlreadyExistsError(f"Book with slug '{book_data.slug}' already exists")
        return self.create_book(book_data)

    def delete_book(self, slug: str) -> bool:
        """Удаляет книгу по slug"""
        for i, book in enumerate(self.books):
            if book.slug == slug:
                self.books.pop(i)
                return True
        return False