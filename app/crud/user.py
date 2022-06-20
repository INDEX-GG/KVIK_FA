from sqlalchemy.orm import Session
import uuid
import datetime
from app.db.db_models import User, UserPhoto
from app.schemas import user as user_schema
from app.utils import security


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
    return user
