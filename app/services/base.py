from fastapi import HTTPException


class BaseService:
    def __init__(self, dao):
        self.dao = dao

    def create(self, db, data):
        return self.dao.create(db, data)

    def get(self, db, item_id):
        item = self.dao.get(db, item_id)
        if item is None:
            raise HTTPException(status_code=404, detail="Record not found")
        return item

    def list(self, db, skip=0, limit=100):
        return self.dao.list(db, skip, limit)

    def update(self, db, item_id, data):
        return self.dao.update(db, self.get(db, item_id), data)

    def delete(self, db, item_id):
        self.dao.delete(db, self.get(db, item_id))
