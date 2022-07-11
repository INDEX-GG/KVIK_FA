from pydantic import BaseModel


class Car(BaseModel):
    mark: str | None = None
    model: str | None = None
    generation: str | None = None
    modification: str | None = None
    year: int | None = None
    fuelType: str | None = None
    driveType: str | None = None
    transmission: str | None = None
    power: int | None = None
    engineSize: float | None = None
    bodyType: str | None = None
    doors: str | None = None
