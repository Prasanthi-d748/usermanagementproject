from app.dao.tasks import dao
from app.services.base import BaseService


class TaskService(BaseService):
    def get_by_category_id(self, db, category_id: int):
        return self.dao.get_by_category_id(db, category_id)


service = TaskService(dao)
