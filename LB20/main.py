from fastapi import FastAPI
from main_views import router

app = FastAPI(title="Library App", docs_url="/docs")

app.include_router(router)