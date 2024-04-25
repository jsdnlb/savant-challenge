from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from api.controllers.user import (
    create_user,
    delete_user,
    get_all_users,
    get_user_id,
    patch_user,
    update_user,
)
from api.db.database import get_db
from api.db.models import User
from api.schemas.user import UserSchema, UserUpdateSchema
from api.security.authentication import get_user_disabled_current

router = APIRouter()


@router.get("/users/me")
def user(user: User = Depends(get_user_disabled_current)):
    return user


@router.get("/users/")
def get_users(
    skip: int = 0,
    limit: int = 100,
    user: User = Depends(get_user_disabled_current),
    db: Session = Depends(get_db),
):
    return get_all_users(db, skip, limit)


@router.get("/users/{user_id}")
def get_user(
    user_id: int,
    user: User = Depends(get_user_disabled_current),
    db: Session = Depends(get_db),
):
    return get_user_id(db, user_id)


@router.post("/users/")
def create_user_service(
    request: UserSchema,
    user: User = Depends(get_user_disabled_current),
    db: Session = Depends(get_db),
):
    return create_user(db, user=request)


@router.put("/users/{user_id}")
async def update_user_service(
    user_id: str,
    user_update: UserUpdateSchema,
    user: User = Depends(get_user_disabled_current),
    db: Session = Depends(get_db),
):
    return update_user(db, user_id, user_update)


@router.patch("/users/{user_id}")
def patch_user_service(
    user_id: int,
    user_update: UserUpdateSchema,
    user: User = Depends(get_user_disabled_current),
    db: Session = Depends(get_db),
):
    return patch_user(db, user_id, user_update)


@router.delete("/users/{user_id}")
def delete_user_service(
    user_id: int,
    user: User = Depends(get_user_disabled_current),
    db: Session = Depends(get_db),
):
    return delete_user(db, user_id)
