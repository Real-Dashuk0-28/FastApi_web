from fastapi import APIRouter, Depends
from LB3.modules.movie import Movie, MovieCreate
from .crud import movie_storage
from LB3.app.security import verify_basic_auth

router = APIRouter()

@router.get("/", response_model=list[Movie])
def get_movies():
    return movie_storage.get_all()


@router.post("/", response_model=Movie)
def create_movie(
    movie_in: MovieCreate,
    username: str = Depends(verify_basic_auth)
):
    movie = Movie(**movie_in.model_dump())
    return movie_storage.create(movie)