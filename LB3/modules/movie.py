from typing import Annotated, Optional
from annotated_types import MinLen, MaxLen
from pydantic import BaseModel


class MovieBase(BaseModel):
    title: str
    slug: str
    description: str
    year: int
    duration: int


class MovieCreate(MovieBase):
    slug: Annotated[str, MinLen(3), MaxLen(30)]


class Movie(MovieBase):
    pass


class MovieUpdate(MovieBase):
    pass


class MoviePartialUpdate(BaseModel):
    title: Optional[str] = None
    slug: Optional[str] = None
    description: Optional[str] = None
    year: Optional[int] = None
    duration: Optional[int] = None