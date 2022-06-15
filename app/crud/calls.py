from sqlalchemy.orm import Session
import datetime
from app.db.db_models import PhoneCalls


def create_call(db: Session, phone: str, validate_code: int):
    db_call = PhoneCalls(phone=phone,
                         phoneValidate=False,
                         ValidateCode=validate_code,
                         createdAt=datetime.datetime.utcnow())
    db.add(db_call)
    db.commit()
