from sqlalchemy.orm import Session
import uuid
import datetime
from app.db.db_models import Post
from app.schemas import post as post_schema, user as user_schema


def create_post(db: Session, ):
    db_image_road = Post(
        uuid=uuid.uuid4()
    )
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

