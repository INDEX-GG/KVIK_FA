from sqlalchemy.orm import Session
import uuid
import datetime
from app.db.db_models import User
from app.schemas import user as user_schema
from app.utils import security


def check_user_by_phone(db: Session, phone: str):
    db_user = db.query(User).filter(User.phone == phone).first()
    if not db_user:
        return False
    return True


def create_user(db: Session, user: user_schema.UserCreate):
    if check_user_by_phone(db=db, phone=user.phone):
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
    db_user = db.query(User).filter(User.phone == username).first()
    if not db_user:
        return False
    if not security.verify_password(password, db_user.password):
        return False
    db_user.lastLoginAt = datetime.datetime.utcnow()
    db.commit()
    return db_user
