from LB3.modules.book import Book

BOOKS: list[Book] = [
    Book(
        title="Harry Potter",
        slug="harry",
        description="Some description",
        pages=400,
    ),
    Book(
        title="Lord's of the ring",
        slug="ring",
        description="Some description",
        pages=800,
    ),
]


def get_books() -> list[Book]:
    return BOOKS


def create_book(book: Book) -> Book:
    BOOKS.append(book)
    return book
