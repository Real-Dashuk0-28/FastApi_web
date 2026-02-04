from fastapi import FastAPI
from models import Feedback
from pydantic import field_validator

app = FastAPI()


@field_validator("message")
@classmethod
def validate_message(cls, value:str) -> str:
    forbidden_words = ["редиска", "бяка", "козявка"]
    text_lower = value.lower()

    for word in forbidden_words:
        if word in text_lower:
            raise ValueError("Использование недопустимых слов")
    return value


feedback_storage = []

@app.post("/feedback", tags=["Отзывы пользователей"])
def create_feedback(feedback: Feedback):
    feedback_storage.append(feedback)
    return {
        "message": f"Спасибо, {feedback.name}! Ваш отзыв сохранён."
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)