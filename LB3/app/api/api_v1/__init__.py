from fastapi import APIRouter
from api.api_v1.movies.views import router as movies_router
from api.api_v1.books.views import router as books_router


api_v1_router = APIRouter()

api_v1_router.include_router(movies_router, prefix="/movies", tags=["Movies"])
api_v1_router.include_router(books_router, prefix="/books", tags=["Books"])
