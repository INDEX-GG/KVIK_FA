from sqlalchemy.orm import Session
from app.db.db_models import Car
from app.schemas import car as car_schema


def get_cars(db: Session, car: car_schema.Car):
    query = db.query(Car).limit(10)

    cars = query.all()
    print(cars)
    pass


def car_suggestion(db: Session, car: car_schema.Car):
    # get_cars(db=db, car=car)
    if not car.mark and not car.model and not car.year and not car.bodyType \
            and not car.generation and not car.fuelType and not car.driveType \
            and not car.transmission and not car.modification:
        print("CASE1")

    if car.model and car.engineSize:
        print("CASE123123")





    return True
