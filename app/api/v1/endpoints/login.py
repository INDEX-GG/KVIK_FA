from fastapi import APIRouter, Depends, HTTPException, Body
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.api.dependencies import get_db
from app.crud import user as crud_user
from app.schemas import response as response_schema, request as request_schema, user as user_schema
from app.utils import security


router = APIRouter(prefix="", tags=["Login"])


@router.get("/refresh", response_model=response_schema.AccessToken, tags=[], summary="Refresh token")
async def refresh(refresh_token_data: dict = Depends(security.decode_refresh_token)):
    token_data = {"sub": refresh_token_data.get("sub")}
    access_token = security.create_access_token(token_data)
    return {"accessToken": access_token}


@router.post("/reset-password", response_model=response_schema.ResponseSuccess, tags=[],
             summary="Recovery password by phone", description="",
             responses={400: response_schema.custom_errors("Conflict", ["user with this phone does not exist"])})
async def reset_password(user_phone: str = Depends(security.decode_phone_token),
                         new_password: str = Body(embed=True),
                         db: Session = Depends(get_db)):
    user = crud_user.get_user_by_phone(db, phone=user_phone)
    if not user:
        raise HTTPException(status_code=400, detail="user with this phone does not exist")
    crud_user.change_user_password(db=db, user=user, new_password=security.hash_password(new_password))
    return {"message": "success"}


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


@router.post("/login_google", response_model=response_schema.ResponseLogin, tags=[], summary="Sign in with Google",
             responses={400: response_schema.custom_errors("Bad Request", ["Invalid token"])})
async def login_google(google_data: request_schema.RequestGoogleData,
                       db: Session = Depends(get_db)):
    token_data = security.decode_google_token(str(google_data.token))
    if not token_data:
        raise HTTPException(status_code=400, detail="Invalid token")
    google_id = token_data.sub
    user_data = user_schema.UserCreateOauth(googleId=google_id, email=token_data.email, name=token_data.given_name,
                                            surname=token_data.family_name, photo=token_data.picture)
    user = crud_user.get_user_by_google_id(db, google_id=google_id)
    if not user:
        user = crud_user.create_user_oauth(user=user_data, db=db)
    token_data = {"sub": str(user.id)}
    access_token = security.create_access_token(data=token_data)
    refresh_token = security.create_refresh_token(data=token_data)
    return {"accessToken": access_token, "refreshToken": refresh_token}


@router.post("/login_vk", response_model=response_schema.ResponseLogin, tags=[], summary="Sign in with VK",
             responses={400: response_schema.custom_errors("Bad Request", ["Invalid data"])})
async def login_google(vk_data: request_schema.RequestVkData,
                       db: Session = Depends(get_db)):
    if not security.check_vk_data(vk_data):
        raise HTTPException(status_code=400, detail="Invalid data")
    vk_id = str(vk_data.auth_data.uid)
    user_data = user_schema.UserCreateOauth(vkId=vk_id, name=vk_data.auth_data.first_name,
                                            surname=vk_data.auth_data.last_name, photo=vk_data.auth_data.photo)
    user = crud_user.get_user_by_vk_id(db, vk_id=vk_id)
    if not user:
        user = crud_user.create_user_oauth(user=user_data, db=db)
    token_data = {"sub": str(user.id)}
    access_token = security.create_access_token(data=token_data)
    refresh_token = security.create_refresh_token(data=token_data)
    return {"accessToken": access_token, "refreshToken": refresh_token, "tokenType": "bearer"}


@router.post("/login_apple", response_model=response_schema.ResponseLogin, tags=[], summary="Sign in with Apple",
             responses={400: response_schema.custom_errors("Bad Request", ["Invalid data"])})
async def login_google(apple_data: request_schema.RequestAppleData,
                       db: Session = Depends(get_db)):
    token_data = security.decode_apple_token(apple_data.id_token)
    if not token_data:
        raise HTTPException(status_code=400, detail="Invalid data")
    apple_id = token_data.sub
    user_data = user_schema.UserCreateOauth(appleId=apple_id, email=apple_data.email, name=apple_data.firstName,
                                            surname=apple_data.lastName)
    user = crud_user.get_user_by_apple_id(db, apple_id=apple_id)
    if not user:
        user = crud_user.create_user_oauth(user=user_data, db=db)
    token_data = {"sub": str(user.id)}
    access_token = security.create_access_token(data=token_data)
    refresh_token = security.create_refresh_token(data=token_data)
    return {"accessToken": access_token, "refreshToken": refresh_token, "tokenType": "bearer"}