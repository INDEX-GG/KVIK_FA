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
    id: int
    patch: str
    title: str
    transTitle: str
    postingPatch: str
    postingTitle: str
    transPostingTitle: str
    dynamicTitle: bool
    additionalFields: List[CategoryAdditionalField]
