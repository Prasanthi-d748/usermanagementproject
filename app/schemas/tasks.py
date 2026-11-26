from datetime import date, datetime

from pydantic import BaseModel

from app.schemas.base import ORMModel


class TaskCreate(BaseModel):
    user_id: int | None = None
    category_id: int | None = None
    task_title: str
    description: str | None = None
    priority: str | None = "Medium"
    status: str | None = "Pending"
    due_date: date | None = None


class TaskUpdate(BaseModel):
    user_id: int | None = None
    category_id: int | None = None
    task_title: str | None = None
    description: str | None = None
    priority: str | None = None
    status: str | None = None
    due_date: date | None = None


class TaskRead(ORMModel):
    task_id: int
    user_id: int | None
    category_id: int | None
    task_title: str
    description: str | None
    priority: str | None
    status: str | None
    due_date: date | None
    created_at: datetime
