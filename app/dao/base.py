from sqlalchemy.orm import Session


class BaseDAO:
    def __init__(self, model):
        self.model = model

    def create(self, db: Session, data: dict):
        item = self.model(**data)
        db.add(item)
        db.commit()
        db.refresh(item)
        return item

    def get(self, db: Session, item_id: int):
        return db.get(self.model, item_id)

    def list(self, db: Session, skip: int = 0, limit: int = 100):
        return db.query(self.model).offset(skip).limit(limit).all()

    def update(self, db: Session, item, data: dict):
        for key, value in data.items():
            setattr(item, key, value)
        db.commit()
        db.refresh(item)
        return item

    def delete(self, db: Session, item):
        db.delete(item)
        db.commit()
