from LB3.modules.movie import Movie

MOVIES: list[Movie] = [
    Movie(
        slug="harry",
        title="Harry Potter",
        description="Some description",
        year=2002,
        duration=150,
    ),
    Movie(
        slug="ring",
        title="Lord's of the ring",
        description="Some description",
        year=2000,
        duration=200,
    ),
]


def get_movies() -> list[Movie]:
    return MOVIES


def create_movie(movie: Movie) -> Movie:
    MOVIES.append(movie)
    return movie
