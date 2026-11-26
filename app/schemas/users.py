from datetime import datetime

from pydantic import BaseModel

from app.schemas.base import ORMModel


class UserCreate(BaseModel):
    full_name: str
    email: str
    password: str
    phone: str | None = None


class UserUpdate(BaseModel):
    full_name: str | None = None
    email: str | None = None
    password: str | None = None
    phone: str | None = None


class UserRead(ORMModel):
    user_id: int
    full_name: str
    email: str
    phone: str | None
    created_at: datetime
