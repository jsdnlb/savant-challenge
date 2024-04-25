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


@router.get("/users/me", tags=["Users"])
def user(user: User = Depends(get_user_disabled_current)):
    """
    Retrieves the currently authenticated user's information.

    **Parameters:**

    - `user` (User): The authenticated user object obtained from the dependency.

    **Returns:**

    A dictionary representation of the user object, containing relevant user information.

    **Raises:**

    - Exception: If user authentication fails or the user is disabled.

    **Notes:**

    - This endpoint requires a valid access token in the authorization header for authentication.
    - The specific user information returned depends on the structure of your `User` model.
    """
    return user


@router.get("/users/", tags=["Users"])
def get_users(
    skip: int = 0,
    limit: int = 100,
    user: User = Depends(get_user_disabled_current),
    db: Session = Depends(get_db),
):
    """
    Retrieves a paginated list of users.

    **Parameters:**

    - `skip` (int, optional): Number of users to skip in the results (defaults to 0).
    - `limit` (int, optional): Maximum number of users to return (defaults to 100).
    - `user` (User): The authenticated user object obtained from the dependency.
    - `db` (Session): The database session dependency for interacting with the database.

    **Returns:**

    A list of dictionaries, where each dictionary represents a user object.
    """
    return get_all_users(db, skip, limit)


@router.get("/users/{user_id}", tags=["Users"])
def get_user(
    user_id: int,
    user: User = Depends(get_user_disabled_current),
    db: Session = Depends(get_db),
):
    """
    Retrieves a specific user by their ID.

    **Parameters:**

    - `user_id` (int): The unique identifier of the user to retrieve.
    - `user` (User): The authenticated user object obtained from the dependency.
    - `db` (Session): The database session dependency for interacting with the database.

    **Returns:**

    A dictionary representing the requested user, or None if the user does not exist.
    """
    return get_user_id(db, user_id)


@router.post("/users/", tags=["Users"])
def create_user_service(
    request: UserSchema,
    user: User = Depends(get_user_disabled_current),
    db: Session = Depends(get_db),
):
    """
    Creates a new user in the database.

    **Parameters:**

    - `request` (UserSchema): A dictionary containing user data to be created,
      validated against the `UserSchema` model.
    - `user` (User): The authenticated user object obtained from the dependency.
    - `db` (Session): The database session dependency for interacting with the database.

    **Returns:**

    A dictionary representing the newly created user object.

    """
    return create_user(db, user=request)


@router.put("/users/{user_id}", tags=["Users"])
async def update_user_service(
    user_id: str,
    user_update: UserUpdateSchema,
    user: User = Depends(get_user_disabled_current),
    db: Session = Depends(get_db),
):
    """
    Updates a user's information in the database (using PUT method for full replacement).

    **Parameters:**

    - `user_id` (str): The unique identifier of the user to update.
    - `user_update` (UserUpdateSchema): A dictionary containing updated user data,
      validated against the `UserUpdateSchema` model.
    - `user` (User): The authenticated user object obtained from the dependency.
    - `db` (Session): The database session dependency for interacting with the database.

    **Notes:**

    - This endpoint requires a valid access token in the authorization header for authentication.
    - Users with appropriate permissions can update user information. Access control logic
      may be implemented based on your specific requirements.
    - The request body should be formatted according to the `UserUpdateSchema` definition.
    - Using PUT method replaces all user data with the provided information.
    """
    return update_user(db, user_id, user_update)


@router.patch("/users/{user_id}", tags=["Users"])
def patch_user_service(
    user_id: int,
    user_update: UserUpdateSchema,
    user: User = Depends(get_user_disabled_current),
    db: Session = Depends(get_db),
):
    """
    Updates specific fields of a user's information in the database (using PATCH method for partial updates).

    **Parameters:**

    - `user_id` (int): The unique identifier of the user to update.
    - `user_update` (UserUpdateSchema): A dictionary containing updated user data,
      validated against the `UserUpdateSchema` model. Only provided fields will be updated.
    - `user` (User): The authenticated user object obtained from the dependency.
    - `db` (Session): The database session dependency for interacting with the database.

    **Notes:**

    - This endpoint requires a valid access token in the authorization header for authentication.
    - The request body should be formatted according to the `UserUpdateSchema` definition.
      Only fields included in the request body will be updated.
    - Using PATCH method allows for partial updates of user data.
    """
    return patch_user(db, user_id, user_update)


@router.delete("/users/{user_id}", tags=["Users"])
def delete_user_service(
    user_id: int,
    user: User = Depends(get_user_disabled_current),
    db: Session = Depends(get_db),
):
    """
    Deletes a user from the database.

    **Parameters:**

    - `user_id` (int): The unique identifier of the user to delete.
    - `user` (User): The authenticated user object obtained from the dependency.
    - `db` (Session): The database session dependency for interacting with the database.

    **Returns:**

    None if the user is deleted successfully, or a dictionary with an error message
    if deletion fails.

    **Raises:**

    - Exception: If user authentication fails, the user is disabled, or user deletion fails.
    """
    return delete_user(db, user_id)
