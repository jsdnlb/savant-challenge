from typing import Optional, List, Dict, Any
from pydantic import BaseModel


class User(BaseModel):
    id: int
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
    result: List[Dict[str, Any]]
