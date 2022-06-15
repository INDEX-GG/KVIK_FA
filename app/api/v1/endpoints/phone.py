from sqlalchemy.orm import Session
from pydantic import constr
from fastapi import APIRouter, Depends, Path
from app.api.dependencies import get_db
from app.schemas import response as response_schema
from app.crud import calls as calls_crud
from app.utils import phone_call


router = APIRouter(prefix="/phone", tags=["Users"])


@router.get("/call/{phone}", response_model=response_schema.ResponseSuccess, tags=[], summary="Call to phone",
            responses={400: {"model": response_schema.ResponseCustomError}})
async def read_users_me(phone: constr(regex=r"^(\+)[7][0-9]{10}$") = Path(),
                        db: Session = Depends(get_db)):

    # code = phone_call.call_to_phone(phone)
    code = 1234
    calls_crud.create_call(phone=phone, validate_code=code, db=db)

    print(phone)

    return {"message": "success"}
