from sqlalchemy.orm import Session
from fastapi import Depends
import uuid
import datetime
from app.api.dependencies import get_db
from app.db.db_models import Post, PostPhoto
from app.schemas import post as post_schema
from app.utils import security
from app.api import dependencies
from sqlalchemy import select


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

def get_post_out(db: Session, post_id:int):
    db_post = db.query(Post).filter(Post.id == post_id).first()
    if db_post:
        return db_post
    else: return False

def get_post_view(db: Session, post_id:int):
    db_post = db.query(Post.id, Post.title, Post.price, Post.description, Post.trade).filter(Post.id == post_id).first()
    if db_post:
        return db_post
    else: return False

def get_post_view_all(db: Session):
    db_post = db.query(Post.id, Post.title, Post.price, Post.description, Post.trade).all()
    print(db_post)
    if db_post:
        return db_post
    else: return False

