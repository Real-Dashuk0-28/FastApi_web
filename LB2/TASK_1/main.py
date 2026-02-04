from fastapi import FastAPI
from models import User
app = FastAPI()

user = User(
    name="John Doe",
    id=1
)

@app.get("/users")
def get_users():
    return user


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)