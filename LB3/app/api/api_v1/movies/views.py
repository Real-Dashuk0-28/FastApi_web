from typing import Annotated
from fastapi import APIRouter, Depends

from LB3.modules.movie import Movie, MovieCreate
from .crud import get_movies, create_movie
from .dependencies import get_movie_by_slug

router = APIRouter(prefix="/movies", tags=["movies"])


@router.get("/", response_model=list[Movie])
def list_movies():
    return get_movies()


@router.post("/", response_model=Movie)
def add_movie(movie_in: MovieCreate):
    movie = Movie(**movie_in.model_dump())
    return create_movie(movie)


@router.get("/{slug}", response_model=Movie)
def movie_details(
    movie: Annotated[Movie, Depends(get_movie_by_slug)],
):
    return movie
