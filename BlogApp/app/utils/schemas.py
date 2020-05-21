from pydantic import BaseModel
from datetime import datetime
from typing import Dict


class Message(BaseModel):
    message: str


class UserBase(BaseModel):
    email: str


class UserVerify(UserBase):
    id: int


class UserCreate(UserBase):
    password: str
    name: str


class UserUpdate(UserBase):
    name: str


class UserAuthenticate(UserBase):
    password: str


class UserPasswordReset(BaseModel):
    token: str
    password: str


# return in response
class User(UserBase):
    id: int

    class Config:
        orm_mode = True


class PostBase(BaseModel):
    pass


class PostCreate(PostBase):
    title: str
    post: str


class PostUpdate(PostBase):
    title: str
    post: str


# return in response
class Post(PostBase):
    id: int

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: str = None
    expire: str = None
    issue_time: str = None
