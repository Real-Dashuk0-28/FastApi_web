from fastapi import APIRouter, Depends
from .crud import get_movies
from .dependencies import movie_by_id

router = APIRouter()

@router.get("/")
def read_movies():
    return get_movies()

@router.get("/{movie_id}")
def read_movie(movie=Depends(movie_by_id)):
    return movie
