from fastapi import Depends
from sqlalchemy.orm import Session

from app.database.dependencies import get_db
from app.routers.crud import make_router
from app.schemas.categories import CategoryRead
from app.schemas.tasks import TaskRead
from app.schemas.user_details import UserDetailsRead
from app.schemas.user_profiles import ProfileRead
from app.schemas.users import UserCreate, UserRead, UserUpdate
from app.services.users import service

router = make_router(service, UserCreate, UserUpdate, UserRead, "users")


@router.put("/{user_id}", response_model=UserRead)
def replace_user(user_id: int, payload: UserCreate, db: Session = Depends(get_db)):
    return service.update(db, user_id, payload.model_dump())


@router.get("/{user_id}/details", response_model=UserDetailsRead)
def get_user_details(user_id: int, db: Session = Depends(get_db)):
    user, profile, categories, tasks = service.get_details(db, user_id)

    return {
        "user": UserRead.model_validate(user),
        "profile": ProfileRead.model_validate(profile) if profile else None,
        "categories": [CategoryRead.model_validate(category) for category in categories],
        "tasks": [TaskRead.model_validate(task) for task in tasks],
    }
