from pydantic import BaseModel

from app.schemas.categories import CategoryRead
from app.schemas.tasks import TaskRead
from app.schemas.user_profiles import ProfileRead
from app.schemas.users import UserRead


class UserDetailsRead(BaseModel):
    user: UserRead
    profile: ProfileRead | None
    categories: list[CategoryRead]
    tasks: list[TaskRead]
