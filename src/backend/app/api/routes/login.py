from datetime import timedelta, datetime, timezone
from typing import Annotated, Any

from fastapi import APIRouter, Depends, HTTPException, Response, Cookie
from fastapi.security import OAuth2PasswordRequestForm
from starlette.responses import JSONResponse

from app.core.crud import user as crud

from app.api.deps import CurrentUser, SessionDep, get_current_active_superuser
from app.core import security
from app.core.config import settings
from app.core.models.refresh_token import RefreshToken
from app.core.security import get_password_hash
from app.core.models.user import Message, NewPassword, Token, UserPublic
from app.core.utils import (
    generate_password_reset_token,
    generate_reset_password_email,
    send_email,
    verify_password_reset_token,
)

router = APIRouter()

@router.post("/login/access-token")
def login_access_token_web(
    session: SessionDep, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
) -> JSONResponse:
    """
    OAuth2 compatible token login, get an access token for future requests using header Authorization
    """
    user = crud.authenticate(
        session=session, email=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    elif not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    refresh_token_expires = timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)

    access_token = security.create_access_token(user.id, expires_delta=access_token_expires)
    refresh_token = security.create_access_token(user.id, expires_delta=refresh_token_expires)  # Using the same function

    # Store refresh token in the database
    new_refresh_token = RefreshToken(
        user_id=user.id,
        refresh_token=refresh_token,
        expires_at=datetime.now(timezone.utc) + refresh_token_expires
    )
    session.add(new_refresh_token)
    session.commit()

    response = JSONResponse(content={"message": "Login successful"})
    response.set_cookie("access_token", access_token, httponly=True, secure=True, samesite="strict")
    response.set_cookie("refresh_token", refresh_token, httponly=True, secure=True, samesite="strict")
    return response

#
# @router.post("/login/access-token-web")
# def login_access_token_api(
#     session: SessionDep, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
# ) -> JSONResponse:
#     """
#     OAuth2 compatible token login, get an access token for future requests using HTTP only cookies
#     """
#     user = crud.authenticate(
#         session=session, email=form_data.username, password=form_data.password
#     )
#     if not user:
#         raise HTTPException(status_code=400, detail="Incorrect email or password")
#     elif not user.is_active:
#         raise HTTPException(status_code=400, detail="Inactive user")
#
#     access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
#     access_token = security.create_access_token(
#         user.id, expires_delta=access_token_expires
#     )
#     response = JSONResponse(content={"message": "Login successful"})
#     response.set_cookie(
#         key="access_token",
#         value=access_token,
#         httponly=True,
#         secure=True,
#         samesite="strict"
#     )
#     return response


@router.post("/refresh-token")
def refresh_access_token(
    session: SessionDep, refresh_token: str = Cookie(None)
):
    """
    Issues a new access token using a valid, non-revoked refresh token.
    """
    if not refresh_token:
        raise HTTPException(status_code=403, detail="No refresh token provided")

    # Retrieve token and check if it’s revoked or expired
    token_entry = session.query(RefreshToken).filter(RefreshToken.refresh_token == refresh_token).first()
    if not token_entry:
        raise HTTPException(status_code=403, detail="Invalid refresh token")

    if token_entry.revoked:
        raise HTTPException(status_code=403, detail="Refresh token has been revoked")

    if token_entry.expires_at < datetime.utcnow():
        raise HTTPException(status_code=403, detail="Refresh token has expired")

    # Generate new access token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(token_entry.user_id, expires_delta=access_token_expires)

    response = JSONResponse(content={"access_token": access_token})
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=True,
        samesite="strict"
    )
    return response


@router.post("/login/test-token", response_model=UserPublic)
def test_token(current_user: CurrentUser) -> Any:
    """
    Test access token
    """
    return current_user


@router.post("/logout")
async def logout(response: Response,
                session: SessionDep,
                 refresh_token: str = Cookie(None),
                 ):
    """
    Logs out the user by marking the refresh token as revoked.
    """
    if not refresh_token:
        raise HTTPException(status_code=400, detail="No refresh token provided")

    # Find the refresh token and mark it as revoked
    token_entry = session.query(RefreshToken).filter(RefreshToken.refresh_token == refresh_token).first()
    if token_entry:
        token_entry.revoked = True  # Blacklist the token
        session.commit()

    # Clear cookies
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")

    return JSONResponse(content={"message": "Logout successful"})
