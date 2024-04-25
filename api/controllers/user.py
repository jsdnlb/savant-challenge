from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from passlib.context import CryptContext
from fastapi import HTTPException
from api.db.models import User, UserView
from api.schemas.user import UserResponse, UserSchema, UserUpdateSchema


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_all_users(db: Session, skip: int, limit: int) -> UserResponse:
    all_records = db.query(UserView).offset(skip).limit(limit).all()
    user_ids = [user.id for user in all_records]
    return {"message": "List of users", "users_ids": user_ids, "result": all_records}


def get_user_id(db: Session, user_id: int):
    _user = db.query(User).filter(User.id == user_id).first()
    if not _user:
        raise HTTPException(status_code=404, detail="User not found")
    return _user


def create_user(db: Session, user: UserSchema):
    try:
        _user = User(**user.dict())
        hash = pwd_context.hash(_user.hashed_password)
        _user.hashed_password = hash
        db.add(_user)
        db.commit()
        return _user
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail="Username or email already exists")
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Internal server error")
    finally:
        db.refresh(_user)


def update_user(db: Session, user_id: int, user_update: UserUpdateSchema):
    _user = get_user_id(db=db, user_id=user_id)

    for field, value in user_update.dict().items():
        setattr(_user, field, value)
    try:
        db.commit()
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail="Username or email already exists")
    finally:
        db.refresh(_user)

    return _user


def patch_user(db: Session, user_id: int, user_update: UserUpdateSchema):
    _user = get_user_id(db=db, user_id=user_id)

    for field, value in user_update.dict(exclude_unset=True).items():
        setattr(_user, field, value)
    db.commit()
    db.refresh(_user)

    return _user


def delete_user(db: Session, user_id: int):
    _user = get_user_id(db=db, user_id=user_id)
    db.delete(_user)
    db.commit()

    return {"message": "User deleted successfully", "user_deleted": _user}
