from pydantic import BaseModel
from uuid import UUID
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


class UserBase(BaseModel):
    email: str | None = None
    phone: int | None = None
    name: str | None = None
    surname: str | None = None
    username: str | None = None
    photo: int | None = None
    rating: int | None = None
    role: int | None = None
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


class UserOut(UserBase):
    id: int
    uuid: UUID
    email: str | None = None
    emailVerified: bool
    phoneVerified: bool
    createdAt: datetime.datetime
    photo: UserPhoto | None = None
    role: UserRole

    class Config:
        orm_mode = True
