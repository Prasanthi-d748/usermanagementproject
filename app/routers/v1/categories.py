from fastapi import Depends, Response
from sqlalchemy.orm import Session

from app.database.dependencies import get_db
from app.routers.crud import make_router
from app.schemas.categories import CategoryCreate, CategoryRead, CategoryUpdate
from app.services.categories import service

router = make_router(service, CategoryCreate, CategoryUpdate, CategoryRead, "categories")


@router.get("/user/{user_id}", response_model=list[CategoryRead])
def get_categories_for_user(user_id: int, db: Session = Depends(get_db)):
    return service.get_by_user_id(db, user_id)


@router.post("/user/{user_id}", response_model=CategoryRead, status_code=201)
def create_category_for_user(user_id: int, payload: CategoryCreate, db: Session = Depends(get_db)):
    return service.create_for_user(user_id=user_id, db=db, data=payload.model_dump(exclude={"user_id"}))


@router.put("/user/{user_id}/{category_id}", response_model=CategoryRead)
def replace_user_category(
    user_id: int,
    category_id: int,
    payload: CategoryCreate,
    db: Session = Depends(get_db),
):
    return service.update_for_user(
        user_id=user_id,
        category_id=category_id,
        db=db,
        data=payload.model_dump(exclude={"user_id"}),
    )


@router.delete("/user/{user_id}/{category_id}", status_code=204)
def delete_user_category(user_id: int, category_id: int, db: Session = Depends(get_db)):
    service.delete_for_user(db, user_id, category_id)
    return Response(status_code=204)
