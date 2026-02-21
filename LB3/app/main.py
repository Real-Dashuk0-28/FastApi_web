import uvicorn
from fastapi import FastAPI, HTTPException
from LB3.app.api import router as api_router


app = FastAPI(title="Books & Movies API")

app.include_router(api_router)


@app.get("/")
def read_root():
    return {"docs": "/docs"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
