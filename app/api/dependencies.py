from fastapi.security import OAuth2PasswordBearer
from app.db.session import SessionLocal


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token", auto_error=False)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
