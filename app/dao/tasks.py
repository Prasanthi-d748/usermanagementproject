from app.dao.base import BaseDAO
from app.models import Task


class TaskDAO(BaseDAO):
    def __init__(self):
        super().__init__(Task)

    def get_by_category_id(self, db, category_id: int):
        return db.query(Task).filter(Task.category_id == category_id).all()


dao = TaskDAO()
