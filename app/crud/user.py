from sqlalchemy.orm import Session
import uuid
import datetime
from app.db.db_models import User
from app.schemas import user as user_schema
from app.utils import security


def check_user_with_phone(db: Session, phone: str):
    db_user = db.query(User).filter(User.phone == phone).first()
    if db_user:
        return False
    return True


def create_user_phone(db: Session, user: user_schema.UserCreate):
    instance = db.query(User).filter(User.phone == user.phone).first()
    if instance:
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
