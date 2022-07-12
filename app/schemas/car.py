from pydantic import BaseModel
from typing import List


class Car(BaseModel):
    brand: str | None = None
    model: str | None = None
    year_of_issue: int | None = None
    bodytype: str | None = None
    doors: int | None = None
    generation: str | None = None
    fueltype: str | None = None
    drivetype: str | None = None
    transmission: str | None = None
    modification: str | None = None


class Suggestion(BaseModel):
    name: str
    values: List[int] | List[str]
    completedFields: list[dict] | None = None
