from fastapi import Depends, Response
from sqlalchemy.orm import Session

from app.database.dependencies import get_db
from app.routers.crud import make_router
from app.schemas.categories import CategoryRead
from app.schemas.tasks import TaskRead
from app.schemas.user_details import UserDetailsRead
from app.schemas.user_details import UserDetailsCreate, UserDetailsUpdate
from app.schemas.user_profiles import ProfileRead
from app.schemas.users import UserCreate, UserRead, UserUpdate
from app.services.users import service

router = make_router(service, UserCreate, UserUpdate, UserRead, "users")


def _details_response(details):
    user, profile, categories, tasks = details
    return {
        "user": UserRead.model_validate(user),
        "profile": ProfileRead.model_validate(profile) if profile else None,
        "categories": [CategoryRead.model_validate(category) for category in categories],
        "tasks": [TaskRead.model_validate(task) for task in tasks],
    }


@router.post("/details", response_model=UserDetailsRead, status_code=201)
def create_user_details(payload: UserDetailsCreate, db: Session = Depends(get_db)):
    data = payload.model_dump()
    data["profile"] = payload.profile.model_dump(exclude={"user_id"}) if payload.profile else None
    data["categories"] = [item.model_dump(exclude={"user_id"}) for item in payload.categories]
    data["tasks"] = [item.model_dump(exclude={"user_id"}) for item in payload.tasks]
    return _details_response(service.create_details(db, data))


@router.put("/{user_id}", response_model=UserRead)
def replace_user(user_id: int, payload: UserCreate, db: Session = Depends(get_db)):
    return service.update(db, user_id, payload.model_dump())


@router.get("/{user_id}/details", response_model=UserDetailsRead)
def get_user_details(user_id: int, db: Session = Depends(get_db)):
    return _details_response(service.get_details(db, user_id))


@router.put("/{user_id}/details", response_model=UserDetailsRead)
def update_user_details(user_id: int, payload: UserDetailsUpdate, db: Session = Depends(get_db)):
    data = payload.model_dump(exclude_unset=True)
    if "profile" in data and data["profile"] is not None:
        data["profile"].pop("user_id", None)
    for field in ("categories", "tasks"):
        if field in data and data[field] is not None:
            for item in data[field]:
                item.pop("user_id", None)
    return _details_response(service.update_details(db, user_id, data))


@router.delete("/{user_id}/details", status_code=204)
def delete_user_details(user_id: int, db: Session = Depends(get_db)):
    service.delete_details(db, user_id)
    return Response(status_code=204)
