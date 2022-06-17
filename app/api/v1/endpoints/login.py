from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.api.dependencies import get_db
from app.crud import user as crud_user
from app.schemas import response as response_schema
from app.utils import security


router = APIRouter(prefix="", tags=["Login"])


# @router.get("/refresh", response_model=token_schema.AccessToken, tags=[], summary="Refresh token")
# async def refresh(refresh_token_data: dict = Depends(security.decode_refresh_token)):
#     access_token = security.create_access_token(refresh_token_data)
#     return {"accessToken": access_token, "tokenType": "bearer"}


@router.post("/login", response_model=response_schema.ResponseLogin, tags=[], summary="OAuth2 Login",
             responses={400: response_schema.custom_errors("Bad Request", ["Incorrect username or password"])})
async def login(form_data: OAuth2PasswordRequestForm = Depends(),
                db: Session = Depends(get_db)):
    user = crud_user.authenticate_user(username=form_data.username, password=form_data.password, db=db)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password",
                            headers={"WWW-Authenticate": "Bearer"})
    token_data = {"sub": str(user.id)}
    access_token = security.create_access_token(data=token_data)
    refresh_token = security.create_refresh_token(data=token_data)
    return {"accessToken": access_token, "refreshToken": refresh_token}


