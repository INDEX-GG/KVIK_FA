from sqlalchemy.orm import Session
import datetime
from app.db.db_models import PhoneCalls, PhoneVerifyUnsuccessfulTry


def create_call(db: Session, phone: str, verification_code: str):
    db_call = PhoneCalls(phone=phone,
                         phoneValidate=False,
                         validateCode=verification_code,
                         createdAt=datetime.datetime.utcnow())
    db.add(db_call)
    db.commit()


def check_count_of_calls(db: Session, phone: str, max_count_of_calls_in_period: int = 3,
                         time_period_in_minutes: int = 30):
    time_limit = datetime.datetime.utcnow() - datetime.timedelta(minutes=time_period_in_minutes)
    db_calls = db.query(PhoneCalls).filter(PhoneCalls.phone == phone, PhoneCalls.createdAt >= time_limit).all()
    if len(db_calls) >= max_count_of_calls_in_period:
        return False
    return True


def check_verification_code(db: Session, phone: str, verification_code: str, time_period_in_minutes: int = 5):
    time_limit = datetime.datetime.utcnow() - datetime.timedelta(minutes=time_period_in_minutes)
    db_call = db.query(PhoneCalls)\
        .filter(PhoneCalls.phone == phone, PhoneCalls.createdAt >= time_limit, PhoneCalls.phoneValidate == False)\
        .order_by(PhoneCalls.createdAt.desc()).first()
    if not db_call:
        create_unsuccessful_try_record(db=db, phone=phone)
        return False
    if verification_code != db_call.validateCode:
        create_unsuccessful_try_record(db=db, phone=phone)
        return False
    db_call.phoneValidate = True
    db.commit()
    return True


def create_unsuccessful_try_record(db: Session, phone: str):
    db_spam_record = PhoneVerifyUnsuccessfulTry(phone=phone, createdAt=datetime.datetime.utcnow())
    db.add(db_spam_record)
    db.commit()


def check_count_of_unsuccessful_try_verif_code(db: Session, phone: str,
                                               max_count_of_unsuccessful_try_in_period: int = 5,
                                               time_period_in_minutes: int = 5):
    time_limit = datetime.datetime.utcnow() - datetime.timedelta(minutes=time_period_in_minutes)
    db_try = db.query(PhoneVerifyUnsuccessfulTry).filter(PhoneVerifyUnsuccessfulTry.phone == phone,
                                                         PhoneVerifyUnsuccessfulTry.createdAt >= time_limit).all()
    if len(db_try) >= max_count_of_unsuccessful_try_in_period:
        return False
    return True
