from fastapi import APIRouter
from .movies import router as movies_router
from .books import router as books_router

router = APIRouter(prefix="/api/v1")

router.include_router(movies_router)
router.include_router(books_router)