from datetime import timedelta
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from api.security.authentication import authenticate_user
from api.security.token import create_token

router = APIRouter()


@router.post("/token", tags=["Auth and create token"])
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Logs in a user and generates a JSON Web Token (JWT) for access.

    **Parameters:**

    - `form_data` (OAuth2PasswordRequestForm): User credentials (username and password)
      passed in the request body.

    **Returns:**

    A dictionary containing:

    - `access_token` (str): The JWT access token for authenticated requests.
    - `token_type` (str): The token type, always set to "bearer" in this case.

    **Raises:**

    - Exception: If user authentication fails.
    """
    user = await authenticate_user(form_data.username, form_data.password)
    access_token_expires = timedelta(minutes=30)
    access_token_jwt = create_token({"sub": user.username}, access_token_expires)
    return {"access_token": access_token_jwt, "token_type": "bearer"}
