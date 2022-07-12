from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.db.db_models import Car, CarMark
from app.schemas import car as car_schema


def car_suggestion(db: Session, car: car_schema.Car):
    if not car.mark and not car.model and not car.year and not car.bodyType \
            and not car.doors and not car.generation and not car.fuelType and not car.driveType \
            and not car.transmission and not car.modification:
        return get_marks(db=db)

    if car.mark and not car.model and not car.year and not car.bodyType \
            and not car.doors and not car.generation and not car.fuelType and not car.driveType \
            and not car.transmission and not car.modification:
        return get_models(db=db, mark=car.mark)

    if car.mark and car.model and not car.year and not car.bodyType \
            and not car.doors and not car.generation and not car.fuelType and not car.driveType \
            and not car.transmission and not car.modification:
        return get_years(db=db, mark=car.mark, model=car.model)

    if car.mark and car.model and car.year and not car.bodyType \
            and not car.doors and not car.generation and not car.fuelType and not car.driveType \
            and not car.transmission and not car.modification:
        return get_body_types(db=db, mark=car.mark, model=car.model, year=car.year)

    if car.mark and car.model and car.year and car.bodyType \
            and not car.doors and not car.generation and not car.fuelType and not car.driveType \
            and not car.transmission and not car.modification:
        return get_doors(db=db, mark=car.mark, model=car.model, year=car.year, body_type=car.bodyType)

    if car.mark and car.model and car.year and car.bodyType \
            and car.doors and not car.generation and not car.fuelType and not car.driveType \
            and not car.transmission and not car.modification:
        return get_generations(db=db, mark=car.mark, model=car.model, year=car.year, body_type=car.bodyType,
                               door=car.doors)

    if car.mark and car.model and car.year and car.bodyType \
            and car.doors and car.generation and not car.fuelType and not car.driveType \
            and not car.transmission and not car.modification:
        return get_fuel_types(db=db, mark=car.mark, model=car.model, year=car.year, body_type=car.bodyType,
                              door=car.doors, generation=car.generation)

    if car.mark and car.model and car.year and car.bodyType \
            and car.doors and car.generation and car.fuelType and not car.driveType \
            and not car.transmission and not car.modification:
        return get_drive_types(db=db, mark=car.mark, model=car.model, year=car.year, body_type=car.bodyType,
                               door=car.doors, generation=car.generation, fuel_type=car.fuelType)

    if car.mark and car.model and car.year and car.bodyType \
            and car.doors and car.generation and car.fuelType and car.driveType \
            and not car.transmission and not car.modification:
        return get_transmissions(db=db, mark=car.mark, model=car.model, year=car.year, body_type=car.bodyType,
                                 door=car.doors, generation=car.generation, fuel_type=car.fuelType,
                                 drive_type=car.driveType)

    if car.mark and car.model and car.year and car.bodyType \
            and car.doors and car.generation and car.fuelType and car.driveType \
            and car.transmission and not car.modification:
        return get_modifications(db=db, mark=car.mark, model=car.model, year=car.year, body_type=car.bodyType,
                                 door=car.doors, generation=car.generation, fuel_type=car.fuelType,
                                 drive_type=car.driveType, transmission=car.transmission)

    if car.mark and car.model and car.year and car.bodyType \
            and car.doors and car.generation and car.fuelType and car.driveType \
            and car.transmission and car.modification:
        return get_complectations(db=db, mark=car.mark, model=car.model, year=car.year, body_type=car.bodyType,
                                  door=car.doors, generation=car.generation, fuel_type=car.fuelType,
                                  drive_type=car.driveType, transmission=car.transmission,
                                  modification=car.modification)

    return False


def get_marks(db: Session):
    query = db.query(CarMark.title).order_by(CarMark.title.asc()).all()
    marks = [x.title for x in query]
    return {"name": "brand", "values": marks}


def get_models(db: Session, mark):
    query = db.query(Car.model).filter(Car.mark == mark).order_by(Car.model.asc()).distinct().all()
    if len(query) == 0:
        raise HTTPException(404)
    models = [x.model for x in query]
    return {"name": "model", "values": models}


def get_years(db: Session, mark, model):
    query = db.query(Car.yearFrom, Car.yearTo).filter(Car.mark == mark, Car.model == model).distinct().all()
    if len(query) == 0:
        raise HTTPException(404)
    years = set()
    for i in query:
        years.update(list(range(i.yearFrom, i.yearTo + 1)))
    return {"name": "year_of_issue", "values": years}


def get_body_types(db: Session, mark, model, year):
    query = db.query(Car.bodyType).filter(Car.mark == mark, Car.model == model,
                                          Car.yearFrom <= year, Car.yearTo >= year)\
        .order_by(Car.bodyType.asc()).distinct().all()
    if len(query) == 0:
        raise HTTPException(404)
    body_types = [x.bodyType for x in query]
    return {"name": "bodytype", "values": body_types}


def get_doors(db: Session, mark, model, year, body_type):
    query = db.query(Car.doors).filter(Car.mark == mark, Car.model == model,
                                       Car.yearFrom <= year, Car.yearTo >= year, Car.bodyType == body_type)\
        .order_by(Car.doors.asc()).distinct().all()
    if len(query) == 0:
        raise HTTPException(404)
    doors = [x.doors for x in query]
    return {"name": "doors", "values": doors}


def get_generations(db: Session, mark, model, year, body_type, door):
    query = db.query(Car.generation).filter(Car.mark == mark, Car.model == model,
                                            Car.yearFrom <= year, Car.yearTo >= year, Car.bodyType == body_type,
                                            Car.doors == door)\
        .order_by(Car.generation.asc()).distinct().all()
    if len(query) == 0:
        raise HTTPException(404)
    generations = [x.generation for x in query]
    return {"name": "generation", "values": generations}


def get_fuel_types(db: Session, mark, model, year, body_type, door, generation):
    query = db.query(Car.fuelType).filter(Car.mark == mark, Car.model == model,
                                          Car.yearFrom <= year, Car.yearTo >= year, Car.bodyType == body_type,
                                          Car.doors == door, Car.generation == generation)\
        .order_by(Car.fuelType.asc()).distinct().all()
    if len(query) == 0:
        raise HTTPException(404)
    fuel_types = [x.fuelType for x in query]
    return {"name": "fueltype", "values": fuel_types}


def get_drive_types(db: Session, mark, model, year, body_type, door, generation, fuel_type):
    query = db.query(Car.driveType).filter(Car.mark == mark, Car.model == model,
                                           Car.yearFrom <= year, Car.yearTo >= year, Car.bodyType == body_type,
                                           Car.doors == door, Car.generation == generation,
                                           Car.fuelType == fuel_type)\
        .order_by(Car.driveType.asc()).distinct().all()
    if len(query) == 0:
        raise HTTPException(404)
    drive_types = [x.driveType for x in query]
    return {"name": "drivetype", "values": drive_types}


def get_transmissions(db: Session, mark, model, year, body_type, door, generation, fuel_type, drive_type):
    query = db.query(Car.transmission).filter(Car.mark == mark, Car.model == model,
                                              Car.yearFrom <= year, Car.yearTo >= year, Car.bodyType == body_type,
                                              Car.doors == door, Car.generation == generation,
                                              Car.fuelType == fuel_type, Car.driveType == drive_type)\
        .order_by(Car.transmission.asc()).distinct().all()
    if len(query) == 0:
        raise HTTPException(404)
    transmissions = [x.transmission for x in query]
    return {"name": "transmission", "values": transmissions}


def get_modifications(db: Session, mark, model, year, body_type, door, generation, fuel_type, drive_type, transmission):
    query = db.query(Car.modification).filter(Car.mark == mark, Car.model == model,
                                              Car.yearFrom <= year, Car.yearTo >= year, Car.bodyType == body_type,
                                              Car.doors == door, Car.generation == generation,
                                              Car.fuelType == fuel_type, Car.driveType == drive_type,
                                              Car.transmission == transmission)\
        .order_by(Car.modification.asc()).distinct().all()
    if len(query) == 0:
        raise HTTPException(404)
    modifications = [x.modification for x in query]
    return {"name": "modification", "values": modifications}


def get_complectations(db: Session, mark, model, year, body_type, door, generation,
                       fuel_type, drive_type, transmission, modification):
    query = db.query(Car.complectation, Car.power, Car.engineSize)\
        .filter(Car.mark == mark, Car.model == model, Car.yearFrom <= year, Car.yearTo >= year,
                Car.bodyType == body_type, Car.doors == door, Car.generation == generation, Car.fuelType == fuel_type,
                Car.driveType == drive_type, Car.transmission == transmission, Car.modification == modification)\
        .order_by(Car.complectation.asc()).distinct().all()
    if len(query) == 0:
        raise HTTPException(404)
    complectations = [x.complectation for x in query]
    return {"name": "complectation", "values": complectations,
            "completedFields": [{"name": "power", "value": query[0].power},
                                {"name": "enginesize", "value": query[0].engineSize}]}
