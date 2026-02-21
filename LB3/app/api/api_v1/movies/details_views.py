from typing import Annotated
from fastapi import APIRouter, Depends, status
from LB3.modules.movie import Movie, MovieUpdate, MoviePartialUpdate
from .crud import movie_storage
from .dependencies import get_movie_by_slug

router = APIRouter()

movie_dependency = Annotated[Movie, Depends(get_movie_by_slug)]


@router.get("/{slug}/", response_model=Movie)
def get_movie(movie: movie_dependency):
    return movie


@router.delete(
    "/{slug}/",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_movie(movie: movie_dependency):
    movie_storage.delete(movie)


@router.put("/{slug}/", response_model=Movie)
def update_movie(
    movie_in: MovieUpdate,
    movie: movie_dependency
):
    return movie_storage.update(movie, movie_in)


@router.patch("/{slug}/", response_model=Movie)
def partial_update_movie(
    movie_in: MoviePartialUpdate,
    movie: movie_dependency
):
    return movie_storage.partial_update(movie, movie_in)