from pydantic import BaseModel
from typing import List
import json


class PostAdditionalFields(BaseModel):
    alias: str
    value: str | int | bool | None = None


class PostCreate(BaseModel):
    categoryId: int
    title: str | None = None
    description: str
    price: int
    trade: bool | None = False
    phoneHidden: bool | None = False
    delivery: bool | None = False
    saveDeal: bool | None = False
    additionalFields: List[PostAdditionalFields] | None = []
    address: str

    @classmethod
    def __get_validators__(cls):
        yield cls.validate_to_json

    @classmethod
    def validate_to_json(cls, value):
        if isinstance(value, str):
            return cls(**json.loads(value))
        return value

    class Config:
        orm_mode = True

