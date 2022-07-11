from sqlalchemy.orm import Session
from app.api.dependencies import get_db
from app.db.db_models import Role
from app.schemas import user as user_schema


roles = [{"id": 1, "title": "basic user"}]


def get_role_by_id(db: Session, role_id: int):
    db_role = db.query(Role).filter(Role.id == role_id).first()
    if db_role:
        return db_role
    else:
        return False


def create_role(db: Session, role: user_schema.UserRole):
    if get_role_by_id(db=db, role_id=role.id):
        return False
    db_role = Role(id=role.id,
                   title=role.title)
    db.add(db_role)
    db.commit()
    return True


def create_roles(db: Session = next(get_db())):
    for role in roles:
        create_role(db=db, role=user_schema.UserRole(**role))
