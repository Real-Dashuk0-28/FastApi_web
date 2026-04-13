from typing import List, Dict, Any, Optional
from models import BookCreate, Book


class BooksStorage:
    """Хранилище книг с CRUD операциями"""

    def __init__(self):
        self._books: Dict[str, Book] = {}

    def create(self, book_data: BookCreate) -> Book:
        """Создает новую книгу"""
        book = Book(**book_data.model_dump())
        self._books[book.slug] = book
        return book

    def get_list(self) -> List[Book]:
        return list(self._books.values())

    def get_by_slug(self, slug: str) -> Optional[Book]:
        """Возвращает книгу по slug или None"""
        return self._books.get(slug)

    def update(self, old_book: Book, new_book_data: BookCreate) -> Book:
        """Полностью обновляет книгу"""
        updated_book = Book(**new_book_data.model_dump())
        self._books[updated_book.slug] = updated_book
        return updated_book

    def partial_update(self, slug: str, data: Dict[str, Any]) -> Book:
        """Частично обновляет книгу"""
        if slug not in self._books:
            raise ValueError(f"Book with slug {slug} not found")

        old_book = self._books[slug]
        # Обновляем только переданные поля
        updated_data = old_book.model_dump()
        updated_data.update(data)
        updated_book = Book(**updated_data)
        self._books[slug] = updated_book
        return updated_book

    def delete(self, slug: str) -> bool:
        """Удаляет книгу по slug"""
        if slug in self._books:
            del self._books[slug]
            return True
        return False