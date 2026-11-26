import hashlib
import secrets

from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError

from app.dao.users import dao
from app.models import User
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
