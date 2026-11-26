from fastapi import APIRouter

from app.routers.v1 import categories, tasks, user_profiles, users

router = APIRouter()
for resource_router in (users.router, user_profiles.router, categories.router, tasks.router):
    router.include_router(resource_router)

__all__ = ["router"]
