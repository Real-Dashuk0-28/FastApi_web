from fastapi import FastAPI
from api.main_views import router

app = FastAPI()

app.include_router(router)