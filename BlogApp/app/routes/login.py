from fastapi import APIRouter, Depends, HTTPException
from starlette import status
from fastapi.responses import JSONResponse
from datetime import timedelta
from sqlalchemy.orm import Session
from jwt import exceptions
from jwt.utils import get_int_from_datetime
from datetime import datetime
from typing import Any
import sys

sys.path.append("..")
from db import crud
from utils import deps, schemas, response_schemas
from auth import access_token
from conf import ProjectSettings
from utils import send_reset_password_email

router = APIRouter()


# replace response_model=Token with custom responses
@router.post("getToken",
             responses=response_schemas.get_token_response)
def authenticate_user(user: schemas.UserAuthenticate,
                      db: Session = Depends(deps.get_db)) -> JSONResponse:
    db_user = crud.get_user(db, email=user.email)
    if db_user is None:
        return JSONResponse(status_code=400,
                            content={"message": "Invalid Credentials"})
    else:
        is_password_correct = crud.check_username_password(db, user)
        if is_password_correct is False:
            return JSONResponse(status_code=400,
                                content={"message": "Invalid Credentials"})
        else:
            access_token_expires = timedelta(
                minutes=ProjectSettings.ACCESS_TOKEN_EXPIRE_MINUTES)
            token = access_token.create_access_token(
                data={"sub": user.email},
                expires_delta=access_token_expires)
            return JSONResponse(status_code=200,
                                content={"access_token": token,
                                         "token_type": "Bearer"})


@router.post("password-recovery/{email}",
             responses=response_schemas.general_responses)
def recover_password(email: str,
                     db: Session = Depends(deps.get_db)) -> JSONResponse:
    """
    Password Recovery
    """
    db_user = crud.get_user(db, email=email)

    if db_user is None:
        return JSONResponse(status_code=404, content={
            "message": "The user with this email "
                       "does not exist in the system."})

    password_reset_token = access_token.generate_password_reset_token(
        email=email)
    send_reset_password_email(email=email,
                              password_reset_token=password_reset_token)
    return JSONResponse(status_code=200,
                        content={"message": "success"})


@router.post("reset-password",
             responses=response_schemas.general_responses)
def reset_password(reset_data: schemas.UserPasswordReset,
                   db: Session = Depends(deps.get_db)) -> JSONResponse:
    """
    Reset password
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    expire_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="access expired",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = access_token.verify_password_reset_token(
            token=reset_data.token)
        token_validity = payload.get("exp")
        if get_int_from_datetime(datetime.utcnow()) >= token_validity:
            raise expire_exception
        token_email: str = payload.get("sub")
        if token_email is None:
            raise credentials_exception
    except exceptions.JWTException as e:
        print(e)
        raise credentials_exception
    db_user = crud.verify_user(db, email=token_email)
    if db_user is None:
        raise credentials_exception

    data = crud.update_user_password(db, email=token_email,
                                     password=reset_data.password)
    if data is None:
        return JSONResponse(status_code=500,
                            content={"message": "Internal Server Error"})
    return JSONResponse(status_code=200,
                        content={"message": "success"})
