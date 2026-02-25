from fastapi import APIRouter, Depends
from .api_v1 import router as api_v1_router
from LB3.app.api.dependencies import verify_token

router = APIRouter(
    prefix="/movies",
    tags=["Movies"],
    dependencies=[Depends(verify_token)],  # ← ВАЖНО
    responses={
        401: {"description": "Unauthorized"}
    }
)

router.include_router(api_v1_router)

