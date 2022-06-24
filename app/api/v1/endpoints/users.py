from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api.dependencies import get_db
from app.crud import user as users_crud
from app.schemas import user as user_schema, response as response_schema
from app.utils import security

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("", response_model=response_schema.ResponseSuccess, tags=[], summary="Registration user",
             description="", status_code=201,
             responses={409: response_schema.custom_errors("Conflict", ["User with this phone already exist"])})
async def registration(user_data: user_schema.UserCreateResponse,
                       user_phone: str = Depends(security.decode_phone_token),
                       db: Session = Depends(get_db)):
    user = user_schema.UserCreate(**user_data.__dict__, phone=user_phone)
    new_user = users_crud.create_user(user=user, db=db)
    if not new_user:
        raise HTTPException(status_code=409, detail="User with this phone already exist")
    return {"message": "success"}


@router.get("/me", response_model=user_schema.UserOut, tags=[], summary="Get Current User")
async def read_users_me(current_user: dict = Depends(users_crud.get_current_user)):
    return current_user
