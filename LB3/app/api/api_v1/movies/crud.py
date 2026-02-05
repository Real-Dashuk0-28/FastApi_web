movies_db = {
    1: {"id": 1, "title": "Inception"},
    2: {"id": 2, "title": "Interstellar"},
}

def get_movies():
    return list(movies_db.values())

def get_movie(movie_id: int):
    return movies_db.get(movie_id)
