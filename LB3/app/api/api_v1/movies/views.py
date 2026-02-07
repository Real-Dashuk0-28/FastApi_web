from fastapi import APIRouter
from LB3.modules.movie import Movie, MovieCreate
from .crud import movie_storage
from .dependencies import get_movie_by_slug
from typing import Annotated
from fastapi import Depends


router = APIRouter(prefix="/movies", tags=["movies"])

@router.get("/", response_model=list[Movie])
def get_movies():
    return movie_storage.get_all()

@router.post("/", response_model=Movie)
def create_movie(movie_in: MovieCreate):
    movie = Movie(**movie_in.model_dump())
    return movie_storage.create(movie)

@router.get("/{slug}", response_model=Movie)
def get_movie(
    movie: Annotated[Movie, Depends(get_movie_by_slug)],
):
    return movie


