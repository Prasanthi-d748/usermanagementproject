from app.dao.base import BaseDAO
from app.models import Category, Task, User, UserProfile


class UserDAO(BaseDAO):
    def __init__(self):
        super().__init__(User)

    def get_user_details(self, db, user_id: int):
        user = db.get(User, user_id)
        if user is None:
            return None

        profile = db.query(UserProfile).filter(UserProfile.user_id == user_id).first()
        categories = db.query(Category).filter(Category.user_id == user_id).all()
        tasks = db.query(Task).filter(Task.user_id == user_id).all()
        return user, profile, categories, tasks


dao = UserDAO()
