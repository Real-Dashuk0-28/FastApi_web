import unittest
import sys
import os
import redis

# Добавляем путь к проекту
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from schemas.book import Book, BookCreate, BookUpdate, BookPartialUpdate
from api.api_v1.books.crud import storage
from core import config


class TestBookStorage(unittest.TestCase):
    """Тесты для хранения книг в Redis"""

    def setUp(self):
        """Подготовка перед каждым тестом — очищаем Redis"""
        redis_client = redis.Redis(
            host=config.REDIS_HOST,
            port=config.REDIS_PORT,
            db=config.REDIS_BOOKS_DB,
            decode_responses=True
        )
        redis_client.delete(config.REDIS_BOOKS_HASH)

    def test_create_book(self):
        """Тест создания книги"""
        book_in = BookCreate(
            title="Test Book",
            slug="test-book",
            description="Test description",
            pages=100
        )

        book = storage.create(book_in)

        self.assertEqual(book.title, "Test Book")
        self.assertEqual(book.slug, "test-book")
        self.assertEqual(book.description, "Test description")
        self.assertEqual(book.pages, 100)

        # Проверяем, что книга сохранилась в Redis
        saved_book = storage.get_by_slug("test-book")
        self.assertIsNotNone(saved_book)
        self.assertEqual(saved_book.title, "Test Book")

    def test_get_all_books(self):
        """Тест получения всех книг"""
        storage.create(BookCreate(
            title="Book 1",
            slug="book-1",
            description="First",
            pages=100
        ))

        storage.create(BookCreate(
            title="Book 2",
            slug="book-2",
            description="Second",
            pages=200
        ))

        books = storage.get()

        self.assertEqual(len(books), 2)
        slugs = [b.slug for b in books]
        self.assertIn("book-1", slugs)
        self.assertIn("book-2", slugs)

    def test_get_by_slug(self):
        """Тест получения книги по slug"""
        storage.create(BookCreate(
            title="Test Book",
            slug="test-book",
            description="Test",
            pages=100
        ))

        book = storage.get_by_slug("test-book")

        self.assertIsNotNone(book)
        self.assertEqual(book.title, "Test Book")

    def test_get_by_slug_not_found(self):
        """Тест получения несуществующей книги"""
        book = storage.get_by_slug("non-existent")
        self.assertIsNone(book)

    def test_delete_by_slug(self):
        """Тест удаления книги по slug"""
        storage.create(BookCreate(
            title="Test Book",
            slug="test-book",
            description="Test",
            pages=100
        ))

        storage.delete_by_slug("test-book")

        self.assertIsNone(storage.get_by_slug("test-book"))
        self.assertEqual(len(storage.get()), 0)

    def test_delete_book_object(self):
        """Тест удаления книги по объекту"""
        book = storage.create(BookCreate(
            title="Test Book",
            slug="test-book",
            description="Test",
            pages=100
        ))

        storage.delete(book)

        self.assertIsNone(storage.get_by_slug("test-book"))

    def test_update_book(self):
        """Тест полного обновления книги"""
        original = storage.create(BookCreate(
            title="Original",
            slug="original",
            description="Original desc",
            pages=100
        ))

        book_update = BookUpdate(
            title="Updated",
            description="Updated desc",
            pages=200
        )

        updated = storage.update(original, book_update)

        self.assertEqual(updated.title, "Updated")
        self.assertEqual(updated.description, "Updated desc")
        self.assertEqual(updated.pages, 200)
        self.assertEqual(updated.slug, "original")

        # Проверяем, что изменения сохранились в Redis
        saved = storage.get_by_slug("original")
        self.assertEqual(saved.title, "Updated")

    def test_partial_update_book(self):
        """Тест частичного обновления книги"""
        original = storage.create(BookCreate(
            title="Original",
            slug="original",
            description="Original desc",
            pages=100
        ))

        book_partial = BookPartialUpdate(description="New description")

        updated = storage.partial_update(original, book_partial)

        self.assertEqual(updated.title, "Original")
        self.assertEqual(updated.description, "New description")
        self.assertEqual(updated.pages, 100)
        self.assertEqual(updated.slug, "original")

    def test_partial_update_empty(self):
        """Тест пустого частичного обновления"""
        original = storage.create(BookCreate(
            title="Original",
            slug="original",
            description="Original desc",
            pages=100
        ))

        book_partial = BookPartialUpdate()

        updated = storage.partial_update(original, book_partial)

        self.assertEqual(updated.title, "Original")
        self.assertEqual(updated.description, "Original desc")
        self.assertEqual(updated.pages, 100)


class TestBookSlugConstraints(unittest.TestCase):
    """Тесты для проверки ограничений slug"""

    def setUp(self):
        """Подготовка перед каждым тестом"""
        redis_client = redis.Redis(
            host=config.REDIS_HOST,
            port=config.REDIS_PORT,
            db=config.REDIS_BOOKS_DB,
            decode_responses=True
        )
        redis_client.delete(config.REDIS_BOOKS_HASH)

    def test_valid_slugs(self):
        """Проверка корректных slug"""
        valid_slugs = [
            "abc",
            "valid-slug",
            "a" * 30,
            "test-123",
            "my_book",
        ]

        for slug in valid_slugs:
            with self.subTest(slug=slug):
                book = storage.create(BookCreate(
                    title="Test",
                    slug=slug,
                    description="Test",
                    pages=100
                ))
                self.assertEqual(book.slug, slug)

    def test_invalid_slugs(self):
        """Проверка некорректных slug"""
        invalid_slugs = [
            "a", "ab", "a" * 31, ""
        ]

        for slug in invalid_slugs:
            with self.subTest(slug=slug):
                with self.assertRaises(Exception):
                    storage.create(BookCreate(
                        title="Test",
                        slug=slug,
                        description="Test",
                        pages=100
                    ))


class TestBookPagesConstraints(unittest.TestCase):
    """Тесты для проверки ограничений pages"""

    def setUp(self):
        """Подготовка перед каждым тестом"""
        redis_client = redis.Redis(
            host=config.REDIS_HOST,
            port=config.REDIS_PORT,
            db=config.REDIS_BOOKS_DB,
            decode_responses=True
        )
        redis_client.delete(config.REDIS_BOOKS_HASH)

    def test_valid_pages(self):
        """Проверка корректных значений pages"""
        valid_pages = [1, 10, 100, 1000, 10000]

        for pages in valid_pages:
            with self.subTest(pages=pages):
                book = storage.create(BookCreate(
                    title="Test",
                    slug=f"test-{pages}",
                    description="Test",
                    pages=pages
                ))
                self.assertEqual(book.pages, pages)

    def test_invalid_pages(self):
        """Проверка некорректных значений pages"""
        invalid_pages = [0, -1, -100, 100.5, 99.9]

        for pages in invalid_pages:
            with self.subTest(pages=pages):
                with self.assertRaises(Exception):
                    storage.create(BookCreate(
                        title="Test",
                        slug=f"test-{pages}",
                        description="Test",
                        pages=pages
                    ))


if __name__ == "__main__":
    unittest.main()