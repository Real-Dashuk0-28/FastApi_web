import pytest
from collections.abc import Generator
from crud import BookCrud, BookCreate, BookAlreadyExistsError


@pytest.fixture
def simple_crud():
    return BookCrud()

@pytest.fixture
def crud_with_cleanup() -> Generator[BookCrud, None, None]:
    """Создаёт CRUD ДО теста и удаляет книги ПОСЛЕ теста"""

    print("\n[Setup] Создаю новый BookCrud...")
    crud = BookCrud()

    yield crud

    print("[Teardown] Очищаю данные после теста...")
    crud.books.clear()
    crud.next_id = 1


# ============================================
# Тест на исключение
# ============================================

def test_create_or_raise_if_exists_exception():
    """Попытка создать дубликат выбрасывается исключение"""

    crud = BookCrud()

    book1 = BookCreate(title="Война и мир", slug="voyna-i-mir")
    crud.create_book(book1)

    book2 = BookCreate(title="Война и мир 2", slug="voyna-i-mir")

    with pytest.raises(BookAlreadyExistsError) as exc_info:
        crud.create_or_raise_if_exists(book2)

    assert "voyna-i-mir" in str(exc_info.value)


# ============================================
# Тест с использованием фикстуры
# ============================================

def test_create_or_raise_if_exists_success(simple_crud):
    """Создание новой книги (не дубл) работает нормально"""

    new_book = BookCreate(title="Мастер и Маргарита", slug="master-i-margarita")

    result = simple_crud.create_or_raise_if_exists(new_book)

    assert result.title == "Мастер и Маргарита"
    assert result.slug == "master-i-margarita"
    assert result.id == 1


# ============================================
# Тест с фикстурой-генератором с autо-очисткой
# ============================================

def test_with_cleanup_fixture(crud_with_cleanup):
    book = BookCreate(title="Тестовая книга", slug="test-book")
    crud_with_cleanup.create_book(book)

    assert len(crud_with_cleanup.books) == 1
    assert crud_with_cleanup.books[0].slug == "test-book"

