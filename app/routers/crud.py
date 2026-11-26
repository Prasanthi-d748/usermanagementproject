from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session

from app.database.dependencies import get_db


def make_router(service, create_schema, update_schema, read_schema, path: str):
    router = APIRouter(prefix=f"/{path}", tags=[path.replace("-", " ").title()])

    @router.post("/", response_model=read_schema, status_code=201)
    def create(payload: create_schema, db: Session = Depends(get_db)):
        return service.create(db, payload.model_dump())

    @router.get("/", response_model=list[read_schema])
    def list_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
        return service.list(db, skip, min(limit, 100))

    @router.get("/{item_id}", response_model=read_schema)
    def get_item(item_id: int, db: Session = Depends(get_db)):
        return service.get(db, item_id)

    @router.patch("/{item_id}", response_model=read_schema)
    def update(item_id: int, payload: update_schema, db: Session = Depends(get_db)):
        return service.update(db, item_id, payload.model_dump(exclude_unset=True))

    @router.delete("/{item_id}", status_code=204)
    def delete(item_id: int, db: Session = Depends(get_db)):
        service.delete(db, item_id)
        return Response(status_code=204)

    return router
