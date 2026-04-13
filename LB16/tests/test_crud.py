import unittest
from models import BookCreate
from storage.crud import BooksStorage


class BooksStorageUpdateTestCase(unittest.TestCase):

    def setUp(self):
        self.storage = BooksStorage()
        self.book = self.create_book()

    def tearDown(self):
        self.storage.delete(self.book.slug)

    def create_book(self):
        book_data = BookCreate(
            slug="test-slug",
            title="Test Book",
            description="Original description",
            author="Test Author"
        )
        return self.storage.create(book_data)

    def test_update(self):
        """Тест полного обновления книги"""
        book_update = BookCreate(
            slug="test-slug",
            title="Test Book",
            description="Updated description",
            author="Test Author"
        )

        # Выполняем обновление
        updated_book = self.storage.update(self.book, book_update)

        # Проверки
        self.assertNotEqual(self.book.description, updated_book.description)
        self.assertEqual(updated_book.description, book_update.description)

    def test_partial_update(self):
        """Тест частичного обновления"""
        partial_data = {"description": "Partially updated description"}

        # Выполняем частичное обновление
        updated_book = self.storage.partial_update(self.book.slug, partial_data)

        # Проверки
        self.assertEqual(updated_book.description, partial_data["description"])
        # Остальные поля не изменились
        self.assertEqual(updated_book.title, self.book.title)


class BooksStorageListTestCase(unittest.TestCase):
    """Тесты для получения списка книг и получения по slug"""

    @classmethod
    def setUpClass(cls):
        cls.storage = BooksStorage()
        cls.books = []

        test_books_data = [
            ("book-1", "First Book", "Description for book 1"),
            ("book-2", "Second Book", "Description for book 2"),
            ("book-3", "Third Book", "Description for book 3"),
        ]

        for slug, title, description in test_books_data:
            book_data = BookCreate(
                slug=slug,
                title=title,
                description=description,
                author="Test Author"
            )
            book = cls.storage.create(book_data)
            cls.books.append(book)

    @classmethod
    def tearDownClass(cls):
        for book in cls.books:
            cls.storage.delete(book.slug)

    def test_get_list(self):
        """Проверяет, что при запросе списка книг возвращаются все созданные сущности"""
        books_list = self.storage.get_list()

        for book in self.books:
            self.assertIn(book, books_list)

        self.assertEqual(len(books_list), len(self.books))

    def test_get_by_slug(self):
        """Проверяет, что можно получить книгу по slug"""
        for book in self.books:
            with self.subTest(book_slug=book.slug):
                # subTest позволяет продолжить выполнение даже при падении одного теста
                found_book = self.storage.get_by_slug(book.slug)

                # Проверяем, что найденная книга соответствует ожидаемой
                self.assertEqual(found_book.slug, book.slug)
                self.assertEqual(found_book.title, book.title)
                self.assertEqual(found_book.description, book.description)
                self.assertEqual(found_book.author, book.author)