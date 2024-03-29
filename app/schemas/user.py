from pydantic import BaseModel
from typing import List
from uuid import UUID
from app.schemas import post as post_schema
import datetime


class UserRole(BaseModel):
    id: int
    title: str


class UserPhoto(BaseModel):
    id: int
    url: str


class UserCreateResponse(BaseModel):
    name: str
    password: str

    class Config:
        orm_mode = True


class UserCreateRequest(BaseModel):
    name: str
    password: str

    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    name: str
    phone: str
    password: str


class UserCreateOauth(BaseModel):
    email: str | None = None
    name: str | None = None
    surname: str | None = None
    emailVerify: bool = False
    photo: str | None = None
    photoId: int | None = None
    googleId: str | None = None
    vkId: str | None = None
    appleId: str | None = None

    class Config:
        orm_mode = True


class UserOut(BaseModel):
    id: int
    uuid: UUID
    email: str | None = None
    emailVerified: bool
    phoneVerified: bool
    createdAt: datetime.datetime
    photo: UserPhoto | None = None
    role: UserRole | None = None
    phone: int | None = None
    name: str | None = None
    surname: str | None = None
    username: str | None = None
    rating: int | None = None
    googleId: str | None = None
    vkId: str | None = None
    appleId: str | None = None
    updatedAt: datetime.datetime | None = None
    lastLoginAt: datetime.datetime | None = None
    deletedAt: datetime.datetime | None = None
    emailVerifiedAt: datetime.datetime | None = None
    phoneVerifiedAt: datetime.datetime | None = None

    class Config:
        orm_mode = True


class UserPostsOut(BaseModel):
    user: UserOut
    posts: List[post_schema.PostLiteOut]

    class Config:
        orm_mode = True


class ChangeUser(BaseModel):
    email: str | None = None
    phone: int | None = None

    class Config:
        orm_mode = True
