from typing import Optional, List, Dict, Any
from pydantic import BaseModel


class UserSchema(BaseModel):
    username: str
    hashed_password: str
    email: str
    full_name: Optional[str] = None
    age: Optional[int] = None
    city: Optional[str] = None
    country: Optional[str] = None
    phone_number: Optional[str] = None
    is_active: bool = True


class UserResponse(BaseModel):
    message: str
    user_ids: List[int]
    result: List[Dict[UserSchema, Any]]


class UserUpdateSchema(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None
    full_name: Optional[str] = None
    age: Optional[int] = None
    city: Optional[str] = None
    country: Optional[str] = None
    phone_number: Optional[str] = None
    is_active: Optional[bool] = None
