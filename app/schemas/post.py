from pydantic import BaseModel
from typing import List


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

    class Config:
        orm_mode = True
