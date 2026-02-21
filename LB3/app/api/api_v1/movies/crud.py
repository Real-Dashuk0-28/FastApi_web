from LB3.modules.movie import Movie
from fastapi import HTTPException, status


class MovieStorage:
    def __init__(self):
        self._movies: list[Movie] = []

    def get_all(self) -> list[Movie]:
        return self._movies

    def get_by_slug(self, slug: str) -> Movie:
        for movie in self._movies:
            if movie.slug == slug:
                return movie
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Movie with slug '{slug}' not found",
        )

    def create(self, movie: Movie) -> Movie:
        self._movies.append(movie)
        return movie

    def delete(self, movie: Movie) -> None:
        self._movies.remove(movie)

    def update(self, movie: Movie, movie_in) -> Movie:
        for field, value in movie_in.model_dump().items():
            setattr(movie, field, value)
        return movie

    def partial_update(self, movie: Movie, movie_in) -> Movie:
        for field, value in movie_in.model_dump(exclude_unset=True).items():
            setattr(movie, field, value)
        return movie


movie_storage = MovieStorage()