from fastapi import HTTPException, status, Depends
from passlib.context import CryptContext
from jose import JWTError, jwt
from google.oauth2 import id_token
from google.auth.transport import requests
import hashlib
import datetime
from app.core.config import settings
from app.api import dependencies
from app.schemas import request as request_schema


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )


def hash_password(password: str):
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def create_phone_token(data: dict, expires_delta: datetime.timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.datetime.utcnow() + expires_delta
    else:
        expire = datetime.datetime.utcnow() + datetime.timedelta(minutes=settings.PHONE_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.PHONE_TOKEN_SECRET_KEY, algorithm=settings.PHONE_TOKEN_ALGORITHM)
    return encoded_jwt


def create_access_token(data: dict, expires_delta: datetime.timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.datetime.utcnow() + expires_delta
    else:
        expire = datetime.datetime.utcnow() + datetime.timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.ACCESS_TOKEN_SECRET_KEY, algorithm=settings.ACCESS_TOKEN_ALGORITHM)
    return encoded_jwt


def create_refresh_token(data: dict, expires_delta: datetime.timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.datetime.utcnow() + expires_delta
    else:
        expire = datetime.datetime.utcnow() + datetime.timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.REFRESH_TOKEN_SECRET_KEY, algorithm=settings.REFRESH_TOKEN_ALGORITHM)
    return encoded_jwt


def decode_phone_token(access_token: str = Depends(dependencies.oauth2_scheme)):
    try:
        payload = jwt.decode(access_token, settings.PHONE_TOKEN_SECRET_KEY,
                             algorithms=[settings.PHONE_TOKEN_ALGORITHM])
        user_phone = payload.get("sub")
    except JWTError:
        raise credentials_exception
    return user_phone


def decode_refresh_token(refresh_token: str = Depends(dependencies.oauth2_scheme)):
    try:
        payload = jwt.decode(refresh_token, settings.REFRESH_TOKEN_SECRET_KEY,
                             algorithms=[settings.REFRESH_TOKEN_ALGORITHM])
    except JWTError:
        raise credentials_exception
    return payload


def decode_google_token(token: str):
    try:
        payload = id_token.verify_oauth2_token(token, requests.Request(), settings.google_Client_ID)
        token_info = request_schema.GoogleTokenData(**payload)
        return token_info
    except Exception:
        return False


def check_vk_data(vk_data: request_schema.RequestVkData):
    check_string = str(settings.vk_app_id) + str(vk_data.auth_data.uid) + str(settings.vk_Secure_Key)
    check_string_md5 = hashlib.md5(check_string.encode()).hexdigest()
    if check_string_md5 != vk_data.auth_data.hash:
        return False
    return True


def decode_apple_token(token: str):
    try:
        payload = jwt.get_unverified_claims(token)
        token_info = request_schema.AppleTokenData(**payload)
        return token_info
    except Exception as e:
        print(e)
        return False
