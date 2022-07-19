from pydantic import BaseModel
import json
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
    delivery: bool | None = False
    saveDeal: bool | None = False
    StatusId: int | None = 1
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
                "address": "redact letter",
                "trade": False,
                "additionalFields":
                    [
                        {"alias": "alias_one", "value": "value_one"},
                        {"alias": "alias_two", "value": "value_two"}
                    ]
                }
        }
        orm_mode = True


class PostStatus(BaseModel):
    id: int
    title: str


class PostImage(BaseModel):
    id: int
    url: str


class PostOutUser(BaseModel):
    id: int
    name: str | None
    surname: str | None


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
