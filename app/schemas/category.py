from pydantic import BaseModel
from typing import List, Dict


class CategoryAdditionalFieldType(BaseModel):
    name: str
    ability_to_edit: bool
    rendering_type: int
    properties: Dict


class CategoryAdditionalField(BaseModel):
    title: str
    alias: str
    requiring: bool
    dependencies: dict
    type: CategoryAdditionalFieldType


CategoryAdditionalFields = List[CategoryAdditionalField]


class Category(BaseModel):
    patch: str
    title: int
    trans_title: str
    dynamicTitle: bool
    postingTitle: str
    trans_posting_title: str

    additionalFields: CategoryAdditionalFields
