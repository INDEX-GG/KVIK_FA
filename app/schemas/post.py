from pydantic import BaseModel
from typing import List
import json


class PostAdditionalFields(BaseModel):
    alias: str
    value: str | int | float | bool | list | None = None


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
