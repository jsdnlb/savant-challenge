from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from api.utils.exception_handler import exception_handler
from core.config import SECRET, ALGORITHM
from passlib.context import CryptContext
from api.db.models import User
from api.db.database import SessionLocal

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
session_db = SessionLocal()


def verify_password(plane_password, hashed_password):
    return pwd_context.verify(plane_password, hashed_password)


async def authenticate_user(username: str, password: str):
    user = session_db.query(User).filter(User.username == username).first()
    if user and verify_password(password, user.hashed_password):
        return user
    raise exception_handler("401_INVALID_CREDENTIALS")


def get_user_current(token: str = Depends(oauth2_scheme)):
    token_decode = jwt.decode(token, key=[SECRET], algorithms=[ALGORITHM])
    username = token_decode.get("sub")

    try:
        token_decode = jwt.decode(token, key=[SECRET], algorithms=[ALGORITHM])
        username = token_decode.get("sub")
        if username == None:
            raise exception_handler("401_INVALID_CREDENTIALS")
    except JWTError:
        raise exception_handler("401_INVALID_CREDENTIALS")

    user = session_db.query(User).filter(User.username == username).first()
    if not user:
        raise exception_handler("401_INVALID_CREDENTIALS")
    return user


def get_user_disabled_current(user: User = Depends(get_user_current)):
    if user.is_active == False:
        raise exception_handler("400_INACTIVE_USER")
    return user
