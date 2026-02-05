from fastapi import HTTPException, status
from .crud import get_movie

def movie_by_id(movie_id: int):
    movie = get_movie(movie_id)
    if not movie:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Movie not found"
        )
    return movie
