from fastapi import FastAPI
from LB3.app.api import router as api_router


app = FastAPI(title="Books & Movies API")

app.include_router(api_router)


@app.get("/")
def read_root():
    return {"docs": "/docs"}
