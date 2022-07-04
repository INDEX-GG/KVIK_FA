from sqlalchemy.orm import Session
from fastapi import Depends
import uuid
import datetime
from app.api.dependencies import get_db
from app.db.db_models import Post, PostPhoto
from app.schemas import post as post_schema
from app.utils import security
from app.api import dependencies


def create_post(db: Session, post: post_schema.PostCreate, user_id_out:int):
    db_post = Post(
        title=post.title,
        description=post.description,
        price=post.price,
        trade=post.trade,
        uuid=uuid.uuid4(),
        userId=user_id_out
    )

    db.add(db_post)
    db.commit()
    return True
