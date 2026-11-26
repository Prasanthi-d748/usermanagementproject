from datetime import datetime

from pydantic import BaseModel

from app.schemas.base import ORMModel


class CategoryCreate(BaseModel):
    user_id: int | None = None
    category_name: str
    category_type: str


class CategoryUpdate(BaseModel):
    user_id: int | None = None
    category_name: str | None = None
    category_type: str | None = None


class CategoryRead(ORMModel):
    category_id: int
    user_id: int | None
    category_name: str
    category_type: str
    created_at: datetime
