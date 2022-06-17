from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api.dependencies import get_db
from app.crud import user as users_crud, call as call_crud
from app.schemas import user as user_schema, response as response_schema

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("", response_model=response_schema.ResponseSuccess, tags=[], summary="Registration user",
             description="", status_code=201, responses={409: response_schema.custom_errors(
                                                             "Conflict", ["User with this email already exist"]),
                                                         400: response_schema.custom_errors(
                                                             "Bad Request", ["number of attempts exceeded",
                                                                             "wrong verification code"]
                                                         )})
async def registration(user: user_schema.UserCreateCall,
                       db: Session = Depends(get_db)):
    check_unsuccessful_try = call_crud.check_count_of_unsuccessful_try_verif_code(db=db, phone=user.phone)
    if not check_unsuccessful_try:
        raise HTTPException(status_code=400, detail="number of attempts exceeded")
    check_verification_code = call_crud.check_verification_code(db=db, phone=user.phone,
                                                                verification_code=user.verification_code)
    if not check_verification_code:
        raise HTTPException(status_code=400, detail="wrong verification code")
    new_user = users_crud.create_user_phone(user=user, db=db)
    if not new_user:
        raise HTTPException(status_code=409, detail="User with this email already exist")
    return {"message": "success"}
