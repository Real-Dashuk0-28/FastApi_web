from fastapi import APIRouter, Request
from templating import templates

router = APIRouter()

@router.get("/", name="home", include_in_schema=False)
def home_page(request: Request):
    features = [
        "Поиск книг по каталогу",
        "Электронный читательский билет",
        "Бронирование книг онлайн",
        "Продление срока возврата",
        "Рекомендации по интересам"
    ]
    return templates.TemplateResponse("home.html", {"request": request, "features": features})

@router.get("/about", name="about", include_in_schema=False)
def about_page(request: Request):
    return templates.TemplateResponse("about.html", {"request": request})
