from sqlalchemy.orm import Session
from app.api.dependencies import get_db
from app.db.db_models import Role, PostsStatus
from app.schemas import user as user_schema, post as post_schema


roles = [{"id": 1, "title": "basic user"}]
posts_statuses = [
    {"id": 1, "title": "photo load in progress"},
    {"id": 2, "title": "being checked by a moderator"},
    {"id": 3, "title": "rejected by moderator"},
    {"id": 4, "title": "active"},
    {"id": 5, "title": "removed from publication by user"},
    {"id": 6, "title": "posting expired"}
]


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


def get_post_status_by_id(db: Session, status_id: int):
    db_status = db.query(PostsStatus).filter(PostsStatus.id == status_id).first()
    if db_status:
        return db_status
    else:
        return False


def create_post_status(db: Session, status: post_schema.PostStatus):
    if get_post_status_by_id(db=db, status_id=status.id):
        return False
    db_status = PostsStatus(id=status.id, title=status.title)
    db.add(db_status)
    db.commit()
    return True


def create_posts_statuses(db: Session = next(get_db())):
    for post_status in posts_statuses:
        create_post_status(db=db, status=post_schema.PostStatus(**post_status))
