from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root_view(name: str = "world"):
    return {
        "docs": "https://example.com/docs",
        "message": f"Hello, {name}!"
    }