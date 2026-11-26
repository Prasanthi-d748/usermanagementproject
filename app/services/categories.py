from fastapi import HTTPException

from app.dao.categories import dao
from app.models import User
from app.services.base import BaseService


class CategoryService(BaseService):
    def _require_user(self, db, user_id: int):
        if db.get(User, user_id) is None:
            raise HTTPException(status_code=404, detail="User not found")

    def get_by_user_id(self, db, user_id: int):
        self._require_user(db, user_id)
        return self.dao.get_by_user_id(db, user_id)

    def create_for_user(self, db, user_id: int, data: dict):
        self._require_user(db, user_id)
        data["user_id"] = user_id
        return self.dao.create(db, data)

    def update_for_user(self, db, user_id: int, category_id: int, data: dict):
        self._require_user(db, user_id)
        category = self.dao.get_one_for_user(db, user_id, category_id)
        if category is None:
            raise HTTPException(status_code=404, detail="Category not found for this user")
        data["user_id"] = user_id
        return self.dao.update(db, category, data)

    def delete_for_user(self, db, user_id: int, category_id: int):
        self._require_user(db, user_id)
        category = self.dao.get_one_for_user(db, user_id, category_id)
        if category is None:
            raise HTTPException(status_code=404, detail="Category not found for this user")
        self.dao.delete(db, category)


service = CategoryService(dao)
