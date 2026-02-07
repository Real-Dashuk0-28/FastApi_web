from fastapi import HTTPException, status
from LB3.modules.movie import Movie
from .crud import MOVIES


def get_movie_by_slug(slug: str) -> Movie:
    movie = next((m for m in MOVIES if m.slug == slug), None)
    if not movie:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Movie with slug {slug!r} not found",
        )
    return movie
