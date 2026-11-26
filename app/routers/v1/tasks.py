from fastapi import Depends
from sqlalchemy.orm import Session

from app.database.dependencies import get_db
from app.routers.crud import make_router
from app.schemas.tasks import TaskCreate, TaskRead, TaskUpdate
from app.services.tasks import service

router = make_router(service, TaskCreate, TaskUpdate, TaskRead, "tasks")


@router.get("/category/{category_id}", response_model=list[TaskRead])
def get_tasks_by_category(category_id: int, db: Session = Depends(get_db)):
    return service.get_by_category_id(db, category_id)

