from fastapi import APIRouter
from .views import router as books_views_router

router = APIRouter(prefix="/books", tags=["books"])

router.include_router(books_views_router)