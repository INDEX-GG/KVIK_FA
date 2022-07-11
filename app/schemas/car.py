from pydantic import BaseModel
from typing import List


class Car(BaseModel):
    mark: str | None = None
    model: str | None = None
    year: int | None = None
    bodyType: str | None = None
    doors: int | None = None
    generation: str | None = None
    fuelType: str | None = None
    driveType: str | None = None
    transmission: str | None = None
    modification: str | None = None


class Suggestion(BaseModel):
    name: str
    values: List[int] | List[str]
