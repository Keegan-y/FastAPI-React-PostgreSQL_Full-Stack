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
def create_post(post: schemas.PostCreate,
                db: Session = Depends(deps.get_db),
                current_user: schemas.UserVerify = Depends(
                    deps.get_current_user)) -> JSONResponse:
    data = crud.create_post(db=db, user_id=current_user.id, post=post)
    if data is None:
        return JSONResponse(status_code=500,
                            content={"message": "Internal Server Error"})
    return JSONResponse(status_code=200,
                        content={"message": "success"})


@router.put("{post_id}", responses=response_schemas.general_responses)
def update_post(post_id: int, post: schemas.PostUpdate,
                db: Session = Depends(deps.get_db),
                current_user: schemas.UserVerify = Depends(
                    deps.get_current_user)) -> JSONResponse:
    data = crud.update_post(db, post_id=post_id, post=post)
    if data is None:
        return JSONResponse(status_code=500,
                            content={"message": "Internal Server Error"})
    return JSONResponse(status_code=200,
                        content={"message": "success"})


@router.delete("{post_id}",
               responses=response_schemas.general_responses)
def delete_post(post_id: int, db: Session = Depends(deps.get_db),
                current_user: schemas.UserVerify = Depends(
                    deps.get_current_user)) -> JSONResponse:
    data = crud.delete_post(db, post_id=post_id)
    if data is None:
        return JSONResponse(status_code=500,
                            content={"message": "Internal Server Error"})
    return JSONResponse(status_code=200,
                        content={"message": "success"})


@router.get("{post_id}",
            responses=response_schemas.single_post_responses)
def single_post(post_id: int, db: Session = Depends(deps.get_db),
                current_user: schemas.UserVerify = Depends(
                    deps.get_current_user)) -> JSONResponse:
    db_post = crud.get_post(db, post_id=post_id)
    if db_post is None:
        return JSONResponse(status_code=500,
                            content={"message": "Internal Server Error"})
    json_compatible_item_data = jsonable_encoder(db_post)
    return JSONResponse(status_code=200, content=json_compatible_item_data)


@router.get("{user_id}/all", responses=response_schemas.all_posts_responses)
def all_posts(user_id: int, page_num: int = 1,
              db: Session = Depends(deps.get_db),
              current_user: schemas.UserVerify = Depends(
                  deps.get_current_user)) -> JSONResponse:

    db_post = crud.get_all_posts(user_id, page_num, db)
    if db_post is None:
        return JSONResponse(status_code=500,
                            content={"message": "Internal Server Error"})
    json_compatible_item_data = jsonable_encoder(db_post.items)
    return JSONResponse(status_code=200,
                        content={"total_pages": db_post.pages,
                                 "total_items": db_post.total_items,
                                 "page_data": {"page_num": page_num,
                                               "items_count": db_post.page_size,
                                               "items":
                                                   json_compatible_item_data}})
