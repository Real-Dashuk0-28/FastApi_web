from fastapi import FastAPI
from models import Feedback, User, User_A


app = FastAPI()
user = User(
    name="John Doe",
    id=1
)

# Задание 1
@app.get("/users", tags=["Получение user"])
def get_users():
    return user

# Задание 2
@app.post("/users", tags=["Создание пользователя"])
def create_user(user: User_A):
    is_adult = user.age >= 18
    return {
        "name": user.name,
        "age": user.age,
        "is_adult": is_adult
    }

# Задание 3
feedback_storage = []

@app.post("/feedback", tags=["Отзывы пользователей"])
def create_feedback(feedback: Feedback):
    feedback_storage.append(feedback)
    return {
        "message": f"Обратная связь получена. Спасибо, {feedback.name}."
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)