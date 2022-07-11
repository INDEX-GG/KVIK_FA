from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api.dependencies import get_db
from app.schemas import response as response_schema, car as car_schema
from app.schemas.response import custom_errors
from app.crud import car as car_crud


router = APIRouter(prefix="/car_directory", tags=["Car Directory"])


@router.get("", summary="Car directory",
            # response_model=response_schema.ResponseSuccess, status_code=200,
            responses={409: custom_errors("Conflict", [{"msg": "User with this phone already exist"}])
                       })
async def car_directory(car: car_schema.Car = Depends(),
                        db: Session = Depends(get_db)):

    answer = car_crud.car_suggestion(db=db, car=car)

    return answer
