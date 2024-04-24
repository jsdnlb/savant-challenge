from sqlalchemy.orm import Session
from api.db.models import User, UserView
from api.models.user import UserResponse


def get_all_users(db: Session, skip: int, limit: int) -> UserResponse:
    all_records = db.query(UserView).offset(skip).limit(limit).all()
    user_ids = [user.id for user in all_records]
    return {"message": "List of users", "users_ids": user_ids, "result": all_records}
