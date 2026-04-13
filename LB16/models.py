from pydantic import BaseModel, Field, field_validator


class BookCreate(BaseModel):
    """Модель для создания книги"""
    slug: str = Field(..., min_length=3, max_length=30)
    title: str
    description: str
    author: str

    @field_validator('slug')
    def validate_slug(cls, v: str) -> str:
        if len(v) < 3:
            raise ValueError('slug too short')
        if len(v) > 30:
            raise ValueError('slug too long')
        return v


class Book(BookCreate):
    pass