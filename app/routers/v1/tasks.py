from app.routers.crud import make_router
from app.schemas.tasks import TaskCreate, TaskRead, TaskUpdate
from app.services.tasks import service

router = make_router(service, TaskCreate, TaskUpdate, TaskRead, "tasks")

