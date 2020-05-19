from sqlalchemy.orm import Session
from sqlalchemy.orm import defer
from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError
from typing import Any
import sys

sys.path.append("..")
from db import models, pagination
from utils import passutil, schemas
from logs import fastapi_logger


# ---------------- user queries -------------------- #
def check_username_password(db: Session,
                            user: schemas.UserAuthenticate) -> Any:
    db_user_info = get_user(db,
                            email=user.email)

    return passutil.verify_password(str(user.password),
                                    str(db_user_info.password))


def create_user(db: Session, user: schemas.UserCreate) -> Any:
    try:
        hashed_password = passutil.get_password_hash(str(user.password))
        db_user = models.User(email=user.email, password=hashed_password,
                              name=user.name)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except SQLAlchemyError as e:
        fastapi_logger.exception("create_user")
        return None


def update_user(db: Session, user_id: int, user: schemas.UserUpdate) -> Any:
    try:
        db_user = db.query(models.User).filter(
            models.User.id == user_id).first()
        db_user.name = user.name
        db.commit()
        db.refresh(db_user)
        return db_user
    except SQLAlchemyError as e:
        fastapi_logger.exception("update_user")
        return None


def update_user_password(db: Session, email: str, password: str) -> Any:
    try:
        hashed_password = passutil.get_password_hash(password)
        db_user = db.query(models.User).filter(
            models.User.email == email).first()
        db_user.password = hashed_password
        db.commit()
        db.refresh(db_user)
        return db_user
    except SQLAlchemyError as e:
        fastapi_logger.exception("update_user_password")
        return None


def delete_user(db: Session, user_id: int) -> Any:
    try:
        # db_user = db.query(models.User).filter(models.User.id == user_id)
        # db.delete(db_user)
        db.query(models.User).filter(
            models.User.id == user_id).delete()
        db.commit()
        # db.refresh(db_user)
        return True
    except SQLAlchemyError as e:
        fastapi_logger.exception("delete_user")
        return None


def verify_user(db: Session, email: str) -> Any:
    try:
        data = db.query(models.User.id, models.User.email).filter(
            models.User.email == email).first()
        return data
    except SQLAlchemyError as e:
        fastapi_logger.exception("verify_user")
        return None


def get_user(db: Session, email: str) -> Any:
    try:
        data = db.query(models.User).filter(
            models.User.email == email).options(defer('password')).first()
        return data
    except SQLAlchemyError as e:
        fastapi_logger.exception("get_user")
        return None


def get_user_id(db: Session, id: int) -> Any:
    try:
        data = db.query(models.User).filter(
            models.User.id == id).options(defer('password')).first()
        return data
    except SQLAlchemyError as e:
        fastapi_logger.exception("get_user_id")
        return None


# https://docs.sqlalchemy.org/en/13/orm/loading_columns.html#deferred
def get_all_user(db: Session) -> Any:
    try:
        data = db.query(models.User).options(defer('password')).all()
        return data
    except SQLAlchemyError as e:
        fastapi_logger.exception("get_all_user")
        return None


# ---------------- post queries -------------------- #

def create_post(db: Session, user_id: int, post: schemas.PostCreate) -> Any:
    try:
        db_post = models.Post(title=post.title, post=post.post,
                              post_date=datetime.utcnow(),
                              user_id=user_id)
        db.add(db_post)
        db.commit()
        db.refresh(db_post)
        return db_post
    except SQLAlchemyError as e:
        fastapi_logger.exception("create_post")
        return None


def update_post(db: Session, post_id: int, post: schemas.PostUpdate) -> Any:
    try:
        db_post = db.query(models.Post).filter(
            models.Post.id == post_id).first()
        db_post.title = post.title
        db_post.post = post.post
        db_post.post_date = datetime.utcnow()
        db.commit()
        db.refresh(db_post)
        return db_post
    except SQLAlchemyError as e:
        fastapi_logger.exception("update_post")
        return None


# def get_all_posts(user_id: int, page_num: int, db: Session):
#     try:
#         # data = db.query(models.Post).paginate(page=page_num, per_page=20)
#         data = db.query(models.Post).filter_by(user_id=user_id).order_by(
#             models.Post.post_date.desc()).paginate(page=page_num, per_page=20)
#         return data
#     except SQLAlchemyError as e:
#         print(e.args)
#         return None

def get_all_posts(user_id: int, page_num: int, db: Session) -> Any:
    try:
        # data = db.query(models.Post).paginate(page=page_num, per_page=20)
        query = db.query(models.Post).filter_by(user_id=user_id).order_by(
            models.Post.post_date.desc())
        data = pagination.paginate(query=query, page=page_num, page_size=20)
        return data
    except SQLAlchemyError as e:
        fastapi_logger.exception("get_all_posts")
        return None


def get_post(db: Session, post_id: int) -> Any:
    try:
        data = db.query(models.Post).filter(models.Post.id == post_id).first()
        return data
    except SQLAlchemyError as e:
        fastapi_logger.exception("get_post")
        return None


def delete_post(db: Session, post_id: int) -> Any:
    try:
        # db_post = db.query(models.Post).delete(models.Post.id == post.id)
        # db.delete(db_post)
        db.query(models.Post).filter(
            models.Post.id == post_id).delete()
        db.commit()
        return True
    except SQLAlchemyError as e:
        fastapi_logger.exception("delete_post")
        return None
