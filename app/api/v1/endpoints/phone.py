from sqlalchemy.orm import Session
from pydantic import constr
from fastapi import APIRouter, Depends, Path, HTTPException
from app.api.dependencies import get_db
from app.schemas import response as response_schema
from app.crud import call as call_crud, user as user_crud
from app.utils import phone_call


router = APIRouter(prefix="/phone", tags=["Phone"])


@router.get("/call/registration/{phone}", response_model=response_schema.ResponseSuccess,
            tags=[], summary="Call to phone",
            responses={409: response_schema.custom_errors(
                "Conflict", ["User with this email already exist"]),
                400: response_schema.custom_errors(
                    "Bad Request", ["usage limit exceeded",
                                    "hardware or services problems"]
                )})
async def registration_call(phone: constr(regex=r"^(\+)[7][0-9]{10}$") = Path(),
                            db: Session = Depends(get_db)):
    check_exist_user_with_phone = user_crud.check_user_with_phone(phone=phone, db=db)
    if not check_exist_user_with_phone:
        raise HTTPException(status_code=409, detail="user with this phone already exist")
    check_count_of_calls = call_crud.check_count_of_calls(phone=phone, max_count_of_calls_in_period=3,
                                                          time_period_in_minutes=30, db=db)
    if not check_count_of_calls:
        raise HTTPException(status_code=400, detail="usage limit exceeded")
    code = phone_call.call_to_phone(phone)
    if not code:
        raise HTTPException(status_code=400, detail="hardware or services problems")
    call_crud.create_call(phone=phone, verification_code=code, db=db)
    return {"message": "success"}
