import hashlib
import secrets

from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError

from app.dao.users import dao
from app.models import User
from app.models import Category, Task, UserProfile
from app.services.base import BaseService


def hash_password(password: str) -> str:
    salt = secrets.token_hex(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode(), salt.encode(), 310_000).hex()
    return f"pbkdf2_sha256${salt}${digest}"


class UserService(BaseService):
    def get_details(self, db, user_id: int):
        details = self.dao.get_user_details(db, user_id)
        if details is None:
            raise HTTPException(status_code=404, detail="Record not found")
        return details

    def create_details(self, db, data):
        user = self.create(db, data["user"])
        user_id = user.user_id
        try:
            if data.get("profile") is not None:
                db.add(UserProfile(user_id=user_id, **data["profile"]))
            db.add_all([Category(user_id=user_id, **item) for item in data.get("categories", [])])
            db.add_all([Task(user_id=user_id, **item) for item in data.get("tasks", [])])
            db.commit()
        except Exception:
            db.rollback()
            raise
        return self.get_details(db, user_id)

    def update_details(self, db, user_id: int, data):
        self.get(db, user_id)
        if data.get("user"):
            self.update(db, user_id, data["user"])
        if "profile" in data and data["profile"] is not None:
            profile = db.query(UserProfile).filter(UserProfile.user_id == user_id).first()
            values = data["profile"]
            if profile is None:
                db.add(UserProfile(user_id=user_id, **values))
            else:
                for key, value in values.items():
                    setattr(profile, key, value)
        for field, model in (("categories", Category), ("tasks", Task)):
            if field in data and data[field] is not None:
                db.query(model).filter(model.user_id == user_id).delete(synchronize_session=False)
                db.add_all([model(user_id=user_id, **item) for item in data[field]])
        db.commit()
        return self.get_details(db, user_id)

    def delete_details(self, db, user_id: int):
        user = self.get(db, user_id)
        db.query(Task).filter(Task.user_id == user_id).delete(synchronize_session=False)
        db.query(Category).filter(Category.user_id == user_id).delete(synchronize_session=False)
        db.query(UserProfile).filter(UserProfile.user_id == user_id).delete(synchronize_session=False)
        db.delete(user)
        db.commit()

    def create(self, db, data):
        if db.query(User).filter(User.email == data["email"]).first():
            raise HTTPException(status_code=409, detail="A user with this email already exists")
        data["password"] = hash_password(data["password"])
        try:
            return super().create(db, data)
        except IntegrityError as exc:
            db.rollback()
            raise HTTPException(status_code=409, detail="A user with this email already exists") from exc

    def update(self, db, item_id, data):
        if "email" in data and db.query(User).filter(User.email == data["email"], User.user_id != item_id).first():
            raise HTTPException(status_code=409, detail="A user with this email already exists")
        if data.get("password"):
            data["password"] = hash_password(data["password"])
        try:
            return super().update(db, item_id, data)
        except IntegrityError as exc:
            db.rollback()
            raise HTTPException(status_code=409, detail="A user with this email already exists") from exc


service = UserService(dao)
