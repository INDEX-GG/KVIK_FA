from sqlalchemy.orm import Session
from fastapi import Depends
import uuid
import datetime
from app.api.dependencies import get_db
from app.db.db_models import User, UserPhoto
from app.schemas import user as user_schema
from app.utils import security
from app.api import dependencies


def get_user_by_id(db: Session, user_id: int):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user:
        return db_user
    else:
        return False


def get_user_by_phone(db: Session, phone: str):
    db_user = db.query(User).filter(User.phone == phone).first()
    if not db_user:
        return False
    return db_user


def get_user_by_google_id(db: Session, google_id: str):
    db_user = db.query(User).filter(User.googleId == google_id).first()
    if db_user:
        return db_user
    else:
        return False


def get_user_by_apple_id(db: Session, apple_id: str):
    db_user = db.query(User).filter(User.appleId == apple_id).first()
    if db_user:
        return db_user
    else:
        return False


def get_user_by_vk_id(db: Session, vk_id: str):
    db_user = db.query(User).filter(User.vkId == str(vk_id)).first()
    if db_user:
        return db_user
    else:
        return False


def create_user(db: Session, user: user_schema.UserCreate):
    if get_user_by_phone(db=db, phone=user.phone):
        return False
    db_user = User(uuid=uuid.uuid4(),
                   phone=user.phone,
                   phoneHidden=False,
                   name=user.name,
                   emailVerified=False,
                   phoneVerified=False,
                   password=security.hash_password(user.password),
                   roleId=1,
                   createdAt=datetime.datetime.utcnow())
    db.add(db_user)
    db.commit()
    return True


def authenticate_user(db: Session, username: str, password: str):
    db_user: User = get_user_by_phone(db=db, phone=username)
    if not db_user:
        return False
    if not security.verify_password(password, db_user.password):
        return False
    db_user.lastLoginAt = datetime.datetime.utcnow()
    db.commit()
    return db_user


def change_user_password(db: Session, user: User, new_password: str):
    user.password = new_password
    db.commit()


def create_user_oauth(db: Session, user: user_schema.UserCreateOauth):
    if user.photo:
        db_photo = UserPhoto(url=user.photo)
        db.add(db_photo)
        db.commit()
        db.refresh(db_photo)
        user.photoId = db_photo.id
    db_user = User(uuid=uuid.uuid4(),
                   email=user.email,
                   name=user.name,
                   surname=user.surname,
                   emailVerified=user.emailVerify,
                   phoneHidden=False,
                   googleId=user.googleId,
                   vkId=user.vkId,
                   appleId=user.appleId,
                   phoneVerified=False,
                   roleId=1,
                   photoId=user.photoId,
                   createdAt=datetime.datetime.utcnow())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_current_user(db: Session = Depends(get_db), access_token: str = Depends(dependencies.oauth2_scheme)):
    token_data = security.decode_access_token(access_token)
    user_id = token_data.get("sub")
    user: User = get_user_by_id(db=db, user_id=user_id)
    if not User:
        raise security.credentials_exception
    user_out = get_user_out(db_user=user)
    return user_out


def get_user_out(db_user: User):
    user_dict = db_user.__dict__
    user_dict["role"] = db_user.role.__dict__
    if db_user.photo:
        user_dict["photo"] = db_user.photo.__dict__
    user = user_schema.UserOut(**user_dict)
    return user


# def change_user_data(db: Session, user: User, user_data: user_schema.ChangeUser):
#     if user_data.email:
#         user.email = user_data.email
#     if user_data.phone:
#         user.phone = user_data.phone
#     db.commit()
