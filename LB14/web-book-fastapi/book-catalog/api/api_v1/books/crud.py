import redis
import json
from pydantic import BaseModel
from core import config
from schemas.book import Book, BookCreate, BookUpdate, BookPartialUpdate

# Создаем Redis клиент для работы с книгами
redis_books_client = redis.Redis(
    host=config.REDIS_HOST,
    port=config.REDIS_PORT,
    db=config.REDIS_BOOKS_DB,  # ← исправлено
    decode_responses=True
)


class BooksStorage(BaseModel):
    """Хранилище книг в Redis"""

    def save_book(self, book: Book) -> None:
        """Сохраняет книгу в Redis хеш"""
        book_json = book.model_dump_json()
        redis_books_client.hset(config.REDIS_BOOKS_HASH, book.slug, book_json)

    def get(self) -> list[Book]:
        """Получает список всех книг из Redis"""
        books_json = redis_books_client.hvals(config.REDIS_BOOKS_HASH)
        books = []
        for book_json in books_json:
            books.append(Book.model_validate_json(book_json))
        return books

    def get_by_slug(self, slug: str) -> Book | None:
        """Получает книгу из Redis по slug"""
        book_json = redis_books_client.hget(config.REDIS_BOOKS_HASH, slug)
        if not book_json:
            return None
        return Book.model_validate_json(book_json)

    def create(self, book_in: BookCreate) -> Book:
        """Создает новую книгу"""
        # Проверяем, не существует ли уже книга с таким slug
        if self.get_by_slug(book_in.slug):
            raise ValueError(f"Book with slug '{book_in.slug}' already exists")

        book = Book(**book_in.model_dump())
        self.save_book(book)
        return book

    def delete_by_slug(self, slug: str) -> None:
        """Удаляет книгу из Redis по slug"""
        redis_books_client.hdel(config.REDIS_BOOKS_HASH, slug)

    def delete(self, book: Book) -> None:
        """Удаляет книгу из Redis"""
        self.delete_by_slug(slug=book.slug)

    def update(self, book: Book, book_in: BookUpdate) -> Book:
        """Полное обновление книги"""
        for field, value in book_in.model_dump().items():
            setattr(book, field, value)
        self.save_book(book)
        return book

    def partial_update(self, book: Book, book_in: BookPartialUpdate) -> Book:
        """Частичное обновление книги"""
        for field, value in book_in.model_dump(exclude_unset=True).items():
            setattr(book, field, value)
        self.save_book(book)
        return book


# Создаем экземпляр хранилища
storage = BooksStorage()