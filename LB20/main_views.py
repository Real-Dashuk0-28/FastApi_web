from fastapi import APIRouter, Request
from datetime import datetime
from templating import templates

router = APIRouter()


@router.get("/", include_in_schema=False)
def home_page(request: Request):
    current_year = datetime.now().year
    features = [
        "Поиск книг по каталогу",
        "Электронный читательский билет",
        "Бронирование книг онлайн",
        "Продление срока возврата",
        "Рекомендации по интересам"
    ]
    return templates.TemplateResponse(
        "home.html",
        {
            "request": request,
            "year": current_year,
            "author": "Иванова",
            "features": features
        }
    )