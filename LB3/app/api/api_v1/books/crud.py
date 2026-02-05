books_db = {
    1: {"id": 1, "title": "1984"},
    2: {"id": 2, "title": "Brave New World"},
}

def get_books():
    return list(books_db.values())

def get_book(book_id: int):
    return books_db.get(book_id)
