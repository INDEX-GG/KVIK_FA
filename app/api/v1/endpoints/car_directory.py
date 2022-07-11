from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api.dependencies import get_db
from app.schemas import car as car_schema
from app.schemas.response import custom_errors
from app.crud import car as car_crud


router = APIRouter(prefix="/car_directory", tags=["Car Directory"])


@router.get("", summary="Car directory",
            response_model=car_schema.Suggestion, status_code=200,
            responses={400: custom_errors("Bad Request", [{"msg": "Invalid data"}])
                       })
async def car_directory(car: car_schema.Car = Depends(),
                        db: Session = Depends(get_db)):
    suggestion = car_crud.car_suggestion(db=db, car=car)
    if not suggestion:
        raise HTTPException(status_code=400, detail={"msg": "Invalid data"})
    return suggestion
