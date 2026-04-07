import unittest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from pydantic import ValidationError
from schemas.book import Book, BookCreate, BookUpdate, BookPartialUpdate


class BookCreateTestCase(unittest.TestCase):
    """Тесты для схемы BookCreate"""

    def test_book_can_be_created_from_create_schema(self):
        """Проверка создания книги из BookCreate"""
        book_in = BookCreate(
            title="Test Book",
            slug="test-book",
            description="Test description",
            pages=100
        )

        book = Book(**book_in.model_dump())

        self.assertEqual(book_in.title, book.title)
        self.assertEqual(book_in.slug, book.slug)
        self.assertEqual(book_in.description, book.description)
        self.assertEqual(book_in.pages, book.pages)

    def test_book_create_accepts_different_slug(self):
        """Проверка, что BookCreate принимает slug разной длины"""
        slugs = [
            "abc",  # 3 символа
            "valid-slug",  # 10 символов
            "a" * 30,  # 30 символов (максимум)
        ]

        for slug in slugs:
            with self.subTest(slug=slug):
                book_in = BookCreate(
                    title="Test",
                    slug=slug,
                    description="Test",
                    pages=100
                )
                self.assertEqual(slug, book_in.slug)

    def test_book_create_rejects_invalid_slug(self):
        """Проверка, что BookCreate отклоняет некорректный slug"""
        invalid_slugs = [
            "a",  # 1 символ
            "ab",  # 2 символа
            "a" * 31,  # 31 символ
            "",  # пустая строка
        ]

        for slug in invalid_slugs:
            with self.subTest(slug=slug):
                with self.assertRaises(Exception):
                    BookCreate(
                        title="Test",
                        slug=slug,
                        description="Test",
                        pages=100
                    )

    def test_pages_must_be_integer(self):
        """Проверка, что pages не может быть float"""
        invalid_pages = [0, -1, -100, 100.5, 99.9]

        for pages in invalid_pages:
            with self.subTest(pages=pages):
                with self.assertRaises(Exception):
                    BookCreate(
                        title="Test",
                        slug="test",
                        description="Test",
                        pages=pages
                    )

    # ============ ТЕСТЫ ДЛЯ ЛАБОРАТОРНОЙ РАБОТЫ №15 ============

    def test_book_slug_too_short(self):
        """ slug (меньше 3 символов) вызывает ValidationError """
        with self.assertRaises(ValidationError):
            BookCreate(
                title='test',
                slug='a',
                description='TEst description',
                pages=100,
            )
    def test_book_slug_too_long(self):
        """ slug (больше 30 символов) вызывает ValidationError """
        with self.assertRaises(ValidationError):
            BookCreate(
                title='test',
                slug='a' * 31,
                description='TEst',
                pages=100,
            )
    def test_book_slug_too_long_with_regex(self):
        """Проверка длинного slug с проверкой текста ошибки"""
        with self.assertRaisesRegex(ValidationError, "should have at most 30 characters"):
            BookCreate(
                title='test',
                slug='a' * 31,
                description='Test',
                pages=100,
            )

class BookUpdateTestCase(unittest.TestCase):
    """Тесты для схемы BookUpdate"""

    def test_book_update_changes_fields(self):
        """Проверка обновления полей книги"""
        original_book = Book(
            title="Original",
            slug="original",
            description="Original desc",
            pages=100
        )

        book_update = BookUpdate(
            title="New Title",
            description="New description",
            pages=200
        )

        # Обновляем книгу
        for field, value in book_update.model_dump().items():
            setattr(original_book, field, value)

        self.assertEqual("New Title", original_book.title)
        self.assertEqual("New description", original_book.description)
        self.assertEqual(200, original_book.pages)
        self.assertEqual("original", original_book.slug)

    def test_book_update_partial(self):
        """Проверка обновления только некоторых полей"""
        original_book = Book(
            title="Original",
            slug="original",
            description="Original desc",
            pages=100
        )

        book_partial = BookPartialUpdate(title="Updated Title")

        for field, value in book_partial.model_dump(exclude_unset=True).items():
            setattr(original_book, field, value)

        self.assertEqual("Updated Title", original_book.title)
        self.assertEqual("Original desc", original_book.description)
        self.assertEqual(100, original_book.pages)


class BookPartialUpdateTestCase(unittest.TestCase):
    """Тесты для схемы BookPartialUpdate"""

    def test_partial_update_empty(self):
        """Пустое обновление не меняет книгу"""
        original_book = Book(
            title="Original",
            slug="original",
            description="Original desc",
            pages=100
        )

        book_partial = BookPartialUpdate()

        for field, value in book_partial.model_dump(exclude_unset=True).items():
            setattr(original_book, field, value)

        self.assertEqual("Original", original_book.title)
        self.assertEqual("Original desc", original_book.description)
        self.assertEqual(100, original_book.pages)

    def test_partial_update_only_description(self):
        """Обновление только description"""
        original_book = Book(
            title="Original",
            slug="original",
            description="Original desc",
            pages=100
        )

        book_partial = BookPartialUpdate(description="New description")

        for field, value in book_partial.model_dump(exclude_unset=True).items():
            setattr(original_book, field, value)

        self.assertEqual("Original", original_book.title)
        self.assertEqual("New description", original_book.description)
        self.assertEqual(100, original_book.pages)
        self.assertEqual("original", original_book.slug)

    def test_partial_update_all_fields(self):
        """Обновление всех полей через partial update"""
        original_book = Book(
            title="Original",
            slug="original",
            description="Original desc",
            pages=100
        )

        book_partial = BookPartialUpdate(
            title="New Title",
            description="New description",
            pages=200
        )

        for field, value in book_partial.model_dump(exclude_unset=True).items():
            setattr(original_book, field, value)

        self.assertEqual("New Title", original_book.title)
        self.assertEqual("New description", original_book.description)
        self.assertEqual(200, original_book.pages)


if __name__ == "__main__":
    unittest.main()