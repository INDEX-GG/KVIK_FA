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
    type: CategoryAdditionalFieldType


CategoryAdditionalFields = List[CategoryAdditionalField]


class Category(BaseModel):
    patch: str
    title: int
    dynamicTitle: bool
    postingTitle: str
    transTitle: str
    additionalFields: CategoryAdditionalFields
