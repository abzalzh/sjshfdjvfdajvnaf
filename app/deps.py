from typing import Annotated

import jwt
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.errors import InvalidToken
from app.models import User
from app.security import read_access_token


def get_db():
    with SessionLocal() as session:
        yield session              # the route runs here; then the session is closed


SessionDep = Annotated[Session, Depends(get_db)]

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")    # gives /docs its Authorize button


def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    session: SessionDep,
) -> User:
    # No Authorization header: oauth2_scheme has already answered 401 "Not authenticated".
    try:
        payload = read_access_token(token)
    except jwt.InvalidTokenError:          # changed signature, or exp has passed
        raise InvalidToken()
    user = session.scalar(select(User).where(User.name == payload["sub"]))
    if user is None:                       # a valid token of a user who is not in this database
        raise InvalidToken()
    return user


CurrentUser = Annotated[User, Depends(get_current_user)]
