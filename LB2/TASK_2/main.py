from fastapi import FastAPI
from models import User

app = FastAPI()

@app.post("/users", tags=["Создание пользователя"])
def create_user(user: User):
    is_adult = user.age >= 18
    return {
        "name": user.name,
        "age": user.age,
        "is_adult": is_adult
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)