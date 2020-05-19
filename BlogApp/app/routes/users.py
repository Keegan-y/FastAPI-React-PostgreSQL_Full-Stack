from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
import sys

sys.path.append("..")
from utils import deps, schemas
from db import crud
from utils import response_schemas

router = APIRouter()


@router.post("", responses=response_schemas.general_responses)
def register_user(user: schemas.UserCreate,
                  db: Session = Depends(deps.get_db)) -> JSONResponse:
    data = crud.get_user(db, email=user.email)
    if data is not None and not data:
        return JSONResponse(status_code=400,
                            content={"message": "email already registered"})
        # raise HTTPException(status_code=400,
        #                     detail="email already registered")
    data = crud.create_user(db=db, user=user)
    if data is None:
        return JSONResponse(status_code=500,
                            content={"message": "Internal Server Error"})
    return JSONResponse(status_code=200,
                        content={"message": "success"})


@router.put("{user_id}", responses=response_schemas.general_responses)
def update_user(user_id: int, user: schemas.UserUpdate,
                db: Session = Depends(deps.get_db),
                current_user: schemas.UserVerify = Depends(
                    deps.get_current_user)) -> JSONResponse:
    data = crud.update_user(db, user_id=user_id, user=user)
    if data is None:
        return JSONResponse(status_code=500,
                            content={"message": "Internal Server Error"})
    return JSONResponse(status_code=200,
                        content={"message": "success"})


@router.delete("{user_id}",
               responses=response_schemas.general_responses)
def delete_user(user_id: int, db: Session = Depends(deps.get_db),
                current_user: schemas.UserVerify = Depends(
                    deps.get_current_user)) -> JSONResponse:
    data = crud.delete_user(db, user_id=user_id)
    if data is None:
        return JSONResponse(status_code=500,
                            content={"message": "Internal Server Error"})
    return JSONResponse(status_code=200,
                        content={"message": "success"})


@router.get("{user_id}",
            responses=response_schemas.single_users_responses)
def single_user(user_id: int, db: Session = Depends(deps.get_db),
                current_user: schemas.UserVerify = Depends(
                    deps.get_current_user)) -> JSONResponse:
    db_user = crud.get_user_id(db, id=user_id)
    if db_user is None:
        return JSONResponse(status_code=500,
                            content={"message": "Internal Server Error"})
    json_compatible_item_data = jsonable_encoder(db_user)
    return JSONResponse(status_code=200, content=json_compatible_item_data)


@router.get("", responses=response_schemas.all_users_responses)
def all_user(db: Session = Depends(deps.get_db),
             current_user: schemas.UserVerify = Depends(
                 deps.get_current_user)) -> JSONResponse:
    db_user = crud.get_all_user(db)
    if db_user is None:
        return JSONResponse(status_code=500,
                            content={"message": "Internal Server Error"})
    json_compatible_item_data = jsonable_encoder(db_user)
    return JSONResponse(status_code=200, content=json_compatible_item_data)
