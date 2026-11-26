from fastapi import Depends
from sqlalchemy.orm import Session

from app.database.dependencies import get_db
from app.routers.crud import make_router
from app.schemas.user_profiles import ProfileCreate, ProfileRead, ProfileUpdate
from app.services.user_profiles import service

router = make_router(service, ProfileCreate, ProfileUpdate, ProfileRead, "user-profiles")


@router.put("/{profile_id}", response_model=ProfileRead)
def replace_profile(profile_id: int, payload: ProfileCreate, db: Session = Depends(get_db)):
    return service.update(db, profile_id, payload.model_dump())
