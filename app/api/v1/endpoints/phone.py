from sqlalchemy.orm import Session
from pydantic import constr
from fastapi import APIRouter, Depends, Path, HTTPException
from app.api.dependencies import get_db
from app.schemas import response as response_schema
from app.schemas.response import custom_errors
from app.crud import call as call_crud, user as user_crud
from app.utils import phone_call, security


router = APIRouter(prefix="/phone", tags=["Phone"])


@router.get("/check_registration/{phone}", summary="Check Phone Registration",
            response_model=response_schema.ResponseCheckPhoneRegistration)
async def check_registration(phone: constr(regex=r"^(\+)[7][0-9]{10}$") = Path(),
                             db: Session = Depends(get_db)):
    check_phone_exist = user_crud.get_user_by_phone(db=db, phone=phone)
    if check_phone_exist:
        return {"phoneRegistration": True}
    return {"phoneRegistration": False}


@router.get("/call/{phone}", summary="Call to phone",
            response_model=response_schema.ResponseSuccess,
            responses={409: custom_errors("Conflict", [{"msg": "User with this phone already exist"}]),
                       400: custom_errors("Bad Request", [{"msg": "usage limit exceeded"},
                                                                          {"msg": "hardware or services problems"}])
                       })
async def call_phone(phone: constr(regex=r"^(\+)[7][0-9]{10}$") = Path(),
                     db: Session = Depends(get_db)):
    check_count_of_calls = call_crud.check_count_of_calls(phone=phone, max_count_of_calls_in_period=3,
                                                          time_period_in_minutes=30, db=db)
    if not check_count_of_calls:
        raise HTTPException(status_code=400, detail={"msg": "usage limit exceeded"})
    code = phone_call.call_to_phone(phone)
    if not code:
        raise HTTPException(status_code=400, detail={"msg": "hardware or services problems"})
    call_crud.create_call(phone=phone, verification_code=code, db=db)
    return {"msg": "success"}


@router.get("/check_verification_code/{phone}/{code}", summary="Check Verification Code",
            response_model=response_schema.ResponseCheckVerifCode,
            responses={400: custom_errors("Bad Request", [{"msg": "number of attempts exceeded"},
                                                                          {"msg": "wrong verification code"}])
                       })
async def check_verification_code(phone: constr(regex=r"^(\+)[7][0-9]{10}$") = Path(),
                                  code: str = Path(),
                                  db: Session = Depends(get_db)):
    check_unsuccessful_try = call_crud.check_count_of_unsuccessful_try_verif_code(db=db, phone=phone)
    if not check_unsuccessful_try:
        raise HTTPException(status_code=400, detail={"msg": "number of attempts exceeded"})
    check_verif_code = call_crud.check_verification_code(db=db, phone=phone, verification_code=code)
    if not check_verif_code:
        raise HTTPException(status_code=400, detail={"msg": "wrong verification code"})
    phone_token = security.create_phone_token(data={"sub": phone})
    return {"phone_token": phone_token}
