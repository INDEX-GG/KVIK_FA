from pydantic import BaseModel
import json
from enum import Enum
from uuid import UUID
import datetime
from typing import List


class PostCreate(BaseModel):
    categoryId: int
    title: str | None = None
    description: str
    price: int
    trade: bool | None = False
    phoneHidden: bool | None = False
    messageHidden: bool | None = False
    delivery: bool | None = False
    saveDeal: bool | None = False
    statusId: int | None = 1
    address: dict
    additionalFields: dict | None = {}

    @classmethod
    def __get_validators__(cls):
        yield cls.validate_to_json

    @classmethod
    def validate_to_json(cls, value):
        if isinstance(value, str):
            return cls(**json.loads(value))
        return value

    class Config:
        schema_extra = {
            "example": {
                "categoryId": 1,
                "description": "Post Description",
                "price": 5000,
                "address": {"key": "value"},
                "trade": False,
                "additionalFields":
                    {"alias_one": "value_one",
                     "alias_two": "alias_two"}
                }
        }
        orm_mode = True


class PostEdit(BaseModel):
    title: str | None = None
    description: str | None = None
    price: int | None = None
    trade: bool | None = None
    phoneHidden: bool | None = None
    delivery: bool | None = None
    saveDeal: bool | None = None
    statusId: None = 1
    address: dict | None = None
    additionalFields: dict | None = {}

    @classmethod
    def __get_validators__(cls):
        yield cls.validate_to_json

    @classmethod
    def validate_to_json(cls, value):
        if isinstance(value, str):
            return cls(**json.loads(value))
        return value

    class Config:
        schema_extra = {
            "example": {
                "description": "Post Description",
                "price": 5000,
                "address": {"key": "value"},
                "trade": False,
                "additionalFields":
                    {"alias_one": "value_one",
                     "alias_two": "alias_two"}
                }
        }
        orm_mode = True


class PostStatus(BaseModel):
    id: int
    title: str


class PostImage(BaseModel):
    id: int
    uuid: UUID


class PostImageResolutions(str, Enum):
    small_square = "100x100"
    medium_square = "200x200"
    large_square = "300x300"
    medium = "640x480"
    large = "1280x960"


class PostOutUser(BaseModel):
    id: int
    name: str | None
    surname: str | None


class PostCategory(BaseModel):
    id: int
    patch: str
    title: str
    transTitle: str
    postingPatch: str
    postingTitle: str
    transPostingTitle: str
    dynamicTitle: bool


class PostInDetailOut(BaseModel):
    id: int
    uuid: UUID
    # categoryId: int
    title: str
    description: str
    price: int
    trade: bool
    delivery: bool
    saveDeal: bool
    phoneHidden: bool
    messageHidden: bool
    status: PostStatus
    address: dict
    additionalFields: dict | None = {}
    createdAt: datetime.datetime
    updatedAt: datetime.datetime | None = None
    photos: List[PostImage]
    category: PostCategory
    user: PostOutUser

    class Config:
        orm_mode = True


class PostOut(BaseModel):
    id: int
    uuid: UUID
    categoryId: int
    title: str
    description: str
    price: int
    trade: bool
    delivery: bool
    saveDeal: bool
    phoneHidden: bool
    status: PostStatus
    address: dict
    additionalFields: dict | None = {}
    createdAt: datetime.datetime
    updatedAt: datetime.datetime | None = None
    photos: List[PostImage]
    user: PostOutUser

    class Config:
        orm_mode = True
