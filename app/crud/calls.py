from sqlalchemy.orm import Session
import uuid
import datetime
from app.db.db_models import User


# def create_call(db: Session, call_phone, phone_validate):
#     instance = db.query(User).filter(User.email == user.email).first()
#     if instance:
#         return False
#     else:
#         db_user = User(uuid=uuid.uuid4(),
#                        email=user.email,
#                        name=user.name,
#                        emailVerified=False,
#                        phoneVerified=False,
#                        password=security.hash_password(user.password),
#                        roleId=1,
#                        createdAt=datetime.datetime.utcnow())
#         db.add(db_user)
#         db.commit()
#         db.refresh(db_user)
#         user_dict = db_user.__dict__
#         user_dict["role"] = db_user.role.__dict__
#         if db_user.photo:
#             user_dict["photo"] = db_user.photo.__dict__
#         user = user_schema.UserOut(**user_dict)
#         return user
