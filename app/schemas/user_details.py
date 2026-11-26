from pydantic import BaseModel, Field

from app.schemas.categories import CategoryCreate, CategoryRead
from app.schemas.tasks import TaskCreate, TaskRead
from app.schemas.user_profiles import ProfileCreate, ProfileRead, ProfileUpdate
from app.schemas.users import UserCreate, UserRead, UserUpdate


class UserDetailsRead(BaseModel):
    user: UserRead
    profile: ProfileRead | None
    categories: list[CategoryRead]
    tasks: list[TaskRead]


class UserDetailsCreate(BaseModel):
    user: UserCreate
    profile: ProfileCreate | None = None
    categories: list[CategoryCreate] = Field(default_factory=list)
    tasks: list[TaskCreate] = Field(default_factory=list)


class UserDetailsUpdate(BaseModel):
    user: UserUpdate | None = None
    profile: ProfileUpdate | None = None
    categories: list[CategoryCreate] | None = None
    tasks: list[TaskCreate] | None = None
