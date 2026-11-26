from app.dao.base import BaseDAO
from app.models import Category


class CategoryDAO(BaseDAO):
    def __init__(self):
        super().__init__(Category)

    def get_by_user_id(self, db, user_id: int):
        return db.query(Category).filter(Category.user_id == user_id).all()

    def get_one_for_user(self, db, user_id: int, category_id: int):
        return db.query(Category).filter(
            Category.user_id == user_id,
            Category.category_id == category_id,
        ).first()


dao = CategoryDAO()
