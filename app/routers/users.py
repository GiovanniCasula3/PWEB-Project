

from fastapi import APIRouter, Request, HTTPException, Path, Form #HTTPException serve per gestire le eccezioni
from app.models.user import UserCreate, User, UserPublic
from typing import Annotated # Annotated serve per annotare i parametri, definire il tipo di dato e
from pydantic import ValidationError
from fastapi.responses import RedirectResponse
from data.db import SessionDep
from sqlmodel import select, delete

router = APIRouter(prefix="/users")

@router.get("/")
def get_all_users(
    session: SessionDep,
    request: Request,
    sort: bool = False
) -> list[UserPublic]:
    """ Get all users. """
    statement = select(User)
    users = session.exec(statement).all()
    if sort:
        return sorted(users, key=lambda user: user.id)
    return list(users)

@router.post("/")
def add_user(
    request: Request,
    user: UserCreate,
    session: SessionDep
):
    """ Add a new user. """
    validated_user = User.model_validate(user)
    session.add(validated_user)
    session.commit()
    return "User successfully added."

@router.get("/{username}")
def get_user_by_username(
    username: Annotated[str, Path(description="The username of the user to retrieve")],
    session: SessionDep
) -> UserPublic:
    """ Get a user by username. """
    statement = select(User).where(User.username == username)
    user = session.exec(statement).one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return UserPublic.model_validate(user)