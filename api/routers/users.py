from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from api.controllers.user import get_all_users
from api.db.database import get_db
from api.db.models import User
from api.security.authentication import get_user_disabled_current

router = APIRouter()


@router.get("/users/me")
def user(user: User = Depends(get_user_disabled_current)):
    return user


@router.get("/users/")
async def get_users(
    user: User = Depends(get_user_disabled_current),
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    return get_all_users(db, skip, limit)
