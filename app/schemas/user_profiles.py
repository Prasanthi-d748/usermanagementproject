from datetime import date

from pydantic import BaseModel

from app.schemas.base import ORMModel


class ProfileCreate(BaseModel):
    user_id: int | None = None
    date_of_birth: date | None = None
    gender: str | None = None
    address: str | None = None
    city: str | None = None
    country: str | None = None
    profile_image: str | None = None


class ProfileUpdate(ProfileCreate):
    pass


class ProfileRead(ORMModel):
    profile_id: int
    user_id: int | None
    date_of_birth: date | None
    gender: str | None
    address: str | None
    city: str | None
    country: str | None
    profile_image: str | None
